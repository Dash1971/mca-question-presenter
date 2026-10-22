# MCA OOW Exam Presenter

An offline practice presenter for OOW Unlimited, with the **Navigator** interface and two expandable subject sections:

| Subject | Papers | Questions |
| --- | --- | --- |
| Navigation (034-83) | Paper 1–4 | 35 per paper |
| Stability & Operations (034-84) | Paper 1–3 | 35 per paper |
| Stability & Operations (034-84) | Paper 4 | 34 |

There are **eight papers and 279 questions** in total. All papers appear under their subject, without origin labels. The five additional papers contain 175 original questions based on the [June 2024 MCA syllabi](https://www.gov.uk/government/publications/mca-deck-safety-examination-syllabuses), with references and answer rationales maintained separately for content review. These are unofficial practice papers, not official MCA examination papers. Each question counts as one practice mark; the scoring is not an assertion of the official examination’s weighting or pass rules.

## Using the presenter

On Windows, extract the ZIP, keep the `MCA Visual Practice` folder together, and run **MCA Visual Practice.exe** inside it. It opens the presenter in your default browser without a server or internet connection. With the web edition, extract the entire folder and open **index.html**. From this repository, open `presenter/web/index.html` or run `python presenter/mca_question_presenter.py`.

1. Expand **Navigation** or **Stability & Operations**, then start or resume a paper.
2. Answer in any order using the question navigator. Responses, your place and review flags save in this browser on this computer.
3. Use **Flag for review** to mark a question to revisit. Figure controls zoom in, zoom out and reset; diagram labels can be selected then placed, or dragged.
4. Choose **Check & submit** to inspect the answered, unanswered and flagged counts. Select a question to return to it, or **Keep working**.
5. Choose **Submit paper** to finish. Unanswered questions score zero. Multi-select, matching, multipart and placement questions are all-or-nothing. The result shows only the final percentage and number correct.
6. Submission locks the attempt. **New attempt** asks before clearing that paper’s saved answers and result; other papers remain intact.

Answers and individual correctness are withheld from the interface. This is client-side offline practice: a technical user can inspect the keys in the app files. There are no accounts, server records or cross-device sync. If browser storage is unavailable, the app tells you that progress is retained only in the current session.

## Build and verification

Windows with Python and PyInstaller: run `presenter\build_windows.bat` (output: `dist\MCA Visual Practice\`). The GitHub Actions workflow tests and builds a Windows ZIP on relevant pull requests and main-branch changes.

```sh
python3 -m unittest discover -s tests
python3 -m compileall presenter tools tests
node --test tests/test_core.cjs
```

Rebuild the five additional question sets with `python3 tools/build_additional_papers.py`. Rebuild their five original SVG figures with `python3 tools/build_training_figures.py` (optional development dependency: matplotlib). Neither operation requires private source documents. Figure assets are checked in and no plotting dependency is needed to run or package the presenter.

`tools/additional-paper-review.json` records all 175 new keys, rationales and public references. It is development material and is not included in the student web or Windows bundles. `docs/content-review.md` records topic coverage and review limits. The source-bank IDs are stable so saved responses from earlier releases remain associated with the same papers; the interface numbers questions consecutively.

The five additional papers received a separate AI accuracy review on 22 October 2026: all 175 stems and keys, 92 numeric answer fields in 72 questions, 19 further quantitative choices, and all five training figures. The review tightened three question wordings and corrected two syllabus tags. `python3 tools/audit_additional_papers.py` reproduces the arithmetic checks and per-question ledger. This is not independent human maritime examiner certification; the other 104 questions were outside that focused review. See `docs/content-review.md` for methods and limits.

`python3 tools/export_instructor_material.py OUTPUT_DIRECTORY` creates a searchable offline answer book, complete question-bank JSON and the data for CSV/workbook exports. Instructor material includes answer keys and must be distributed separately from the student app. Editing an exported file does not alter the app. Existing third-party examination wording and figures retain any applicable distribution restrictions. Private candidate PDFs and identifying details are not part of this repository or the student bundles.

For release documentation, `python3 tools/build_release_guides.py OUTPUT_DIRECTORY` requires the optional development dependency `reportlab`. `node tools/build_instructor_workbook.mjs OUTPUT_DIRECTORY` uses `@oai/artifact-tool` in the authoring environment to turn the exported JSON into the CSV and filtered XLSX. These authoring dependencies are not required by students or the Windows app build.
