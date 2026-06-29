@echo off
setlocal

cd /d "%~dp0\.."

python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --name "MCA Question Presenter" ^
  --add-data "samples;samples" ^
  presenter\mca_question_presenter.py

endlocal
