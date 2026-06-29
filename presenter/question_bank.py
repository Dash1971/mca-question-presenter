from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = {
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_option",
}


@dataclass(frozen=True)
class Question:
    question_text: str
    options: dict[str, str]
    correct_option: str
    topic_tag: str = ""
    sort_order: int = 0

    @property
    def correct_answer_text(self) -> str:
        return self.options[self.correct_option]


def parse_bool(value: str) -> bool:
    return value.strip().lower() not in {"0", "false", "no", "inactive", ""}


def parse_sort_order(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def load_questions(path: Path) -> list[Question]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise ValueError(f"CSV is missing required column(s): {missing_text}")

        questions: list[Question] = []
        for row_number, row in enumerate(reader, start=2):
            if "is_active" in row and not parse_bool(row.get("is_active", "")):
                continue

            correct = (row.get("correct_option") or "").strip().upper()
            if correct not in {"A", "B", "C", "D"}:
                raise ValueError(f"Row {row_number} has invalid correct_option: {correct!r}")

            options = {
                "A": (row.get("option_a") or "").strip(),
                "B": (row.get("option_b") or "").strip(),
                "C": (row.get("option_c") or "").strip(),
                "D": (row.get("option_d") or "").strip(),
            }
            if not (row.get("question_text") or "").strip():
                raise ValueError(f"Row {row_number} has an empty question_text")
            if any(not value for value in options.values()):
                raise ValueError(f"Row {row_number} has an empty answer option")

            questions.append(
                Question(
                    question_text=(row.get("question_text") or "").strip(),
                    options=options,
                    correct_option=correct,
                    topic_tag=(row.get("topic_tag") or "").strip(),
                    sort_order=parse_sort_order(row.get("sort_order", "")),
                )
            )

    questions.sort(key=lambda q: q.sort_order)
    return questions


class QuestionDeck:
    def __init__(self, questions: list[Question]) -> None:
        self.all_questions = questions
        self.topic = "All"
        self.questions: list[Question] = []
        self.index = -1
        self.reshuffle()

    def topics(self) -> list[str]:
        topic_names = sorted({q.topic_tag for q in self.all_questions if q.topic_tag})
        return ["All", *topic_names]

    def set_topic(self, topic: str) -> None:
        self.topic = topic
        self.reshuffle()

    def reshuffle(self) -> None:
        if self.topic == "All":
            self.questions = list(self.all_questions)
        else:
            self.questions = [q for q in self.all_questions if q.topic_tag == self.topic]
        random.shuffle(self.questions)
        self.index = -1

    def current(self) -> Question | None:
        if 0 <= self.index < len(self.questions):
            return self.questions[self.index]
        return None

    def next(self) -> Question | None:
        if self.index + 1 >= len(self.questions):
            return None
        self.index += 1
        return self.current()

    def previous(self) -> Question | None:
        if self.index <= 0:
            return None
        self.index -= 1
        return self.current()

    def progress_text(self) -> str:
        if not self.questions:
            return "0 / 0"
        if self.index < 0:
            return f"0 / {len(self.questions)}"
        return f"{self.index + 1} / {len(self.questions)}"
