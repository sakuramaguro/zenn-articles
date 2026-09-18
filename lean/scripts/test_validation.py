"""Regression checks for evidence that must never be accepted as success."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import catalog
from verify import parse_axioms, validate_diagnostic_output
from verify_all import check_coverage


class CatalogChecks(unittest.TestCase):
    def setUp(self):
        self.data = catalog.load_catalog()

    def test_missing_block_is_rejected(self):
        self.data['blocks'].pop()
        with self.assertRaisesRegex(ValueError, 'coverage mismatch'):
            catalog.validate(self.data)

    def test_duplicate_block_is_rejected(self):
        self.data['blocks'].append(copy.deepcopy(self.data['blocks'][0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate block'):
            catalog.validate(self.data)

    def test_changed_source_is_rejected(self):
        key = next(iter(self.data['source_files']))
        self.data['source_files'][key] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Manuscript file set or content changed'):
            catalog.validate(self.data)

    def test_changed_code_is_rejected(self):
        self.data['blocks'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'stale sha256'):
            catalog.validate(self.data)

    def test_missing_context_is_rejected(self):
        row = next(b for b in self.data['blocks'] if b['category'] == 'fragment')
        row['context']['blocks'] = ['missing_001']
        with self.assertRaisesRegex(ValueError, 'dangling context'):
            catalog.validate(self.data)

    def test_missing_diagnostic_source_is_rejected(self):
        self.data['diagnostics'][0]['blocks'] = ['missing_001']
        with self.assertRaisesRegex(ValueError, 'dangling diagnostic source'):
            catalog.validate(self.data)


class ChapterFiles(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / 'chapters').mkdir()
        self.index = {'schema_version': 2, 'block_files': ['chapters/ch01.json']}
        self.row = {'id': 'ch01_001', 'source': 'books/lean4-formalization/ch01.md'}
        (self.root / 'chapters/ch01.json').write_text(json.dumps([self.row]))

    def load(self):
        path = self.root / 'index.json'
        path.write_text(json.dumps(self.index))
        return catalog.load_catalog(path)

    def test_chapter_rows_are_loaded(self):
        self.assertEqual(self.load()['blocks'], [self.row])

    def test_missing_chapter_file_is_rejected(self):
        (self.root / 'chapters/ch01.json').unlink()
        with self.assertRaisesRegex(ValueError, 'file set mismatch'):
            self.load()

    def test_unlisted_chapter_file_is_rejected(self):
        (self.root / 'chapters/ch02.json').write_text('[]')
        with self.assertRaisesRegex(ValueError, 'file set mismatch'):
            self.load()

    def test_duplicate_chapter_path_is_rejected(self):
        self.index['block_files'] *= 2
        with self.assertRaisesRegex(ValueError, 'Duplicate chapter'):
            self.load()

    def test_wrong_chapter_is_rejected(self):
        self.row['source'] = 'books/lean4-formalization/ch02.md'
        (self.root / 'chapters/ch01.json').write_text(json.dumps([self.row]))
        with self.assertRaisesRegex(ValueError, 'wrong chapter'):
            self.load()

    def test_path_outside_chapter_directory_is_rejected(self):
        self.index['block_files'] = ['../ch01.json']
        with self.assertRaisesRegex(ValueError, 'Invalid chapter catalog path'):
            self.load()


class AxiomChecks(unittest.TestCase):
    def test_standard_and_empty_dependencies_are_accepted(self):
        output = "'a' depends on axioms: [propext, Classical.choice, Quot.sound]\n'b' does not depend on any axioms\n"
        self.assertEqual(parse_axioms(output, ['a', 'b'])['b'], [])

    def test_sorry_or_unreviewed_axioms_are_rejected(self):
        for axiom in ('sorryAx', 'inventedAxiom'):
            with self.subTest(axiom=axiom), self.assertRaisesRegex(ValueError, 'unreviewed axioms'):
                parse_axioms(f"'a' depends on axioms: [{axiom}]", ['a'])

    def test_missing_audit_output_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'coverage mismatch'):
            parse_axioms("'a' does not depend on any axioms", ['a', 'b'])


class DiagnosticChecks(unittest.TestCase):
    def test_coded_error_reason_is_checked(self):
        case = {'id': 'missing_name', 'kind': 'error', 'error_count': 1,
                'patterns': ['Unknown constant `Nat.add_comm_wrong`']}
        result = validate_diagnostic_output(
            case, 'error(lean.unknownIdentifier): Unknown constant `Nat.add_comm_wrong`')
        self.assertEqual(result['errors'], 1)

    def test_extra_coded_error_is_rejected(self):
        case = {'id': 'bad_proof', 'kind': 'error', 'error_count': 1, 'patterns': ['unsolved goals']}
        with self.assertRaisesRegex(ValueError, 'expected error reason differs'):
            validate_diagnostic_output(
                case, 'error: unsolved goals\nerror(lean.unknownIdentifier): Unknown constant `x`')

    def test_completed_proof_rejects_coded_diagnostics(self):
        case = {'id': 'completed', 'kind': 'pass', 'declaration': 'a'}
        for severity in ('error', 'warning'):
            with self.subTest(severity=severity), self.assertRaisesRegex(ValueError, 'unexpected diagnostic'):
                validate_diagnostic_output(
                    case, f"{severity}(lean.synthInstanceFailed): failed to synthesize\n"
                    "'a' does not depend on any axioms")

    def test_sorry_lesson_rejects_additional_coded_error(self):
        case = {'id': 'lesson', 'kind': 'sorry', 'declaration': 'a'}
        with self.assertRaisesRegex(ValueError, 'expected sorry warning/axioms differ'):
            validate_diagnostic_output(
                case, "warning: declaration uses `sorry`\n'a' depends on axioms: [sorryAx]\n"
                'error(lean.synthInstanceFailed): failed to synthesize')

    def test_unrelated_failure_is_rejected(self):
        case = {'id': 'bad_proof', 'kind': 'error', 'error_count': 1, 'patterns': ['unsolved goals']}
        with self.assertRaisesRegex(ValueError, 'expected error reason differs'):
            validate_diagnostic_output(case, 'error: unknown module Mathlib')

    def test_additional_error_is_rejected(self):
        case = {'id': 'bad_proof', 'kind': 'error', 'error_count': 1, 'patterns': ['unsolved goals']}
        with self.assertRaisesRegex(ValueError, 'expected error reason differs'):
            validate_diagnostic_output(case, 'error: unsolved goals\nerror: unknown identifier')

    def test_sorry_lesson_requires_both_warning_and_axiom(self):
        case = {'id': 'lesson', 'kind': 'sorry', 'declaration': 'a'}
        for output in ["'a' depends on axioms: [sorryAx]", "warning: declaration uses `sorry`\n'a' depends on axioms: [propext]"]:
            with self.subTest(output=output), self.assertRaisesRegex(ValueError, 'expected sorry warning/axioms differ'):
                validate_diagnostic_output(case, output)

    def test_sorry_lesson_cannot_pass_as_completed_proof(self):
        case = {'id': 'lesson', 'kind': 'pass', 'declaration': 'a'}
        with self.assertRaisesRegex(ValueError, 'unexpected diagnostic'):
            validate_diagnostic_output(case, "warning: declaration uses `sorry`\n'a' depends on axioms: [sorryAx]")


class FullCoverageChecks(unittest.TestCase):
    def setUp(self):
        self.data = {
            'blocks': [{'id': 'c', 'category': 'complete'}, {'id': 'f', 'category': 'fragment'},
                       {'id': 'e', 'category': 'expected_error'}, {'id': 's', 'category': 'unfinished'}],
            'diagnostics': [{'id': 'error', 'kind': 'error', 'blocks': ['e']},
                            {'id': 'hole', 'kind': 'sorry', 'blocks': ['s']}],
        }
        self.actual = {b: {'sha256': b * 64} for b in 'cfes'}
        self.build = dict(status='passed', toolchain='pinned', compiled_source_blocks=['c', 'f'],
                          diagnostics={c['id']: dict(c, expected_reason_confirmed=True,
                                                     expected_warning_confirmed=True)
                                       for c in self.data['diagnostics']})
        self.reports = [dict(status='passed', toolchain='pinned', checks=[
            dict(status='passed', exit_code=0, blocks=['c', 'f'], setup=[],
                 source_sha256={b: b * 64 for b in 'cf'})])]

    def check(self):
        return check_coverage(self.data, self.actual, self.build, self.reports)

    def test_complete_evidence_is_accepted(self):
        self.assertEqual(self.check()['completed_blocks'], 2)

    def test_missing_isolated_target_is_rejected(self):
        self.reports[0]['checks'][0]['blocks'] = ['c']
        del self.reports[0]['checks'][0]['source_sha256']['f']
        with self.assertRaisesRegex(ValueError, 'Isolated source coverage'):
            self.check()

    def test_stale_isolated_source_is_rejected(self):
        self.reports[0]['checks'][0]['source_sha256']['c'] = 'old'
        with self.assertRaisesRegex(ValueError, 'Stale isolated source'):
            self.check()

    def test_failed_isolated_result_is_rejected(self):
        self.reports[0]['checks'][0]['exit_code'] = 1
        with self.assertRaisesRegex(ValueError, 'Unsuccessful isolated case'):
            self.check()

    def test_missing_diagnostic_is_rejected(self):
        del self.build['diagnostics']['hole']
        with self.assertRaisesRegex(ValueError, 'Diagnostic case coverage'):
            self.check()

    def test_unconfirmed_error_reason_is_rejected(self):
        self.build['diagnostics']['error']['expected_reason_confirmed'] = False
        with self.assertRaisesRegex(ValueError, 'Expected error reason'):
            self.check()

    def test_different_toolchain_is_rejected(self):
        self.reports[0]['toolchain'] = 'different'
        with self.assertRaisesRegex(ValueError, 'different toolchain'):
            self.check()


if __name__ == '__main__':
    unittest.main()
