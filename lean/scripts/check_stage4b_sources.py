#!/usr/bin/env python3
"""Check chapters 15–16 and the related chapter 17 indicator with original setup."""
from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import catalog
from verify import DIAGNOSTIC_PATTERN, LOGS, parse_axioms, run

ROOT = catalog.ROOT
SETUP = {'ch16_015': ['ch16_014'], 'ch16_017': ['ch16_007']}
RELATED = ['ch17_010']


def main() -> None:
    result_file = ROOT / '.generated/stage4b-source-checks.json'
    result_file.unlink(missing_ok=True)
    data, actual = catalog.validate()
    ids = [m['block'] for m in data['compiled_mappings']
           if m['block'][:4] in {'ch15', 'ch16'} or m['block'] in RELATED]
    expected = [b['id'] for b in data['blocks'] if b['id'][:4] in {'ch15', 'ch16'}] + RELATED
    if len(ids) != len(set(ids)) or sorted(ids) != sorted(expected):
        raise ValueError('Stage 4-B coverage differs from all chapter blocks and related examples')
    cases = [dict(blocks=[b], setup=SETUP.get(b, [])) for b in sorted(expected)]
    for case in cases:
        target, setup = case['blocks'], case['setup']
        if len(setup) != len(set(setup)) or set(target) & set(setup):
            raise ValueError(f'Duplicated setup or target: {case}')
        if not set(setup) <= set(ids) or any(b >= target[0] for b in setup):
            raise ValueError(f'Setup must use earlier compiled manuscript blocks: {case}')

    directory = ROOT / '.generated/stage4b/source-checks'
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
                      str(path.relative_to(ROOT))], 'source-stage4b-' + identity + '.log')
        if re.search(DIAGNOSTIC_PATTERN, output) or 'sorryAx' in output:
            raise ValueError(f'{identity}: unexpected diagnostic or unfinished proof')
        axioms = parse_axioms(output, names)
        print(identity + ': passed', flush=True)
        return dict(blocks=target, setup=setup, status='passed', exit_code=0,
                    source_sha256={b: actual[b]['sha256'] for b in all_blocks},
                    audited_declarations=axioms)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(check, cases))
    result = dict(status='passed', stage='4-B', checked_at=datetime.now(timezone.utc).isoformat(),
                  toolchain=(ROOT / 'lean-toolchain').read_text().strip(),
                  method='Separate Lean processes; original imports and explicit setup blocks; '
                         'warningAsError=true; autoImplicit=false; all named declarations audited',
                  related_blocks=RELATED, checks=results)
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'Passed: {len(results)} cases / {len(ids)} target blocks; setup reuse counted separately', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
