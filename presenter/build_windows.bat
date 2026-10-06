@echo off
setlocal
cd /d "%~dp0\.."
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onedir ^
  --windowed ^
  --name "MCA Visual Practice" ^
  --add-data "presenter\web;presenter\web" ^
  presenter\mca_question_presenter.py
endlocal
