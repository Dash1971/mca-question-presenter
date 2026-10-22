"""Build the student and instructor PDF guides (development: reportlab)."""
from pathlib import Path
import argparse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

INK=colors.HexColor('#173247'); TEAL=colors.HexColor('#176774'); GREY=colors.HexColor('#516575')
BODY=ParagraphStyle('Body',fontName='Helvetica',fontSize=11,leading=16,textColor=INK,spaceAfter=10)
H1=ParagraphStyle('Title',fontName='Helvetica-Bold',fontSize=27,leading=32,textColor=INK,spaceAfter=14)
H2=ParagraphStyle('Section',fontName='Helvetica-Bold',fontSize=14,leading=19,textColor=TEAL,spaceBefore=10,spaceAfter=7)
SMALL=ParagraphStyle('Small',parent=BODY,fontSize=9,leading=13,textColor=GREY)

STUDENT=[
 ('Start a practice paper',[
 ('MCA OOW Exam Presenter','Navigator | Student guide | 22 October 2026'),
 ('Open the app','On Windows, extract the entire app ZIP. Open the MCA Visual Practice folder and run MCA Visual Practice.exe. Keep its _internal folder beside the executable. The presenter opens in your default browser. No account or internet connection is needed for the bundled questions and figures.'),
 ('Choose your subject','Expand Navigation or Stability &amp; Operations. Each section contains Papers 1 to 4. Select Start paper, Resume paper or View result. Navigation papers have 35 questions each. Stability &amp; Operations Papers 1 to 3 have 35; Paper 4 has 34.'),
 ('Use the Navigator','Select any question number to jump directly to it, or use Previous and Next. On a narrow screen, expand Questions below the question panel. You can answer in any order. Flag for review marks a question to revisit; it does not affect your mark.'),
 ('Enter your answers','For a single-choice question, select one option. For a multi-select question, select every option you consider correct. For matching, choose a definition for every term. For multipart questions, complete every field or dropdown.'),
 ('Numbers and figures','Follow the units, signs and rounding requested. Enter a number only in numeric fields, using a decimal point and a minus sign when required. Do not append units or thousands separators. Use the figure +, - and Reset controls to change magnification. For a placement question, select a label and click its position, or drag it. Click a placed label to remove it.'),
 ('Web edition','If using the web ZIP, extract the whole folder and open index.html in a current browser. Keep the assets folder and other files together. If local-file opening is restricted by your organisation, ask the instructor for the approved setup.'),
 ]),
 ('Finish, save and practise again',[
 ('Saving your place','Answers, flags and your current question save in this browser on this device. Look for Saved on this device. If the app says Progress stays in this session, keep the page open: browser storage is unavailable. There is no account backup or cross-device sync.'),
 ('Check before submitting','Choose Check &amp; submit to see answered, unanswered and flagged counts. These counts show completion, not correctness. A partially completed multipart or matching question remains incomplete. Select a question to revisit it, or Keep working.'),
 ('Submit your attempt','Submit paper finishes and locks the attempt, including unanswered questions. Each question is worth one mark. Every required part must be correct for that mark; there are no partial marks. An extra or missing selection in a multi-select question earns zero for that question. Unanswered questions earn zero.'),
 ('Read your result','The app shows your final percentage and the number correct out of the paper total. The percentage is rounded to the nearest whole number. Correct answers and individual question results are withheld. Record the result before starting again if your instructor needs it.'),
 ('Start another attempt','Choose New attempt on the result screen. Read the confirmation: starting again clears this paper\'s saved answers, flags and result. Keep result cancels. Other papers are unaffected. Choose another paper returns to the library.'),
 ('If progress or figures are missing','Use the same browser, browser profile and app location. Private browsing, cleared browser data, another browser or moving the app can affect saved progress. If a figure is missing, re-extract the complete ZIP. If the executable does not open a browser, ask the instructor to check the default browser or use the web edition.'),
 ('About these papers','These are unofficial OOW Unlimited practice papers based on the stated syllabus topics. They support study alongside instruction and official publications. They use one practice mark per question, and do not reproduce official examination weighting, duration or pass rules. There is no built-in timer or official pass/fail threshold.'),
 ])]

