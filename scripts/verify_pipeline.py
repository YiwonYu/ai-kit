#!/usr/bin/env python3
"""Execute a declared verification suite and preserve evidence. No external dependencies."""
import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import subprocess
import sys
import uuid

from run_experiment import git_info

CATEGORIES = {'structure', 'unit', 'integration', 'e2e', 'negative', 'boundary', 'other'}


def load_config(path):
    '''Load and validate verification requirements and checks.

    Args:
        path: JSON verification configuration path.
    Returns:
        Validated configuration mapping. Raises ValueError for invalid declarations.
    '''
    config = json.loads(path.read_text())
    if not isinstance(config, dict) or not isinstance(config.get('scope'), str) or not config['scope'].strip():
        raise ValueError('scope must explain what this suite actually verifies')
    checks = config.get('checks')
    if not isinstance(checks, list) or not checks:
        raise ValueError('checks must be a nonempty list')
    ids = set()
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError('each check must be an object')
        name = check.get('id')
        if not isinstance(name, str) or not name.strip() or name in ids:
            raise ValueError('check IDs must be unique nonempty strings')
        ids.add(name)
        if not isinstance(check.get('name'), str) or not check['name'].strip():
            raise ValueError('checks need readable names')
        if check.get('category') not in CATEGORIES:
            raise ValueError('unknown category')
        if not isinstance(check.get('required', True), bool) or not isinstance(check.get('pending', False), bool):
            raise ValueError('required and pending must be booleans')
        if not isinstance(check.get('oracle'), str) or not check['oracle'].strip():
            raise ValueError('each check needs an oracle / expected-result explanation')
        timeout = check.get('timeout', 60)
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError('timeout must be positive and finite')
        expected = check.get('expected_exit', 0)
        if isinstance(expected, bool) or not isinstance(expected, int):
            raise ValueError('expected_exit must be an integer')
        if check.get('pending'):
            continue
        if check.get('category') == 'structure':
            paths = check.get('paths')
            if not isinstance(paths, list) or not paths:
                raise ValueError('structure checks need paths')
            for entry in paths:
                if not isinstance(entry, dict) or not isinstance(entry.get('path'), str) or not entry['path']:
                    raise ValueError('invalid structure path')
                if Path(entry['path']).is_absolute() or '..' in Path(entry['path']).parts:
                    raise ValueError('structure paths must stay inside project')
                if entry.get('kind') not in ('file', 'directory'):
                    raise ValueError('structure kind must be file or directory')
        else:
            command = check.get('command')
            if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
                raise ValueError('command must be a nonempty argv list')
    categories = config.get('required_categories', [])
    if not isinstance(categories, list) or not set(categories) <= CATEGORIES:
        raise ValueError('invalid required_categories')
    required_checks = {c['id'] for c in checks if c.get('required', True)}
    for category in categories:
        if not any(c['category'] == category and c['id'] in required_checks for c in checks):
            raise ValueError(f'no required check for category: {category}')
    requirements = config.get('requirements')
    if not isinstance(requirements, list) or not requirements:
        raise ValueError('requirements must map requirements to required checks')
    req_ids = set()
    for req in requirements:
        if not isinstance(req, dict) or not isinstance(req.get('id'), str) or not req['id'] or req['id'] in req_ids:
            raise ValueError('requirement IDs must be unique nonempty strings')
        req_ids.add(req['id'])
        refs = req.get('checks')
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref in required_checks for ref in refs):
            raise ValueError('each requirement must reference existing required checks')
    return config


def structure_result(root, check):
    '''Compare required project paths with the layout contract.

    Args:
        root: Resolved project root.
        check: Structure check with relative paths and expected kinds.
    Returns:
        Status and a list of missing, mismatched or external paths.
    '''
    details = []
    for entry in check['paths']:
        target = (root / entry['path']).resolve()
        if not target.is_relative_to(root):
            details.append(f"outside project: {entry['path']}")
        elif not (target.is_file() if entry['kind'] == 'file' else target.is_dir()):
            details.append(f"missing or wrong type: {entry['path']} ({entry['kind']})")
    return {'status': 'failed' if details else 'passed', 'details': details}


