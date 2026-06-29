# MCA Question Presenter

Local instructor tool for presenting MCA practice questions over Zoom or another
screen-sharing app.

The presenter is intentionally separate from the WordPress plugin scaffold. It
uses the same CSV bank format, but it does not need WordPress, PHP, a database,
student accounts, or a web server.

## Run From Source

From the repository root:

```bash
python presenter/mca_question_presenter.py
```

The app opens two windows:

- **Instructor controls**: load a bank, choose a topic, move through questions,
  reveal/hide answers, and reshuffle.
- **MCA Question Display**: the clean presentation window to share in Zoom.

Keyboard shortcuts:

- Right arrow: next question
- Left arrow: previous question
- Space or Enter: reveal/hide answer
- F11: toggle fullscreen on the display window
- Escape: leave fullscreen

## Question Bank Format

The presenter reads the same CSV columns used by the existing portal assets:

```text
portal,question_text,option_a,option_b,option_c,option_d,correct_option,topic_tag,is_active,sort_order
```

Required columns:

- `question_text`
- `option_a`
- `option_b`
- `option_c`
- `option_d`
- `correct_option`

Optional behavior:

- `is_active` values of `0`, `false`, `no`, `inactive`, or blank are skipped.
- `topic_tag` becomes the topic filter.
- `sort_order` is used for stable loading before the deck is shuffled.

## Windows Build

Install PyInstaller in a clean virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pyinstaller
```

Then run:

```powershell
presenter\build_windows.bat
```

The output will be under:

```text
dist\MCA Question Presenter\
```

Run:

```text
dist\MCA Question Presenter\MCA Question Presenter.exe
```

The build bundles the CSV files from `samples/` so the instructor can launch the
app without browsing for a bank first.

## Scope

Version 1 is a live teaching aid, not an exam system:

- no student login
- no online hosting
- no saved student results
- no pass/fail scoring
- no payment or course access control
- no WordPress dependency
