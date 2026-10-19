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
        cls.papers = json.loads((WEB / 'papers.js').read_text(encoding='utf-8').removeprefix('window.NEW_PAPERS=').rstrip(' ;\n'))

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


    def test_new_papers_cover_both_syllabi(self):
        self.assertEqual([p['id'] for p in self.papers], ['mock', 'navigation-1', 'stability-1'])
        self.assertIsNone(self.papers[0]['questions'])
        for p, prefix in zip(self.papers[1:], ('034-83', '034-84')):
            questions = p['questions']
            self.assertEqual(len(questions), 35)
            self.assertEqual([q['id'] for q in questions], list(range(1, 36)))
            for q in questions:
                self.assertTrue(q['syllabus'].startswith(prefix))
                if q['kind'] in ('single', 'multi'):
                    self.assertGreaterEqual(len(q['options']), 4)
                    self.assertTrue(q['answer'])
                    self.assertTrue(all(0 <= i < len(q['options']) for i in q['answer']))
                elif q['kind'] == 'match':
                    self.assertEqual(len(q['terms']), len(q['answers']))
                    self.assertTrue(all(0 <= i < len(q['definitions']) for i in q['answers']))
                elif q['kind'] == 'place':
                    self.assertEqual(set(q['tokens']), set(q['targets']))
                else:
                    self.fail(q['kind'])
                if 'image' in q:
                    self.assertTrue((WEB / q['image']).is_file())

    def test_exam_interface_withholds_answer_feedback(self):
        app = (WEB / 'app.js').read_text(encoding='utf-8')
        html = (WEB / 'index.html').read_text(encoding='utf-8')
        self.assertIn('Submit exam for percentage', html)
        self.assertIn('Final mark:', app)
        self.assertNotIn('Check answer', html)
        self.assertNotIn('Answer: ${', app)
        self.assertNotIn('drawTargets', app)
        self.assertFalse(self.questions[17]['scored'])

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