def execute(root, check, folder):
    '''Execute one check and collect its evidence.

    Args:
        root: Resolved project working directory.
        check: Validated check declaration.
        folder: Unique directory for this check evidence.
    Returns:
        Status, command result and log paths; blocked for pending checks.
    '''
    if check.get('pending'):
        return {'status': 'blocked', 'details': ['test not implemented: ' + check.get('reason', 'pending')]}
    if check['category'] == 'structure':
        return structure_result(root, check)
    command = [sys.executable if token == '{python}' else token for token in check['command']]
    runner = Path(__file__).with_name('run_experiment.py')
    logs = folder / 'execution'
    args = [sys.executable, str(runner), '--name', check['name'], '--timeout', str(check.get('timeout', 60)),
            '--cwd', str(root), '--output-dir', str(logs), '--', *command]
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / 'runner.log').open('wb') as out:
        subprocess.run(args, stdout=out, stderr=subprocess.STDOUT, check=False)
    matches = list(logs.glob('*/metadata.json'))
    if len(matches) != 1:
        return {'status': 'blocked', 'details': ['runner did not produce metadata'], 'runner_log': str(folder / 'runner.log')}
    meta_path = matches[0]
    meta = json.loads(meta_path.read_text())
    completed = meta['status'] in ('success', 'failed')
    ok = completed and meta['returncode'] == check.get('expected_exit', 0)
    return {'status': 'passed' if ok else 'failed', 'command': command,
            'expected_exit': check.get('expected_exit', 0), 'returncode': meta['returncode'],
            'execution_status': meta['status'], 'elapsed_seconds': meta['elapsed_seconds'],
            'metadata': str(meta_path), 'stdout': str(meta_path.parent / 'stdout.log'),
            'stderr': str(meta_path.parent / 'stderr.log')}


def main():
    '''Run the declared verification suite and write reports.

    Args:
        None. Uses enclosing state or CLI arguments.
    Returns:
        CLI exit code; JSON/Markdown reports and logs under the output directory.
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path('verification.json'))
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output-dir', type=Path, default=Path('runs/verification'))
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error('--root must exist')
    try:
        config_path = args.config.resolve()
        config = load_config(config_path)
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f'invalid verification config: {exc}\n')
    run = args.output_dir.resolve() / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex)
    run.mkdir(parents=True)
    # Snapshot the declared tests along with the code revision; future config edits cannot rewrite evidence.
    (run / 'config.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n')
    report = {'scope': config['scope'], 'root': str(root), 'config': str(config_path),
              'started_at': datetime.now(timezone.utc).isoformat(), 'git': git_info(root),
              'status': 'running', 'requirements': config['requirements'], 'checks': []}
    def save():
        '''Write the current verification report atomically.

        Args:
            None. Uses enclosing state or CLI arguments.
        Returns:
            None. Updates report.json in the enclosing run directory.
        '''
        path = run / 'report.json'
        temp = path.with_suffix('.tmp')
        temp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        temp.replace(path)
    save()
    interrupted = False
    try:
        for index, check in enumerate(config['checks']):
            try:
                result = execute(root, check, run / f'check-{index + 1:03}')
            except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
                result = {'status': 'blocked', 'details': [str(exc)]}
            result.update(id=check['id'], name=check['name'], category=check['category'],
                          required=check.get('required', True), oracle=check['oracle'])
            report['checks'].append(result)
            save()
    except KeyboardInterrupt:
        interrupted = True
    complete = len(report['checks']) == len(config['checks'])
    ok = complete and not interrupted and all(c['status'] == 'passed' for c in report['checks'] if c['required'])
    report.update(status='passed' if ok else 'failed', ended_at=datetime.now(timezone.utc).isoformat())
    save()
    def cell(value):
        '''Escape a value for a Markdown table cell.

        Args:
            value: Object to render as text.
        Returns:
            Single-line string with escaped table separators.
        '''
        return str(value).replace('|', '\\|').replace('\n', ' ')
    lines = ['# Verification', '', f"- Scope: {config['scope']}",
             f"- Result: {report['status']}", f"- Code: {report['git']}",
             '- Evidence: report.json, config.json and execution logs', '',
             '| Check | Category | Required | Result | Oracle |', '|---|---|---|---|---|']
    for check in report['checks']:
        lines.append('| ' + ' | '.join(cell(check[k]) for k in ('name', 'category', 'required', 'status', 'oracle')) + ' |')
    counts = {status: sum(c['status'] == status for c in report['checks'])
              for status in ('passed', 'failed', 'blocked')}
    lines.extend(['', f"- Checks: passed {counts['passed']} / failed {counts['failed']} / blocked {counts['blocked']}"])
    remaining = [c['name'] for c in report['checks'] if c['status'] != 'passed']
    if remaining:
        lines.append('- Next checks: ' + ', '.join(remaining))
    (run / 'report.md').write_text('\n'.join(lines) + '\n')
    print(f"verification: {report['status']}\nreport: {run / 'report.md'}")
    return 130 if interrupted else (0 if ok else 1)


if __name__ == '__main__':
    sys.exit(main())
