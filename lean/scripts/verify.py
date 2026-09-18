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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import catalog

ROOT = catalog.ROOT
LOGS = ROOT / '.generated/logs'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
DIAGNOSTIC_PATTERN = r'\b(error|warning)(?:\([^\n]*?\))?:'


def run(args: list[str], logfile: str, cwd: Path = ROOT, expected_returncode: int = 0) -> str:
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
    if process.returncode != expected_returncode:
        raise RuntimeError(f'Unexpected exit code {process.returncode}, expected {expected_returncode}; see .generated/logs/{logfile}')
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


def validate_diagnostic_output(case: dict, output: str) -> dict:
    kind = case['kind']
    # Lean also emits coded diagnostics such as error(lean.unknownIdentifier).
    severities = re.findall(DIAGNOSTIC_PATTERN, output)
    if kind == 'error':
        errors = severities.count('error')
        if errors != case['error_count'] or any(pattern not in output for pattern in case['patterns']):
            raise ValueError(f'{case["id"]}: expected error reason differs')
        return {'kind': kind, 'errors': errors, 'expected_reason_confirmed': True}
    name = case['declaration']
    if kind == 'pass':
        if severities:
            raise ValueError(f'{case["id"]}: unexpected diagnostic')
        return {'kind': kind, 'axioms': parse_axioms(output, [name])[name]}
    match = re.search(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", output)
    axioms = {x.strip() for x in match[1].split(',')} if match else set()
    if ('warning: declaration uses `sorry`' not in output or 'error' in severities
            or 'sorryAx' not in axioms or not axioms <= ALLOWED_AXIOMS | {'sorryAx'}):
        raise ValueError(f'{case["id"]}: expected sorry warning/axioms differ')
    return {'kind': kind, 'axioms': sorted(axioms), 'expected_warning_confirmed': True}


def check_diagnostics(data: dict, actual: dict) -> dict:
    directory = ROOT / '.generated/diagnostics'
    directory.mkdir(exist_ok=True)

    def check(case):
        # Each lesson runs in a separate Lean process. Its assumptions cannot
        # enter the completed LeanBook modules or the main axiom audit.
        content = '\n'.join(actual[b]['code'] for b in case['blocks']) + case.get('append', '')
        path = directory / (case['id'] + '.lean')
        path.write_text(content)
        output = run(['lake', 'env', 'lean', '-DwarningAsError=false', str(path.relative_to(ROOT))],
                     f'diagnostic-{case["id"]}.log', expected_returncode=1 if case['kind'] == 'error' else 0)
        result = validate_diagnostic_output(case, output)
        return case['id'], dict(result, blocks=case['blocks'])

    with ThreadPoolExecutor(max_workers=2) as pool:
        return dict(pool.map(check, data.get('diagnostics', [])))


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
    print(f'Build and {len(axioms)} axiom checks passed. Checking manuscript diagnostics...', flush=True)
    diagnostics = check_diagnostics(data, actual)
    result = dict(status='passed', checked_at=datetime.now(timezone.utc).isoformat(),
                  review_base=data['review_base'], toolchain=toolchain, lean_version=version,
                  dependencies=dependencies, manuscript_files=len(data['source_files']),
                  catalog_blocks=len(actual), compiled_source_blocks=[m['block'] for m in data['compiled_mappings']],
                  audited_declarations=axioms, diagnostics=diagnostics,
                  verification_stage=data.get('verification_stage', '0'),
                  scope='Selected manuscript blocks and reference corrections; not the whole book')
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'Build passed. Completed declarations: {len(axioms)}; no sorryAx. Diagnostic cases: {len(diagnostics)}.', flush=True)
    print('Result: .generated/verification.json; logs: .generated/logs/')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
