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

## Working With Question Banks

Question banks are CSV files. The required columns are:

```text
question_text,option_a,option_b,option_c,option_d,correct_option
```

Recommended full format:

```text
portal,question_text,option_a,option_b,option_c,option_d,correct_option,topic_tag,is_active,sort_order
```

Rules:

- `correct_option` must be `A`, `B`, `C`, or `D`.
- `topic_tag` controls the topic filter.
- `sort_order` controls the stable load order before shuffling.
- `is_active` values of `0`, `false`, `no`, `inactive`, or blank are skipped.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Windows blocks the app on first launch | Choose **More info** then **Run anyway**, but only for the instructor-provided build |
| Nothing happens after double-clicking | Extract the zip first, then run **MCA Question Presenter.exe** from the extracted folder |
| The selected bank has no questions | Check that `is_active` is not blank, `0`, `false`, `no`, or `inactive` |
| A CSV will not load | Confirm all required columns exist and every row has A-D options |
| The wrong answer is highlighted | Check the row's `correct_option` value |
| Students can see the controls | Share only the **MCA Question Display** window |

## Scope

This app is for live teaching and practice. It does not record student answers,
calculate scores, manage course access, or run online exams.