INSTRUCTOR=[
 ('Set up a practice session',[
 ('MCA OOW Exam Presenter','Navigator | Instructor guide | 22 October 2026'),
 ('Student distribution','Give students the Windows app ZIP and Student Guide. Extract the entire ZIP and run MCA Visual Practice.exe inside MCA Visual Practice. Keep the executable and _internal folder together. The web edition contains the same questions and figures; extract it completely and open index.html. No login, Python installation or internet connection is required to run the packaged app.'),
 ('Keep instructor files separate','The instructor pack contains Question-bank.csv, Question-bank.xlsx, Instructor-Answer-Book.html, question-bank.json and review evidence. These include correct answers. Do not add them to a student app folder or student download. The offline app necessarily contains client-side marking keys, so it is suitable for practice rather than a secure high-stakes examination.'),
 ('Assign a paper clearly','Use subject plus paper number, for example Navigation Paper 3. Each subject has four papers. Seven papers contain 35 questions; Stability &amp; Operations Paper 4 contains 34. The collection has 279 questions. Set your own session duration, permitted aids and result-recording method. The app supplies no timer, candidate accounts, central results register or official pass threshold.'),
 ('Before the class','On the actual teaching computer, check that the app opens, both subject sections expand and a figure loads. Try an answer and confirm the save status. Check the intended browser/profile, device access and school download policies. For a fresh attempt after a previous submission, select New attempt and confirm. A shared browser profile shares local attempts; use separate browser/OS profiles where individual records are needed.'),
 ('Results and privacy','Students see only the final percentage and number correct. Arrange collection of results outside the app, such as an observed result screen or a student report. There is no automatic instructor submission or CSV export of student attempts. Record needed results before restarting, moving the app or clearing browser data.'),
 ]),
 ('Marking and instructor checks',[
 ('How marks are calculated','One question equals one mark. Every required part must be correct. Single/multiple choice requires exactly the keyed selections, matching requires all pairs, and placement requires every label inside its accepted rectangle. Multipart fields are all-or-nothing. Blank or incomplete questions score zero. Final percentage = correct questions / scored questions, rounded to a whole percentage.'),
 ('Numeric entry policy','The five reviewed papers use numeric tolerances centred on the rounded keyed answer: half a unit of the last requested decimal place. For example, 1.8 with tolerance 0.05 accepts 1.75 to 1.85, including the bounds. Equivalent decimal formatting is accepted. Empty input does not equal zero. Units belong in labels; numeric parsing expects a decimal point and optional sign, with no unit text or thousands separators. The export lists the actual key and tolerance. Retained questions may use normalised exact text/number matching instead; their rows say so.'),
 ('Use the CSV or workbook','Each row is one question. Filter Subject, Paper, Question or Review scope. The CSV is UTF-8 with a BOM and quoted multiline cells. Import it as UTF-8 comma-separated text if Excel uses a different default delimiter. The workbook adds filter buttons, frozen identifiers, and editable Instructor status and Instructor comments columns for your checking notes. Save your annotated copy separately.'),
 ('Use the offline answer book','Open Instructor-Answer-Book.html in a browser. Search questions, options and keys, then filter by subject, paper or review scope. Open an answer panel to see the key, explanation and review working. Figures are embedded, so the answer book works as a single file. Placement figures show accepted regions and the key gives percentage coordinates from the top-left. Open visible answers expands the filtered set.'),
 ('Question numbers and keys','The Question column matches the number shown in the app. Use Paper ID plus Source question ID for a stable technical reference. Stability &amp; Operations Paper 4 displays 1 to 34 but its source IDs skip 18. Choice numbers in exports are one-based. Matching keys show term-to-definition text. The machine-readable JSON retains complete fields and target rectangles.'),
 ('Make a correction','Record subject, paper, displayed question, the issue and proposed correction in the workbook. Export edits do not change the app. A maintainer must change the authored bank, rebuild it, rerun the audit and tests, then distribute an updated app. Keep notes with stable IDs when transferring them to a later version.'),
 ]),
 ('Accuracy review and maintenance',[
 ('Review completed','On 22 October 2026, Codex performed a separate AI review of Navigation Papers 2, 3 and 4 and Stability &amp; Operations Papers 2 and 3: all 175 questions, their distractors/pairs, answer keys, units, assumptions and syllabus tags. It reconstructed 92 numeric answer fields in 72 questions and checked 19 further quantitative choices. All numeric keys agreed. All five training figures were checked against their plotted values.'),
 ('Changes before release','Stability &amp; Operations 2 Q29 now uses the definition of weathertight integrity applying in any sea condition. Navigation 4 Q11 explicitly says the stream sets due north. Stability &amp; Operations 3 Q30 excludes exceptional Annex V situations from its routine plastics-disposal question. Two syllabus tags were corrected: Navigation 4 Q4 and Stability &amp; Operations 3 Q7. Source specificity and punctuation were improved.'),
 ('Review scope and limits','This is an AI accuracy review, not independent human maritime examiner certification. The other 104 questions are outside this focused review and are identified per export row. The papers cover the main syllabus sections rather than every sub-outcome, official weighting or the full depth of written examination work. Training curves and hydrostatics are artificial exercise data. Practical choices state principles and ship procedures, not complete emergency checklists.'),
 ('References and evidence','The basis is MCA 034-83 and 034-84, version June 2024, used from March 2025 examinations onwards. Per-question URLs identify primary MCA, IMO, ILO, NOAA, Canadian Coast Guard and AMSA references. content-review.md records findings and limitations; review-audit.json records each reviewed question and the reviewed bank hash. additional-paper-review.json contains the full five-paper keys and rationales. Consult current authoritative publications when teaching operational or legislative topics.'),
 ('Build verification and limits','The release is built on Windows by GitHub Actions with marking and bank tests. Browser interactions were exercised through a local HTTP server on macOS. Direct file launch could not be exercised through the available browser automation, and the Windows executable was not interactively run on this Mac. Perform the classroom opening check on the intended Windows devices before teaching.'),
 ('Updates and saved attempts','The bank and options are fixed between attempts. Browser storage is local and can be cleared or inspected by a user. There is no migration tool for responses after a key or question changes. Before distributing a content update, record any needed old results and use a fresh attempt for an affected paper. Preserve the release manifest and app ZIP together for traceability.'),
 ])]

def build(path,pages,audience):
    story=[]
    for index,(title,sections) in enumerate(pages):
        if index: story.append(PageBreak())
        story.append(Paragraph('OOW UNLIMITED / '+audience.upper(),SMALL));story.append(Paragraph(title,H1))
        for heading,text in sections:
            story += [Paragraph(heading,H2),Paragraph(text,BODY)]
    def footer(canvas,doc):
        canvas.setStrokeColor(colors.HexColor('#D1DEE4'));canvas.line(42,43,A4[0]-42,43)
        canvas.setFont('Helvetica',9);canvas.setFillColor(GREY)
        canvas.drawString(42,28,'MCA OOW Exam Presenter | '+audience+' guide | 22 October 2026')
        canvas.drawRightString(A4[0]-42,28,str(doc.page))
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=32,bottomMargin=56,title=audience+' Guide - MCA OOW Exam Presenter',author='MCA OOW Exam Presenter')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);out=parser.parse_args().output;out.mkdir(parents=True,exist_ok=True)
    build(out/'Student-Guide.pdf',STUDENT,'Student');build(out/'Instructor-Guide.pdf',INSTRUCTOR,'Instructor')
    print('Built student and instructor guides.')
