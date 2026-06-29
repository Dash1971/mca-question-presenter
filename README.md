# MCA Question Presenter

Lightweight desktop presenter for MCA practice questions, designed for
instructors to screen-share randomized questions and reveal answers during live
lessons.

This is a local teaching tool, not an online exam portal. It does not require
WordPress, PHP, accounts, a database, or a web server.

## What It Does

- loads MCA question banks from CSV
- shuffles active questions for each session
- displays one multiple-choice question at a time
- hides the correct answer until the instructor reveals it
- highlights the correct answer on reveal
- filters questions by `topic_tag`
- uses a separate presentation window for Zoom or other screen-sharing apps

## Run From Source

Windows:

```powershell
py presenter\mca_question_presenter.py
```

Linux:

```bash
sudo apt install python3-tk
python3 presenter/mca_question_presenter.py
```

The app opens two windows:

- **Instructor controls**: load a bank, choose a topic, move through questions,
  reveal/hide answers, and reshuffle.
- **MCA Question Display**: the clean presentation window to share in Zoom.

## Keyboard Shortcuts

- Right arrow: next question
- Left arrow: previous question
- Space or Enter: reveal/hide answer
- F11: toggle fullscreen on the display window
- Escape: leave fullscreen

## Included Banks

The `samples/` folder contains two bundled practice banks:

- `oow-navigation-bank-150.csv`
- `oow-stability-bank-150.csv`

The app loads the Navigation bank by default. Use **Load Selected** in the
instructor controls to switch to the Stability bank.

## User Guide

A full instructor guide is available in [`docs/user-guide.md`](docs/user-guide.md).
A shareable PDF version is available in
[`docs/mca-question-presenter-user-guide.pdf`](docs/mca-question-presenter-user-guide.pdf).

## CSV Format

Required columns:

```text
question_text,option_a,option_b,option_c,option_d,correct_option
```

Recommended full format:

```text
portal,question_text,option_a,option_b,option_c,option_d,correct_option,topic_tag,is_active,sort_order
```

`correct_option` must be `A`, `B`, `C`, or `D`.

`is_active` values of `0`, `false`, `no`, `inactive`, or blank are skipped.

## Windows Build

For normal end-user delivery, use the GitHub Actions build instead of asking the
instructor to run commands.

### GitHub Actions Build

1. Open the repository on GitHub.
2. Go to **Actions**.
3. Open **Build Windows App**.
4. Run the workflow manually, or use the latest successful run from `main`.
5. Download the `MCA-Question-Presenter-Windows` artifact.
6. Send the downloaded zip to the instructor.

The instructor only needs to unzip the folder and double-click:

```text
MCA Question Presenter.exe
```

### Manual Windows Build

Install PyInstaller in a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pyinstaller
```

Build:

```powershell
presenter\build_windows.bat
```

Run:

```text
dist\MCA Question Presenter\MCA Question Presenter.exe
```

## Tests

```bash
python3 -m unittest discover -s tests
python3 -m compileall presenter tests
```
