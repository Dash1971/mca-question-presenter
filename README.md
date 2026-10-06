# MCA Visual Practice

An offline, clickable practice presenter built from the supplied 34-page operations mock paper. It contains **35 numbered questions** and 15 extracted visual figures. The older CSV loader and four synthetic 150-question banks are no longer used.

This is an unofficial study aid, not an MCA, SQA, or IAMI assessment application. It is not an exam browser.

## Use

On Windows, extract the Windows build ZIP, keep the `MCA Visual Practice` folder together, and run **MCA Visual Practice.exe** inside it. It opens the practice paper in the default browser, without a web server or internet connection. From source, run `python presenter/mca_question_presenter.py`, or open `presenter/web/index.html` directly.

- Choose a question by number or use Previous/Next.
- Click one answer or several, as indicated by the question, then **Check answer**.
- For matching, choose a definition for each routeing measure.
- For numerical or multi-part answers, fill each field.
- For placement questions 2 and 32, select or drag a label onto the diagram. Drag it again to reposition. Checking scores each label against accepted regions and shows the correct regions in green.
- Use the figure controls to zoom. Large figures can be scrolled.
- Progress is saved in that browser's local storage on the current computer. There is no account or cloud sync.

All 35 questions provide answer feedback. The scored PDF export supplied keys for the previously ungraded items; the two drag questions use its marked target regions. For question 18, the PDF still omits the tidal stimulus, so a learner cannot independently calculate the crossing times from this document. The app discloses that limitation and identifies the source-marked answer after checking.

The app includes extracted diagrams/charts and question wording only. It does **not** include the source PDF, candidate/creator identities, candidate selections, or marks. Keep it local until rights to distribute the paper and chart figures have been checked.

## Rebuild

Windows (Python and PyInstaller installed):

```bat
presenter\build_windows.bat
```

The app folder appears in `dist\MCA Visual Practice\`. The source paper is **not** needed for normal use and is not bundled. For this paper only, `tools/import_mock.py /path/to/source.pdf` regenerates question data and figures; that development tool requires PyMuPDF and Pillow. Review its output before distributing anything.

## Checks

```sh
python3 -m unittest discover -s tests
python3 -m compileall presenter tools tests
```
