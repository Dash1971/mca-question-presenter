# MCA OOW Exam Presenter

An offline, clickable practice presenter with **three exams**:

- Supplied operations mock: 35 questions from the provided paper; **34 scored**. Question 18 is unscored because its tidal graphic was absent from the PDF export.
- New exam 1 — Navigation: **35 original questions** based on the June 2024 MCA/SQA OOW Unlimited Navigation syllabus (034-83).
- New exam 2 — Stability & Operations: **35 original questions** based on the June 2024 MCA/SQA OOW Unlimited Stability and Operations syllabus (034-84).

The two new papers were written for this app; they are not official MCA papers or copies of the supplied candidate mock. They include original training figures, single-choice and select-all items. The source mock also includes fields, matching, and diagram placement. The attached formula sheets and syllabus PDFs are reference material, not bundled into the student app.

## Student use

On Windows, extract the ZIP, keep the `MCA Visual Practice` folder together, and run **MCA Visual Practice.exe** inside it. It opens the app in the default browser without internet. From source, open `presenter/web/index.html` or run `python presenter/mca_question_presenter.py`.

1. Choose an exam in the sidebar.
2. Answer questions in any order. Your selections save automatically in this browser on this computer.
3. Select **Submit exam for percentage**. Each scored question is worth one mark; a multiple-answer or multi-part item is correct only when the entire response is correct. Unanswered questions score zero. The final screen shows **only the percentage and number correct out of the scored total**—no solutions or per-question correctness.
4. The attempt is locked after submission. **Start a new attempt** erases that exam's saved answers and mark, after confirmation.

Figures can be zoomed. Diagram-placement answers can be dragged or placed by selecting a label and clicking the figure.

**Important:** This is an offline client-side practice app, not a secure examination system. Answer keys are withheld from the interface but necessarily exist in the local app files and can be inspected by a technically capable user. For tamper-resistant assessment, keep the key on a controlled server and use authenticated submission instead.

The supplied mock's figures and wording may have distribution restrictions; review rights before redistributing. The app does not bundle either candidate PDF, candidate names, marked responses, the syllabus PDFs, or the formula sheets.

## Build and checks

Windows with Python and PyInstaller: `presenter\build_windows.bat` (output: `dist\MCA Visual Practice\`). The local source paper is **not** required. The development-only `tools/import_mock.py` can regenerate the supplied mock's data and figures, and preserves the unscored-Q18 rule; review output before distribution.

```sh
python3 -m unittest discover -s tests
python3 -m compileall presenter tools tests
```
