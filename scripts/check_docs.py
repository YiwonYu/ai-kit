#!/usr/bin/env python3
"""Check source docstrings and English project text."""
import ast
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def inspect_file(path):
    '''Check one Python file for documented functions.

    Args:
        path: Python source path.
    Returns:
        List of missing or malformed function docstring errors.
    '''
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source, filename=str(path))
    errors = []
    lines = source.splitlines()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        doc = ast.get_docstring(node)
        first = node.body[0]
        if not doc or 'Args:' not in doc or 'Returns:' not in doc:
            errors.append(f'{path.relative_to(ROOT)}:{node.lineno}: {node.name}: purpose/Args/Returns required')
        elif not lines[first.lineno - 1].lstrip().startswith("'''"):
            errors.append(f'{path.relative_to(ROOT)}:{node.lineno}: {node.name}: triple single quotes required')
    return errors


def main():
    '''Validate repository text and Python function documentation.

    Args:
        None. Paths are relative to the kit root.
    Returns:
        Exit code: 0 for success, 1 for documentation errors.
    '''
    errors = []
    ignored = {'.git', 'runs', '__pycache__', '.venv'}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or any(part in ignored for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix not in {'.py', '.md', '.json', '.yml', '.yaml'}:
            continue
        text = path.read_text(encoding='utf-8')
        if re.search(r'[\uac00-\ud7a3]', text):
            errors.append(f'{path.relative_to(ROOT)}: English text required')
        if path.suffix == '.py':
            errors.extend(inspect_file(path))
    for error in errors:
        print(error, file=sys.stderr)
    print(f'Documentation: {len(errors)} errors')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
