#!/usr/bin/env python3
"""Check the catalog, pinned dependencies, build, and named declaration axioms."""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import catalog

ROOT = catalog.ROOT
LOGS = ROOT / '.generated/logs'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def run(args: list[str], logfile: str, cwd: Path = ROOT) -> str:
    process = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, start_new_session=True)
    try:
        output, _ = process.communicate(timeout=900)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        output, _ = process.communicate()
        (LOGS / logfile).write_text(output)
        raise RuntimeError(f'Timeout; see .generated/logs/{logfile}')
    (LOGS / logfile).write_text(output)
    if process.returncode:
        raise RuntimeError(f'Command failed ({process.returncode}); see .generated/logs/{logfile}')
    return output


def parse_axioms(output: str, expected: list[str]) -> dict[str, list[str]]:
    dependencies = {}
    pattern = r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)"
    for match in re.finditer(pattern, output):
        name, raw = match.groups()
        if name in dependencies:
            raise ValueError(f'Duplicate audit output for {name}')
        deps = [item.strip() for item in (raw or '').split(',') if item.strip()]
        unexpected = set(deps) - ALLOWED_AXIOMS
        if unexpected:
            raise ValueError(f'{name}: unreviewed axioms {sorted(unexpected)}')
        dependencies[name] = deps
    if set(dependencies) != set(expected):
        raise ValueError(f'Audit coverage mismatch: {set(dependencies) ^ set(expected)}')
    return dependencies


def main() -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    result_file = ROOT / '.generated/verification.json'
    result_file.unlink(missing_ok=True)
    data, actual = catalog.validate()
    catalog.check_documents(data)
    print(f'Catalog: {len(actual)} blocks, {len(data["source_files"])} source files', flush=True)

    manifest = json.loads((ROOT / 'lake-manifest.json').read_text())
    dependencies = {}
    for package in manifest['packages']:
        if package['type'] != 'git':
            raise ValueError('Unreviewed non-git dependency')
        path = ROOT / manifest['packagesDir'] / package['name']
        revision = run(['git', 'rev-parse', 'HEAD'], f'dep-{package["name"]}-rev.log', path).strip()
        changes = run(['git', 'status', '--porcelain', '--untracked-files=no'],
                      f'dep-{package["name"]}-status.log', path).strip()
        if revision != package['rev'] or changes:
            raise ValueError(f'Dependency revision/worktree differs: {package["name"]}')
        dependencies[package['name']] = revision
    toolchain = (ROOT / 'lean-toolchain').read_text().strip()
    version = run(['lake', 'env', 'lean', '--version'], 'version.log').strip()
    expected_version = toolchain.rsplit(':v', 1)[-1]
    if not version.startswith(f'Lean (version {expected_version},'):
        raise ValueError(f'Unexpected Lean version: {version}')
    print('Pinned environment: checked. Building LeanBook...', flush=True)
    build = run(['lake', 'build'], 'build.log')
    if re.search(r'\bwarning:|\bsorryAx\b', build):
        raise ValueError('Build contains warnings or sorryAx; inspect build.log')

    expected = re.findall(r'^#print axioms (\S+)\s*$', (ROOT / 'Audit.lean').read_text(), re.M)
    if not expected or len(expected) != len(set(expected)):
        raise ValueError('Empty or duplicate audit target list')
    output = run(['lake', 'env', 'lean', 'Audit.lean'], 'axioms.log')
    if re.search(r'\bwarning:|\bsorryAx\b', output):
        raise ValueError('Audit contains warnings or sorryAx')
    axioms = parse_axioms(output, expected)
    result = dict(status='passed', checked_at=datetime.now(timezone.utc).isoformat(),
                  review_base=data['review_base'], toolchain=toolchain, lean_version=version,
                  dependencies=dependencies, manuscript_files=len(data['source_files']),
                  catalog_blocks=len(actual), compiled_source_blocks=[m['block'] for m in data['compiled_mappings']],
                  audited_declarations=axioms,
                  scope='Stage 0 reference examples and two manuscript blocks; not all 421 blocks')
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'Build passed. Axioms checked: {len(axioms)} declarations; no sorryAx.', flush=True)
    print('Result: .generated/verification.json; logs: .generated/logs/')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
