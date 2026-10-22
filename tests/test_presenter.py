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
        self.assertEqual([q['id'] for q in self.questions], [i for i in range(1, 36) if i != 18])
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
        self.assertNotIn(18, [q['id'] for q in self.questions])
        self.assertEqual(self.questions[2]['answers'], ['Moves vertically upwards', 'Reduces', 'No list'])
        self.assertEqual(self.questions[4]['answers'], ['Moves downwards and to port', 'Increases', 'To starboard, reducing'])
        self.assertEqual(self.questions[12]['answer'], [0, 2, 5])
        self.assertEqual(self.questions[32]['answer'], [1, 7])


    def test_new_papers_cover_both_syllabi(self):
        self.assertEqual(len(self.papers), 8)
        self.assertEqual(len({p['id'] for p in self.papers}), 8)
        for subject in ('navigation', 'stability'):
            group = [p for p in self.papers if p['subject'] == subject]
            self.assertEqual([p['number'] for p in group], [1, 2, 3, 4])
            self.assertEqual([p['title'] for p in group], [f'Paper {n}' for n in range(1, 5)])
        self.assertIsNone(next(p for p in self.papers if p['id'] == 'mock')['questions'])
        for p in (p for p in self.papers if p['id'] != 'mock'):
            prefix = '034-83' if p['subject'] == 'navigation' else '034-84'
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
                elif q['kind'] == 'fields':
                    self.assertTrue(q['fields'])
                    for field in q['fields']:
                        self.assertTrue(field['label'])
                        self.assertIsNotNone(field['answer'])
                        self.assertGreaterEqual(field.get('tolerance', 0), 0)
                else:
                    self.fail(q['kind'])
                if 'image' in q:
                    self.assertTrue((WEB / q['image']).is_file())

    def test_exam_interface_withholds_answer_feedback(self):
        app = (WEB / 'app.js').read_text(encoding='utf-8')
        html = (WEB / 'index.html').read_text(encoding='utf-8')
        self.assertIn('Check &amp; submit', html)
        self.assertIn('Final mark', app)
        self.assertNotIn('Check answer', html)
        self.assertNotIn('Answer: ${', app)
        self.assertNotIn('drawTargets', app)
        self.assertNotIn('Grimsby tidal crossing', (WEB / 'paper.js').read_text())

    def test_additional_papers_have_review_records_and_complete_topic_coverage(self):
        review = json.loads((ROOT / 'tools' / 'additional-paper-review.json').read_text())
        self.assertEqual(len(review['papers']), 5)
        self.assertEqual(sum(len(p['questions']) for p in review['papers']), 175)
        stems = []
        for p in review['papers']:
            sections = set()
            for q in p['questions']:
                self.assertTrue(q['rationale'].strip())
                self.assertTrue(q['sources'])
                self.assertNotRegex(q['prompt'], r'\d, \d{3}', 'Thousands separators must stay intact.')
                self.assertTrue(all(key in review['references'] for key in q['sources']))
                sections.add(int(q['syllabus'].split()[1][0]))
                stems.append(q['prompt'])
            self.assertEqual(sections, set(range(1, 10 if p['subject'] == 'navigation' else 7)))
        self.assertEqual(len(stems), len(set(stems)))
        app_data = (WEB / 'papers.js').read_text()
        self.assertNotIn('rationale', app_data)
        self.assertNotIn('Supplied', app_data)
        self.assertNotIn('New exam', app_data)

    def test_independent_calculation_spot_checks(self):
        import math
        papers = {p['id']: p for p in self.papers}
        def values(paper_id, question_id):
            return [float(f['answer']) for f in papers[paper_id]['questions'][question_id-1]['fields']]
        self.assertEqual(values('navigation-2', 10), [round(math.degrees(math.atan2(2, 10)), 1), round(math.hypot(10, 2), 1)])
        self.assertEqual(values('navigation-2', 11), [round(90 + math.degrees(math.asin(5/13)), 1), 12])
        self.assertEqual(values('navigation-2', 13), [137 - (5-2)])
        self.assertEqual(values('navigation-2', 20), [53.1, 72 / .6])
        self.assertEqual(values('navigation-2', 33), [round(1 + (5-1)*.20, 1)])
        self.assertEqual(values('stability-2', 8), [round((8+.12-7.8)*100*18)])
        self.assertEqual(values('stability-2', 13), [round((6000*5+800*12)/6800, 2)])
        self.assertEqual(values('stability-2', 24), [4.92, 5.32])
        self.assertEqual(values('stability-3', 23), [4.8 + .6*.4])
        self.assertEqual(values('stability-3', 25), [round(6-.1+.2, 2), round(6-.1-.2, 2)])

    def test_complete_additional_paper_accuracy_audit(self):
        import sys
        sys.path.insert(0, str(ROOT / 'tools'))
        from audit_additional_papers import audit
        result = audit()
        self.assertEqual(result['questions_reviewed'], 175)
        self.assertEqual(result['numeric_fields'], 92)
        self.assertEqual(result['quantitative_questions_including_graphs_and_choices'], 91)
        saved = json.loads((ROOT / 'tools/review-audit.json').read_text())
        self.assertEqual(saved, result, 'Regenerate the audit after changing the bank.')

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
