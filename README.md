# MCA Question Presenter

MCA Question Presenter is a simple Windows app for showing multiple-choice MCA
practice questions during a lesson. It is designed for an instructor who is
sharing their screen in Zoom, Microsoft Teams, Google Meet, or a classroom.

No technical setup is needed. You do not need Python, Git, a database, or a web
server.

## Download The Windows App

1. Open the [Windows download page](https://github.com/Dash1971/mca-question-presenter/actions/workflows/build-windows.yml).
2. Click the most recent **Build Windows App** entry with a green tick.
3. Scroll down to **Artifacts** at the bottom of the page.
4. Click **MCA-Question-Presenter-Windows** to download it.

GitHub may ask you to sign in before downloading the file.

## Install On Windows

The app is portable, so there is no setup program to run.

1. Open your **Downloads** folder.
2. Right-click **MCA-Question-Presenter-Windows.zip** and choose
   **Extract All...**, then click **Extract**.
3. Open the new extracted folder.
4. If you see **MCA Question Presenter Windows.zip** inside it, right-click that
   file, choose **Extract All...**, then click **Extract** again.
5. Open the **MCA Question Presenter** folder.
6. Double-click **MCA Question Presenter.exe**.

Keep **MCA Question Presenter.exe** and the **_internal** folder together. The
app will not work if you move the `.exe` file by itself.

### If Windows Shows A Warning

Windows may show a blue **Windows protected your PC** message the first time you
open the app.

Only continue if you downloaded the app from this repository or received it
from a trusted instructor. Click **More info**, then click **Run anyway**.

## Use The App

When the app starts, two windows open:

- **Instructor controls** — use this to choose questions, move forward or back,
  and reveal answers.
- **MCA Question Display** — share this window with your students.

The Navigation question bank opens automatically. To use the included Stability
questions, select that bank in the instructor controls and click **Load
Selected**.

You can also click **Load CSV...** to open your own question bank.

### Keyboard Shortcuts

- **Right arrow:** next question
- **Left arrow:** previous question
- **Space** or **Enter:** reveal or hide the answer
- **F11:** make the question display full screen
- **Escape:** leave full-screen mode

## Help

See the [full user guide](docs/user-guide.md) for screen-sharing advice, custom
question-bank instructions, and troubleshooting. A
[PDF user guide](docs/mca-question-presenter-user-guide.pdf) is also available.

## For Developers

The following information is only needed if you want to change or build the
software yourself.

### Run From Source

Windows:

```powershell
py presenter\mca_question_presenter.py
```

Linux:

```bash
sudo apt install python3-tk
python3 presenter/mca_question_presenter.py
```

### Question Bank Format

Required CSV columns:

```text
question_text,option_a,option_b,option_c,option_d,correct_option
```

Recommended full format:

```text
portal,question_text,option_a,option_b,option_c,option_d,correct_option,topic_tag,is_active,sort_order
```

`correct_option` must be `A`, `B`, `C`, or `D`.

Rows with an `is_active` value of `0`, `false`, `no`, `inactive`, or blank are
skipped.

### Build The Windows App

Create and activate a Python virtual environment, then install PyInstaller:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pyinstaller
```

Build the app:

```powershell
presenter\build_windows.bat
```

The finished app will be in `dist\MCA Question Presenter\`.

### Tests

```bash
python3 -m unittest discover -s tests
python3 -m compileall presenter tests
```
