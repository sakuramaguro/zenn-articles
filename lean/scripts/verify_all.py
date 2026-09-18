#!/usr/bin/env python3
"""Run the book's build, diagnostics and every isolated source check."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

import catalog

STAGES = ('2', '3a', '3b', '3c', '4a', '4b', '4c')


def check_coverage(data, actual, build, reports):
    """Reject omitted, stale, or failed evidence, including exercises' diagnostics."""
    completed = {b['id'] for b in data['blocks'] if b['category'] in {'complete', 'fragment'}}
    diagnostic = {b['id'] for b in data['blocks'] if b['category'] in {'expected_error', 'unfinished'}}
    if completed | diagnostic != set(actual):
        raise ValueError('Unreviewed block category')
    if build['status'] != 'passed' or set(build['compiled_source_blocks']) != completed:
        raise ValueError('Build coverage differs from completed manuscript blocks')
    required_cases = {case['id']: case for case in data['diagnostics']}
    if set(build['diagnostics']) != set(required_cases):
        raise ValueError('Diagnostic case coverage differs')
    diagnosed = set()
    for name, result in build['diagnostics'].items():
        case = required_cases[name]
        if result['kind'] != case['kind'] or result['blocks'] != case['blocks']:
            raise ValueError('Diagnostic identity differs')
        if case['kind'] == 'error' and not result.get('expected_reason_confirmed'):
            raise ValueError('Expected error reason not confirmed')
        if case['kind'] == 'sorry' and not result.get('expected_warning_confirmed'):
            raise ValueError('Expected sorry warning not confirmed')
        if case['kind'] != 'pass':
            diagnosed.update(result['blocks'])
    if diagnosed != diagnostic:
        raise ValueError('Diagnostic source coverage differs')
    checked = Counter()
    for report in reports:
        if report['status'] != 'passed' or report['toolchain'] != build['toolchain']:
            raise ValueError('Failed result or different toolchain')
        for case in report['checks']:
            if case['status'] != 'passed' or case['exit_code'] != 0:
                raise ValueError('Unsuccessful isolated case')
            blocks = case.get('setup', []) + case['blocks']
            if set(case['source_sha256']) != set(blocks):
                raise ValueError('Missing source hash evidence')
            for block in blocks:
                if block not in actual or case['source_sha256'][block] != actual[block]['sha256']:
                    raise ValueError('Stale isolated source evidence')
            checked.update(case['blocks'])
    if set(checked) != completed:
        raise ValueError('Isolated source coverage differs')
    return {'completed_blocks': len(completed), 'diagnostic_blocks': len(diagnostic),
            'isolated_cases': sum(len(r['checks']) for r in reports),
            'repeated_targets': {b: n for b, n in checked.items() if n > 1}}


def main():
    directory = catalog.ROOT / '.generated'
    directory.mkdir(exist_ok=True)
    result_file = directory / 'full-verification.json'
    result_file.unlink(missing_ok=True)
    data, actual = catalog.validate()
    catalog.check_documents(data)
    names = ['verification.json'] + [f'stage{s}-source-checks.json' for s in STAGES]
    # A stopped or failed run must not reuse an earlier stage's success record.
    for name in names:
        (directory / name).unlink(missing_ok=True)
    scripts = ['test_validation.py', 'verify.py'] + [f'check_stage{s}_sources.py' for s in STAGES]
    for script in scripts:
        print(f'Running {script}', flush=True)
        subprocess.run([sys.executable, 'scripts/' + script], cwd=catalog.ROOT, check=True)
    build, *reports = [json.loads((directory / name).read_text()) for name in names]
    coverage = check_coverage(data, actual, build, reports)
    result = dict(status='passed', checked_at=datetime.now(timezone.utc).isoformat(),
                  source_files=data['source_files'], toolchain=build['toolchain'],
                  dependencies=build['dependencies'], catalog_blocks=len(actual),
                  audited_declarations=len(build['audited_declarations']),
                  diagnostic_cases=len(build['diagnostics']), reports=names, coverage=coverage)
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(coverage), flush=True)
    print('Full verification passed: .generated/full-verification.json', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
