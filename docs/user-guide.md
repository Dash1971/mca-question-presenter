# MCA Question Presenter User Guide

## Purpose

MCA Question Presenter is a local desktop tool for running live MCA practice
sessions. It is designed for an instructor who wants to screen-share questions,
move through a shuffled deck, and reveal the correct answer only when ready.

The app is intentionally simple: no login, no database, no web server, no
student grading, and no WordPress dependency.

## What Is Included

The app includes two bundled question banks:

| Bank | File | Use |
| --- | --- | --- |
| Navigation | `samples/oow-navigation-bank-150.csv` | Navigation, chartwork, lights, signals, rules, and related OOW practice |
| Stability | `samples/oow-stability-bank-150.csv` | Stability, loading, buoyancy, free surface, and related OOW practice |

The Navigation bank loads automatically when the app starts. Use **Load
Selected** to switch to the Stability bank.

## Install On Windows

Use the Windows build artifact provided by the instructor or course organizer.
The learner does not need Python, Git, GitHub login, or command-line setup.

1. Download the `MCA-Question-Presenter-Windows` zip file.
2. Right-click the zip file and choose **Extract All...**.
3. Open the extracted folder.
4. Double-click **MCA Question Presenter.exe**.

If Windows SmartScreen appears, choose **More info**, then **Run anyway** only
if the file came directly from the instructor or the official course channel.

## Start A Teaching Session

1. Launch the app by double-clicking **MCA Question Presenter.exe**.
2. Two windows open:
   - **Instructor controls**: private control panel for the instructor.
   - **MCA Question Display**: clean window to share with students.
3. In Zoom, Teams, or Google Meet, share only the **MCA Question Display**
   window.
4. Press **Next** to show the first question.
5. Discuss the question with students.
6. Press **Reveal / Hide** when ready to show the answer.
7. Press **Next** to continue.

## Instructor Controls

| Control | What It Does |
| --- | --- |
| **Load CSV...** | Open a custom CSV question bank from your computer |
| **Show Display** | Bring the presentation window back to the front |
| **Topic** | Filter the current bank by `topic_tag` |
| **Previous** | Return to the previous question |
| **Next** | Move to the next question |
| **Reveal / Hide** | Show or hide the correct answer |
| **Reshuffle** | Randomize the current topic or full bank again |
| **Load Selected** | Load one of the bundled banks |

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| Right arrow | Next question |
| Left arrow | Previous question |
| Space | Reveal or hide answer |
| Enter | Reveal or hide answer |
| F11 | Toggle fullscreen on the display window |
| Escape | Leave fullscreen |

## Recommended Screen-Share Setup

Use two windows:

- Keep **Instructor controls** on your own screen.
- Share **MCA Question Display** with students.

If the display window disappears behind other windows, click **Show Display**.
For a cleaner lesson view, press **F11** while the display window is active.

## Upload A Custom CSV

Use **Load CSV...** when you want to teach from your own question bank instead
of the bundled Navigation or Stability banks.

1. Prepare the question bank as a `.csv` file.
2. Save the file using UTF-8 encoding if your spreadsheet app offers an
   encoding choice.
3. Open **MCA Question Presenter.exe**.
4. Click **Load CSV...** in the **Instructor controls** window.
5. Select your CSV file.
6. The app loads the bank, shuffles the active questions, and shows the first
   question immediately.

If the file has `topic_tag` values, they appear in the **Topic** drop-down after
the CSV loads. Choose a topic to teach only that subset, or choose **All** to
use the full bank.

## Working With Question Banks

Question banks are CSV files. The required columns are:

```text
question_text,option_a,option_b,option_c,option_d,correct_option
```

Recommended full format:

```text
portal,question_text,option_a,option_b,option_c,option_d,correct_option,topic_tag,is_active,sort_order
```

Column details:

| Column | Required | What To Put In It |
| --- | --- | --- |
| `question_text` | Yes | The question shown to students |
| `option_a` | Yes | Answer choice A |
| `option_b` | Yes | Answer choice B |
| `option_c` | Yes | Answer choice C |
| `option_d` | Yes | Answer choice D |
| `correct_option` | Yes | The letter of the correct answer: `A`, `B`, `C`, or `D` |
| `portal` | No | A label for the bank or course, for example `oow` |
| `topic_tag` | No | Topic filter name, for example `colregs`, `chartwork`, or `stability` |
| `is_active` | No | Use `1` for active questions; use `0`, `false`, `no`, `inactive`, or blank to skip a row |
| `sort_order` | No | Number used for stable ordering before the app shuffles the session |

Example CSV:

```csv
portal,question_text,option_a,option_b,option_c,option_d,correct_option,topic_tag,is_active,sort_order
oow,"What does a vessel at anchor display by day?","One black ball","Two black balls","A black cylinder","A red cone","A","colregs",1,1
```

Rules:

- `correct_option` must be `A`, `B`, `C`, or `D`.
- `question_text` and all four answer options must not be blank.
- `topic_tag` controls the topic filter.
- `sort_order` controls the stable load order before shuffling.
- `is_active` values of `0`, `false`, `no`, `inactive`, or blank are skipped.
- Extra columns are allowed, but the app ignores them.
- If a question or answer contains a comma, keep the value inside double quotes.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Windows blocks the app on first launch | Choose **More info** then **Run anyway**, but only for the instructor-provided build |
| Nothing happens after double-clicking | Extract the zip first, then run **MCA Question Presenter.exe** from the extracted folder |
| The selected bank has no questions | Check that `is_active` is not blank, `0`, `false`, `no`, or `inactive` |
| A CSV will not load | Confirm all required columns exist, every row has A-D options, and `correct_option` contains only A, B, C, or D |
| Topics do not appear | Add values to the optional `topic_tag` column, then reload the CSV |
| The wrong answer is highlighted | Check the row's `correct_option` value |
| Students can see the controls | Share only the **MCA Question Display** window |

## Scope

This app is for live teaching and practice. It does not record student answers,
calculate scores, manage course access, or run online exams.
