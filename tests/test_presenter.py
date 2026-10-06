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

    def test_every_question_has_a_complete_key(self):
        for q in self.questions:
            if q['kind'] in ('single', 'multi'):
                self.assertGreaterEqual(len(q['options']), 3, q['id'])
                self.assertTrue(q['answer'], q['id'])
                for i in q['answer']:
                    self.assertLess(i, len(q['options']), q['id'])
            elif q['kind'] == 'fields':
                key = q.get('answers') or [f.get('answer') for f in q['fields']]
                self.assertEqual(len(key), len(q['fields']), q['id'])
                self.assertTrue(all(key), q['id'])
            elif q['kind'] == 'match':
                self.assertEqual(len(q['answers']), len(q['terms']), q['id'])
            elif q['kind'] == 'place':
                self.assertEqual(set(q['targets']), set(q['tokens']), q['id'])
                for rect in q['targets'].values():
                    x1, y1, x2, y2 = rect
                    self.assertTrue(0 <= x1 < x2 <= 100 and 0 <= y1 < y2 <= 100, q['id'])
            else:
                self.fail(f"Unsupported question kind: {q['id']}")
        self.assertEqual(self.questions[17]['answers'], ['earliest 05:20', 'latest 09:30'])
        self.assertTrue(self.questions[17]['warning'])
        self.assertEqual(self.questions[2]['answers'], ['Moves vertically upwards', 'Reduces', 'No list'])
        self.assertEqual(self.questions[4]['answers'], ['Moves downwards and to port', 'Increases', 'To starboard, reducing'])
        self.assertEqual(self.questions[12]['answer'], [0, 2, 5])
        self.assertEqual(self.questions[33]['answer'], [1, 7])

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
