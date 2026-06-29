from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from presenter.question_bank import QuestionDeck, load_questions


CSV_TEXT = """portal,question_text,option_a,option_b,option_c,option_d,correct_option,topic_tag,is_active,sort_order
oow,Question one,A1,B1,C1,D1,B,colregs,1,2
oow,Question two,A2,B2,C2,D2,C,stability,1,1
oow,Inactive,A3,B3,C3,D3,A,colregs,0,3
"""


class PresenterLoaderTests(unittest.TestCase):
    def test_load_questions_filters_inactive_and_sorts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "questions.csv"
            path.write_text(CSV_TEXT, encoding="utf-8")

            questions = load_questions(path)

        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0].question_text, "Question two")
        self.assertEqual(questions[1].question_text, "Question one")
        self.assertEqual(questions[0].correct_answer_text, "C2")

    def test_deck_topic_filter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "questions.csv"
            path.write_text(CSV_TEXT, encoding="utf-8")
            questions = load_questions(path)

        deck = QuestionDeck(questions)
        deck.set_topic("colregs")

        self.assertEqual(len(deck.questions), 1)
        self.assertEqual(deck.questions[0].topic_tag, "colregs")


if __name__ == "__main__":
    unittest.main()
