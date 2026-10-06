from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'presenter' / 'web'


class PracticePaperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = (WEB / 'paper.js').read_text(encoding='utf-8')
        cls.raw = data
        cls.questions = json.loads(data.removeprefix('window.PAPER=').rstrip(' ;\n'))

    def test_all_questions_and_figures_present(self):
        self.assertEqual([q['id'] for q in self.questions], list(range(1, 36)))
        for q in self.questions:
            self.assertTrue(q['prompt'])
            if 'image' in q:
                self.assertTrue((WEB / q['image']).is_file(), q['id'])
        self.assertEqual(len({q['image'] for q in self.questions if 'image' in q}), 15)

    def test_keys_and_ungraded_items_are_explicit(self):
        for q in self.questions:
            if q['kind'] in ('single', 'multi'):
                self.assertGreaterEqual(len(q['options']), 3, q['id'])
                for i in q.get('answer', []):
                    self.assertLess(i, len(q['options']), q['id'])
            if q['id'] in (13, 18, 34):
                self.assertTrue(q['note'])
                self.assertNotIn('answer', q)

    def test_private_result_data_and_csv_are_absent(self):
        self.assertNotRegex(self.raw, re.compile(r'Candidate|Created by|Partially Correct', re.I))
        self.assertFalse(list(ROOT.glob('samples/*.csv')))
        self.assertFalse((ROOT / 'presenter' / 'question_bank.py').exists())

    def test_windows_build_contains_web_assets(self):
        script = (ROOT / 'presenter' / 'build_windows.bat').read_text()
        self.assertIn('presenter\\web;presenter\\web', script)
        self.assertIn('--onedir', script)
        self.assertNotIn('samples', script)


if __name__ == '__main__':
    unittest.main()
