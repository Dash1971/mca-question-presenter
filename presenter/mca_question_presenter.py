from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from tkinter import BOTH, BOTTOM, END, LEFT, RIGHT, TOP, X, Y
from tkinter import Button, Frame, Label, Listbox, StringVar, Tk, Toplevel, filedialog, messagebox
from tkinter import ttk

try:
    from .question_bank import Question, QuestionDeck, load_questions
except ImportError:
    from question_bank import Question, QuestionDeck, load_questions


APP_TITLE = "MCA Question Presenter"
DEFAULT_BANK = "samples/oow-bank-150.csv"


def resource_path(relative_path: str) -> Path:
    """Return a path that works from source and from a PyInstaller bundle."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / relative_path
    return Path(__file__).resolve().parents[1] / relative_path


def bundled_banks() -> list[Path]:
    samples = resource_path("samples")
    if not samples.exists():
        return []
    return sorted(samples.glob("*.csv"))


class PresenterWindow:
    def __init__(self, root: Tk) -> None:
        self.window = Toplevel(root)
        self.window.title("MCA Question Display")
        self.window.geometry("1200x760")
        self.window.minsize(900, 580)
        self.window.configure(bg="#f8fafc")
        self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)

        self.fullscreen = False
        self.revealed = False
        self.option_labels: dict[str, Label] = {}

        top = Frame(self.window, bg="#0f172a", padx=28, pady=14)
        top.pack(side=TOP, fill=X)

        self.title_label = Label(
            top,
            text="MCA Question Presenter",
            bg="#0f172a",
            fg="#ffffff",
            font=("Segoe UI", 24, "bold"),
            anchor="w",
        )
        self.title_label.pack(side=LEFT, fill=X, expand=True)

        self.progress_label = Label(
            top,
            text="0 / 0",
            bg="#0f172a",
            fg="#cbd5e1",
            font=("Segoe UI", 18),
            anchor="e",
        )
        self.progress_label.pack(side=RIGHT)

        body = Frame(self.window, bg="#f8fafc", padx=44, pady=34)
        body.pack(side=TOP, fill=BOTH, expand=True)

        self.topic_label = Label(
            body,
            text="",
            bg="#f8fafc",
            fg="#475569",
            font=("Segoe UI", 16, "bold"),
            anchor="w",
        )
        self.topic_label.pack(fill=X, pady=(0, 12))

        self.question_label = Label(
            body,
            text="Load a question bank, then press Next.",
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 30, "bold"),
            justify=LEFT,
            anchor="nw",
            wraplength=1080,
        )
        self.question_label.pack(fill=X, pady=(0, 26))

        options = Frame(body, bg="#f8fafc")
        options.pack(fill=BOTH, expand=True)
        for letter in ["A", "B", "C", "D"]:
            label = Label(
                options,
                text=f"{letter}.",
                bg="#ffffff",
                fg="#111827",
                activebackground="#ffffff",
                font=("Segoe UI", 24),
                justify=LEFT,
                anchor="w",
                wraplength=1040,
                padx=24,
                pady=16,
                relief="solid",
                bd=1,
            )
            label.pack(fill=X, pady=8)
            self.option_labels[letter] = label

        self.answer_label = Label(
            body,
            text="",
            bg="#f8fafc",
            fg="#14532d",
            font=("Segoe UI", 22, "bold"),
            justify=LEFT,
            anchor="w",
            wraplength=1080,
        )
        self.answer_label.pack(fill=X, pady=(16, 0))

        self.window.bind("<F11>", lambda _event: self.toggle_fullscreen())
        self.window.bind("<Escape>", lambda _event: self.set_fullscreen(False))

    def show_question(self, question: Question | None, progress: str) -> None:
        self.revealed = False
        self.progress_label.config(text=progress)
        self.answer_label.config(text="")

        if question is None:
            self.topic_label.config(text="")
            self.question_label.config(text="No question selected.")
            for letter, label in self.option_labels.items():
                label.config(text=f"{letter}.", bg="#ffffff", fg="#111827")
            return

        topic = question.topic_tag.replace("-", " ").title() if question.topic_tag else "General"
        self.topic_label.config(text=topic)
        self.question_label.config(text=textwrap.fill(question.question_text, width=78))
        for letter, label in self.option_labels.items():
            label.config(
                text=f"{letter}. {question.options[letter]}",
                bg="#ffffff",
                fg="#111827",
            )

    def reveal(self, question: Question | None) -> None:
        if question is None:
            return
        self.revealed = True
        for letter, label in self.option_labels.items():
            if letter == question.correct_option:
                label.config(bg="#bbf7d0", fg="#052e16")
            else:
                label.config(bg="#ffffff", fg="#475569")
        self.answer_label.config(
            text=f"Correct answer: {question.correct_option}. {question.correct_answer_text}"
        )

    def hide_answer(self, question: Question | None) -> None:
        if question is None:
            return
        self.revealed = False
        self.answer_label.config(text="")
        for label in self.option_labels.values():
            label.config(bg="#ffffff", fg="#111827")

    def toggle_fullscreen(self) -> None:
        self.set_fullscreen(not self.fullscreen)

    def set_fullscreen(self, enabled: bool) -> None:
        self.fullscreen = enabled
        self.window.attributes("-fullscreen", self.fullscreen)


class InstructorApp:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("560x620")
        self.root.minsize(500, 560)

        self.deck: QuestionDeck | None = None
        self.current_bank: Path | None = None
        self.presenter = PresenterWindow(self.root)

        self.bank_var = StringVar(value="")
        self.topic_var = StringVar(value="All")
        self.status_var = StringVar(value="Load a question bank to begin.")

        self.build_controls()
        self.bind_shortcuts()
        self.load_default_bank()

    def build_controls(self) -> None:
        outer = Frame(self.root, padx=18, pady=18)
        outer.pack(fill=BOTH, expand=True)

        Label(outer, text=APP_TITLE, font=("Segoe UI", 20, "bold"), anchor="w").pack(fill=X)
        Label(
            outer,
            text="Instructor controls. Share the separate presentation window in Zoom.",
            font=("Segoe UI", 10),
            anchor="w",
            fg="#475569",
        ).pack(fill=X, pady=(2, 16))

        bank_frame = ttk.LabelFrame(outer, text="Question bank")
        bank_frame.pack(fill=X, pady=(0, 12))
        self.bank_label = Label(bank_frame, textvariable=self.bank_var, anchor="w", padx=8, pady=6)
        self.bank_label.pack(fill=X)
        Button(bank_frame, text="Load CSV...", command=self.choose_bank).pack(side=LEFT, padx=8, pady=(0, 8))
        Button(bank_frame, text="Show Display", command=self.show_display).pack(side=LEFT, padx=8, pady=(0, 8))

        filters = ttk.LabelFrame(outer, text="Session")
        filters.pack(fill=X, pady=(0, 12))
        Label(filters, text="Topic:", anchor="w").pack(side=LEFT, padx=(8, 4), pady=8)
        self.topic_combo = ttk.Combobox(filters, textvariable=self.topic_var, values=["All"], state="readonly")
        self.topic_combo.pack(side=LEFT, fill=X, expand=True, padx=(0, 8), pady=8)
        self.topic_combo.bind("<<ComboboxSelected>>", lambda _event: self.change_topic())

        actions = ttk.LabelFrame(outer, text="Controls")
        actions.pack(fill=X, pady=(0, 12))
        Button(actions, text="Previous", command=self.previous_question, width=12).pack(side=LEFT, padx=8, pady=10)
        Button(actions, text="Next", command=self.next_question, width=12).pack(side=LEFT, padx=8, pady=10)
        Button(actions, text="Reveal / Hide", command=self.toggle_reveal, width=14).pack(side=LEFT, padx=8, pady=10)
        Button(actions, text="Reshuffle", command=self.reshuffle, width=12).pack(side=LEFT, padx=8, pady=10)

        shortcuts = ttk.LabelFrame(outer, text="Keyboard")
        shortcuts.pack(fill=X, pady=(0, 12))
        shortcut_text = "Right arrow: next    Left arrow: previous    Space/Enter: reveal/hide    F11: fullscreen display"
        Label(shortcuts, text=shortcut_text, justify=LEFT, wraplength=500, padx=8, pady=8).pack(fill=X)

        banks = ttk.LabelFrame(outer, text="Bundled banks")
        banks.pack(fill=BOTH, expand=True, pady=(0, 12))
        self.bank_list = Listbox(banks, height=6)
        self.bank_list.pack(side=LEFT, fill=BOTH, expand=True, padx=(8, 0), pady=8)
        Button(banks, text="Load Selected", command=self.load_selected_bank).pack(side=RIGHT, fill=Y, padx=8, pady=8)
        self.refresh_bank_list()

        Label(outer, textvariable=self.status_var, anchor="w", fg="#334155", wraplength=520).pack(
            side=BOTTOM, fill=X
        )

    def bind_shortcuts(self) -> None:
        for window in [self.root, self.presenter.window]:
            window.bind("<Right>", lambda _event: self.next_question())
            window.bind("<Left>", lambda _event: self.previous_question())
            window.bind("<space>", lambda _event: self.toggle_reveal())
            window.bind("<Return>", lambda _event: self.toggle_reveal())

    def refresh_bank_list(self) -> None:
        self.bank_list.delete(0, END)
        for path in bundled_banks():
            self.bank_list.insert(END, path.name)

    def load_default_bank(self) -> None:
        default = resource_path(DEFAULT_BANK)
        if not default.exists():
            fallback_banks = bundled_banks()
            if not fallback_banks:
                return
            default = fallback_banks[0]
        self.load_bank(default)

    def load_selected_bank(self) -> None:
        selection = self.bank_list.curselection()
        if not selection:
            return
        name = self.bank_list.get(selection[0])
        for path in bundled_banks():
            if path.name == name:
                self.load_bank(path)
                return

    def choose_bank(self) -> None:
        filename = filedialog.askopenfilename(
            title="Choose question bank CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if filename:
            self.load_bank(Path(filename))

    def load_bank(self, path: Path) -> None:
        try:
            questions = load_questions(path)
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Could not load question bank:\n\n{exc}")
            return

        if not questions:
            messagebox.showwarning(APP_TITLE, "The selected bank has no active questions.")
            return

        self.current_bank = path
        self.deck = QuestionDeck(questions)
        self.bank_var.set(path.name)
        self.topic_combo.config(values=self.deck.topics())
        self.topic_var.set("All")
        self.status_var.set(f"Loaded {len(questions)} active questions from {path.name}.")
        self.presenter.show_question(None, self.deck.progress_text())

    def change_topic(self) -> None:
        if not self.deck:
            return
        self.deck.set_topic(self.topic_var.get())
        self.status_var.set(f"Topic: {self.topic_var.get()} - {len(self.deck.questions)} questions ready.")
        self.presenter.show_question(None, self.deck.progress_text())

    def next_question(self) -> None:
        if not self.deck:
            return
        question = self.deck.next()
        if question is None:
            messagebox.showinfo(APP_TITLE, "That deck is complete. Reshuffle to start again.")
            return
        self.presenter.show_question(question, self.deck.progress_text())
        self.show_display()

    def previous_question(self) -> None:
        if not self.deck:
            return
        question = self.deck.previous()
        if question is None:
            return
        self.presenter.show_question(question, self.deck.progress_text())
        self.show_display()

    def toggle_reveal(self) -> None:
        if not self.deck:
            return
        question = self.deck.current()
        if self.presenter.revealed:
            self.presenter.hide_answer(question)
        else:
            self.presenter.reveal(question)
        self.show_display()

    def reshuffle(self) -> None:
        if not self.deck:
            return
        self.deck.reshuffle()
        self.presenter.show_question(None, self.deck.progress_text())
        self.status_var.set(f"Reshuffled {len(self.deck.questions)} questions.")

    def show_display(self) -> None:
        self.presenter.window.deiconify()
        self.presenter.window.lift()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    InstructorApp().run()


if __name__ == "__main__":
    main()
