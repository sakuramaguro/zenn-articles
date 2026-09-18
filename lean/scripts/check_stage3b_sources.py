#!/usr/bin/env python3
"""Check stage 3-B examples in isolation, joining only explicit manuscript sequences."""
from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import catalog
from verify import DIAGNOSTIC_PATTERN, LOGS, parse_axioms, run

ROOT = catalog.ROOT
SEQUENCES = [['ch08_010', 'ch08_011', 'ch08_012', 'ch08_013', 'ch08_014'], ['ch08_021', 'ch08_022'], ['ch08_024', 'ch08_025', 'ch08_026', 'ch08_027'], ['ch09_005', 'ch09_006'], ['ch09_012', 'ch09_013'], ['ch09_014', 'ch09_015', 'ch09_016', 'ch09_017']]


def main() -> None:
    result_file = ROOT / '.generated/stage3b-source-checks.json'
    result_file.unlink(missing_ok=True)
    data, actual = catalog.validate()
    chapters = {'ch08', 'ch09'}
    ids = [m['block'] for m in data['compiled_mappings']
           if m['block'].split('_')[0] in chapters]
    used = {b for sequence in SEQUENCES for b in sequence}
    cases = [[b] for b in sorted(ids) if b not in used] + SEQUENCES
    flattened = [b for sequence in cases for b in sequence]
    if len(ids) != len(set(ids)) or sorted(flattened) != sorted(ids):
        raise ValueError('Stage 3-B source coverage differs from the compiled mappings')

    directory = ROOT / '.generated/stage3b/source-checks'
    directory.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    def check(blocks: list[str]) -> dict:
        identity = '-'.join(blocks)
        code = '\n'.join(actual[b]['code'] for b in blocks)
        names = re.findall(r'^(?:noncomputable )?(?:def|theorem|lemma) (\w+)', code, re.M)
        for name in names:
            if '#print axioms ' + name not in code:
                code += '\n#print axioms ' + name + '\n'
        path = directory / (identity + '.lean')
        path.write_text(code)
        output = run(['lake', 'env', 'lean', '-DwarningAsError=true', '-DautoImplicit=false',
                      str(path.relative_to(ROOT))], 'source-stage3b-' + identity + '.log')
        if re.search(DIAGNOSTIC_PATTERN, output) or 'sorryAx' in output:
            raise ValueError(f'{identity}: unexpected diagnostic or unfinished proof')
        axioms = parse_axioms(output, names)
        print(identity + ': passed', flush=True)
        return dict(blocks=blocks, status='passed', exit_code=0,
                    source_sha256={b: actual[b]['sha256'] for b in blocks},
                    audited_declarations=axioms)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(check, cases))
    result = dict(status='passed', stage='3-B', checked_at=datetime.now(timezone.utc).isoformat(),
                  toolchain=(ROOT / 'lean-toolchain').read_text().strip(),
                  method='Separate Lean processes for each example or explicit sequence; original imports; '
                         'warningAsError=true; autoImplicit=false; named declarations audited',
                  checks=results)
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'Passed: {len(results)} cases / {len(ids)} source blocks', flush=True)
    print('Result: .generated/stage3b-source-checks.json; logs: .generated/logs/', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        print(f'FAILED: {error}', file=sys.stderr)
        sys.exit(1)
