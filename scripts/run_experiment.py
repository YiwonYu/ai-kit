#!/usr/bin/env python3
"""Run a command without a shell; preserve per-run logs and metadata."""
import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid


def utc_now():
    '''Format current UTC time.

    Args:
        None. Uses enclosing state or CLI arguments.
    Returns:
        ISO 8601 timestamp string.
    '''
    return datetime.now(timezone.utc).isoformat()


def git_info(cwd):
    '''Read repository revision and working-tree state.

    Args:
        cwd: Directory for Git inspection.
    Returns:
        Mapping with commit hash and dirty flag; None when unavailable.
    '''
    def query(args):
        '''Read one Git query.

        Args:
            args: Git subcommand and arguments.
        Returns:
            Stripped output, or None on failure.
        '''
        try:
            return subprocess.check_output(['git', *args], cwd=cwd,
                stderr=subprocess.DEVNULL, text=True, timeout=3).strip()
        except (OSError, subprocess.SubprocessError):
            return None
    status = query(['status', '--porcelain'])
    return {'commit': query(['rev-parse', 'HEAD']),
            'dirty': None if status is None else bool(status)}


def stop(proc):
    '''Terminate an experiment and wait for exit.

    Args:
        proc: Running Popen process; POSIX group or Windows child.
    Returns:
        None. The process is terminated and reaped.
    '''
    try:
        if os.name == 'posix':
            os.killpg(proc.pid, signal.SIGKILL)
        elif proc.poll() is None:
            proc.kill()
    except ProcessLookupError:
        pass
    proc.wait()


def main():
    '''Run a command with timeout, seed and evidence capture.

    Args:
        None. Uses enclosing state or CLI arguments.
    Returns:
        CLI exit code; logs and metadata written under the run directory.
    '''
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--name', default='experiment')
    p.add_argument('--timeout', type=float, required=True, help='positive seconds')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--output-dir', type=Path, default=Path('runs'))
    p.add_argument('--cwd', type=Path, default=Path.cwd())
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    command = a.command[1:] if a.command[:1] == ['--'] else a.command
    if not command:
        p.error('a command after -- is required')
    if not math.isfinite(a.timeout) or a.timeout <= 0:
        p.error('--timeout must be finite and positive')
    cwd = a.cwd.resolve()
    if not cwd.is_dir():
        p.error('--cwd must be an existing directory')
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex
    try:
        run_dir = a.output_dir.resolve() / run_id
        run_dir.mkdir(parents=True)
    except OSError as exc:
        p.exit(2, f'cannot create run directory: {exc}\n')
    meta = {'id': run_id, 'name': a.name, 'command': command, 'cwd': str(cwd),
            'seed': a.seed, 'timeout_seconds': a.timeout, 'started_at': utc_now(),
            'status': 'running', 'git': git_info(cwd)}
    path = run_dir / 'metadata.json'
    def save():
        '''Persist the current run metadata atomically.

        Args:
            None. Uses enclosing state or CLI arguments.
        Returns:
            None. Writes the enclosing metadata to metadata.json.
        '''
        temp = path.with_suffix('.tmp')
        temp.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
        temp.replace(path)
    save()
    print(f'run_dir: {run_dir}', flush=True)
    start = time.monotonic()
    proc = None
    result = 2
    try:
        with (run_dir / 'stdout.log').open('wb') as out, (run_dir / 'stderr.log').open('wb') as err:
            env = os.environ.copy()
            env['HARNESS_SEED'] = str(a.seed)
            proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=out, stderr=err,
                                    start_new_session=(os.name == 'posix'))
            try:
                rc = proc.wait(timeout=a.timeout)
                meta['status'] = 'success' if rc == 0 else 'failed'
                result = 0 if rc == 0 else 1
            except subprocess.TimeoutExpired:
                stop(proc)
                meta['status'] = 'timeout'
                result = 124
    except KeyboardInterrupt:
        if proc is not None:
            stop(proc)
        meta['status'] = 'interrupted'
        result = 130
    except OSError as exc:
        meta['status'] = 'launch_error'
        meta['error'] = str(exc)
    finally:
        meta.update(ended_at=utc_now(), elapsed_seconds=time.monotonic() - start,
                    returncode=proc.returncode if proc is not None else None)
        save()
    print(f"status: {meta['status']} ({meta['elapsed_seconds']:.3f}s)")
    return result


if __name__ == '__main__':
    sys.exit(main())
