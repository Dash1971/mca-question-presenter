# MCA Question Presenter

MCA Question Presenter is a simple Windows app for displaying multiple-choice
MCA practice questions during a lesson. An instructor controls the questions in
one window and shares a separate, clean question window with students.

It works well in a classroom or while screen-sharing through Zoom, Microsoft
Teams, or Google Meet.

No technical setup is required. You do not need Python, Git, a database, or a
web server.

> This is an unofficial practice and teaching tool. It is not produced or
> endorsed by the Maritime and Coastguard Agency or SQA.

## Included Question Banks

The Windows app includes four banks with 150 questions each:

- **Chief Mate/Master Navigation** — MCA/SQA syllabus 032-73
- **Chief Mate/Master Stability & Structure** — MCA/SQA syllabus 032-74
- **Officer of the Watch Navigation**
- **Officer of the Watch Stability**

## Download The Windows App

1. Open the [Windows download page](https://github.com/Dash1971/mca-question-presenter/actions/workflows/build-windows.yml).
2. Open the newest **Build Windows App** entry that has a green tick.
3. Scroll to the **Artifacts** section at the bottom of the page.
4. Click **MCA-Question-Presenter-Windows**.

The download is a ZIP file. GitHub may ask you to sign in before downloading
it.

## Install And Open It

There is no installer. Extract the downloaded files and run the app directly:

1. Open your Windows **Downloads** folder.
2. Right-click **MCA-Question-Presenter-Windows.zip**.
3. Select **Extract All...**, then click **Extract**.
4. Open the extracted folder.
5. If it contains another file named **MCA Question Presenter Windows.zip**,
   right-click that file and choose **Extract All...** again.
6. Open the **MCA Question Presenter** folder.
7. Double-click **MCA Question Presenter.exe**.

Keep the `.exe` file and the `_internal` folder together. Moving the `.exe` by
itself will stop the app from working.

### Windows Security Warning

Windows may display **Windows protected your PC** the first time the app opens.

Only continue if you downloaded the app from this repository or received it
from a trusted instructor. Click **More info**, then **Run anyway**.

## Run A Lesson

Opening the app displays two windows:

- **Instructor controls** — keep this private. Use it to select a bank or topic,
  move between questions, reshuffle the deck, and reveal answers.
- **MCA Question Display** — share this window with students.

The Officer of the Watch Navigation bank opens automatically.

To use another bank:

1. Select its filename under **Bundled banks**.
2. Click **Load Selected**.
3. Optionally choose a subject from the **Topic** menu.
4. Click **Next** to continue through the shuffled questions.
5. Click **Reveal / Hide** when you are ready to show the answer.

You can also use **Load CSV...** to open a compatible question bank from your
computer.

## Keyboard Shortcuts

- **Right arrow:** next question
- **Left arrow:** previous question
- **Space** or **Enter:** reveal or hide the answer
- **F11:** make the question display full screen
- **Escape:** leave full-screen mode

## Help

The [full user guide](docs/user-guide.md) includes screen-sharing advice, custom
CSV instructions, and troubleshooting. A
[PDF user guide](docs/mca-question-presenter-user-guide.pdf) is also available.

## Developer Information

The rest of this README is only for people who want to change or rebuild the
software.

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
