#!/usr/bin/env python3
"""Check chapters 10 and 11 with explicit, original setup and proof sequences."""
from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import catalog
from verify import DIAGNOSTIC_PATTERN, LOGS, parse_axioms, run

ROOT = catalog.ROOT
SEQUENCES = [
    ['ch10_007', 'ch10_008'],
    ['ch11_006', 'ch11_007', 'ch11_008', 'ch11_009', 'ch11_010', 'ch11_011'],
    ['ch11_014', 'ch11_015'],
]
EXCLUDED = {'ch10_023', 'ch11_017', 'ch11_020'}
SETUP_OVERRIDES = {
    'ch10_001': [],
    'ch10_012': [1, 11],
    'ch10_013': [1, 11, 12],
    'ch10_015': [1, 11, 12, 13],
    'ch10_017': [1, 11, 12, 13],
    'ch10_020': [1, 11, 12, 13],
    'ch10_024': [1, 4],
    'ch10_025': [1, 4],
    'ch11_001': [],
    'ch11_013': [1, 12],
    'ch11_016': [1, 12],
    'ch11_023': [1, 12, 21],
    'ch11_024': [1, 12, 21, 23],
    'ch11_025': [1, 12, 16],
    'ch11_026': [1, 12, 14, 15, 16, 25],
}


def source_cases() -> list[dict]:
    joined = {block for sequence in SEQUENCES for block in sequence}
    blocks = [[f'{ch}_{n:03}'] for ch in ['ch10', 'ch11'] for n in range(1, 27)
              if f'{ch}_{n:03}' not in joined | EXCLUDED] + SEQUENCES
    cases = []
    for target in sorted(blocks):
        head = target[0]
        setup = [f'{head[:4]}_{n:03}' for n in SETUP_OVERRIDES.get(head, [1])]
        cases.append(dict(blocks=target, setup=setup))
    return cases


def main() -> None:
    result_file = ROOT / '.generated/stage3c-source-checks.json'
    result_file.unlink(missing_ok=True)
    data, actual = catalog.validate()
    ids = [m['block'] for m in data['compiled_mappings']
           if m['block'][:4] in {'ch10', 'ch11'}]
    cases = source_cases()
    flattened = [b for case in cases for b in case['blocks']]
    if len(ids) != len(set(ids)) or sorted(flattened) != sorted(ids):
        raise ValueError('Stage 3-C target coverage differs from compiled mappings')
    for case in cases:
        target, setup = case['blocks'], case['setup']
        if len(setup) != len(set(setup)) or set(target) & set(setup):
            raise ValueError(f'Duplicated setup or target: {case}')
        if not set(setup) <= set(ids) or any(b >= target[0] for b in setup):
            raise ValueError(f'Setup must use earlier compiled manuscript blocks: {case}')

    directory = ROOT / '.generated/stage3c/source-checks'
    directory.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    def check(case: dict) -> dict:
        target, setup = case['blocks'], case['setup']
        identity = '-'.join(target)
        all_blocks = setup + target
        code = '\n'.join(actual[b]['code'] for b in all_blocks)
        names = re.findall(r'^(?:noncomputable )?(?:def|theorem|lemma) (\w+)', code, re.M)
        if len(names) != len(set(names)):
            raise ValueError(f'{identity}: duplicate declaration names')
        for name in names:
            if not re.search(r'^#print axioms ' + re.escape(name) + r'\s*$', code, re.M):
                code += '\n#print axioms ' + name + '\n'
        path = directory / (identity + '.lean')
        path.write_text(code)
        output = run(['lake', 'env', 'lean', '-DwarningAsError=true', '-DautoImplicit=false',
                      str(path.relative_to(ROOT))], 'source-stage3c-' + identity + '.log')
        if re.search(DIAGNOSTIC_PATTERN, output) or 'sorryAx' in output:
            raise ValueError(f'{identity}: unexpected diagnostic or unfinished proof')
        axioms = parse_axioms(output, names)
        print(identity + ': passed', flush=True)
        return dict(blocks=target, setup=setup, status='passed', exit_code=0,
                    source_sha256={b: actual[b]['sha256'] for b in all_blocks},
                    audited_declarations=axioms)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(check, cases))
    result = dict(status='passed', stage='3-C', checked_at=datetime.now(timezone.utc).isoformat(),
                  toolchain=(ROOT / 'lean-toolchain').read_text().strip(),
                  method='Separate Lean processes; explicit original setup blocks and joined sequences; '
                         'warningAsError=true; autoImplicit=false; all named declarations audited',
                  checks=results)
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'Passed: {len(results)} cases / {len(ids)} target blocks; setup reuse counted separately', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
