"""Regression checks for evidence that must never be accepted as success."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import catalog
from verify import parse_axioms


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


if __name__ == '__main__':
    unittest.main()
