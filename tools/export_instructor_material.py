"""Export all app questions, figures, keys and review evidence for instructors."""
from __future__ import annotations
import argparse
import base64
import html
import json
import mimetypes
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT/'presenter/web'

def load_papers():
    papers = json.loads((WEB/'papers.js').read_text().removeprefix('window.NEW_PAPERS=').rstrip(' ;\n'))
    original = json.loads((WEB/'paper.js').read_text().removeprefix('window.PAPER=').rstrip(' ;\n'))
    for p in papers:
        if p['questions'] is None: p['questions'] = original
    return papers

def answer_text(q):
    if q['kind'] in ('single','multi'):
        return '\n'.join(f"{i+1}. {q['options'][i]}" for i in q['answer'])
    if q['kind']=='match':
        return '\n'.join(f"{term} = {q['definitions'][i]}" for term,i in zip(q['terms'],q['answers']))
    if q['kind']=='fields':
        values = q.get('answers') or [f['answer'] for f in q['fields']]
        return '\n'.join(f"{f['label']} = {value}" + (f" (tolerance +/-{f['tolerance']:g})" if 'tolerance' in f else ' (normalised exact match)') for f,value in zip(q['fields'],values))
    return '\n'.join(f'{token}: x={r[0]}..{r[2]}%, y={r[1]}..{r[3]}%' for token,r in q['targets'].items())

def export(out):
    out.mkdir(parents=True,exist_ok=True)
    review = json.loads((ROOT/'tools/additional-paper-review.json').read_text())
    audit = json.loads((ROOT/'tools/review-audit.json').read_text())
    reviewed = {(p['id'],q['id']):q for p in review['papers'] for q in p['questions']}
    checks = {(q['paper_id'],q['question']):q for q in audit['questions']}
    rows, cards = [], []
    for p in load_papers():
        subject = 'Navigation' if p['subject']=='navigation' else 'Stability & Operations'
        for displayed,q in enumerate(p['questions'],1):
            entry = reviewed.get((p['id'],q['id']))
            check = checks.get((p['id'],q['id']))
            options = '\n'.join(f'{i+1}. {v}' for i,v in enumerate(q.get('options',[])))
            if q['kind']=='match': options = 'Terms: '+ '; '.join(q['terms'])+'\nDefinitions:\n'+'\n'.join(f'{i+1}. {v}' for i,v in enumerate(q['definitions']))
            if q['kind']=='fields': options='\n'.join(f['label']+(': '+ '; '.join(f['choices']) if f.get('choices') else '') for f in q['fields'])
            if q['kind']=='place': options='Labels: '+', '.join(q['tokens'])
            row = {'Subject':subject,'Paper':p['number'],'Question':displayed,'Paper ID':p['id'],'Source question ID':q['id'],
                   'Title':q['title'],'Syllabus reference':q.get('syllabus',''),'Type':q['kind'],
                   'Question text':q['prompt'],'Context':q.get('context',''),'Options or fields':options,
                   'Correct answer':answer_text(q),'Explanation':entry['rationale'] if entry else 'Outside focused five-paper accuracy review. Key exported from the retained app bank.',
                   'Figure':q.get('image',''),'Review scope':'Reviewed 2026-10-22 (AI)' if entry else 'Outside focused review',
                   'Review method':check['method'] if check else '', 'Review working':check['review_note'] if check else '',
                   'Primary references':'\n'.join(review['references'][key] for key in entry['sources']) if entry else ''}
            rows.append(row)
            esc = html.escape
            image = ''
            if q.get('image'):
                path = WEB/q['image']
                mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
                data = base64.b64encode(path.read_bytes()).decode()
                image = f'<div class="figure"><img alt="{esc(q["title"])}" src="data:{mime};base64,{data}">'
                if q['kind']=='place':
                    for token,(x1,y1,x2,y2) in q['targets'].items():
                        image += f'<span class="target" style="left:{x1}%;top:{y1}%;width:{x2-x1}%;height:{y2-y1}%">{esc(token)}</span>'
                image += '</div>'
            cards.append(f'<article data-subject="{esc(subject)}" data-paper="{p["number"]}" data-reviewed="{bool(entry)}"><h2>{esc(subject)} · Paper {p["number"]} · Q{displayed}</h2><p class="meta">{esc(row["Title"])} · {esc(row["Syllabus reference"])} · {esc(row["Review scope"])}</p><p>{esc(row["Context"])}</p><p>{esc(q["prompt"])}</p>{image}<pre>{esc(options)}</pre><details><summary>Answer and explanation</summary><pre>{esc(row["Correct answer"])}</pre><p>{esc(row["Explanation"])}</p><p>{esc(row["Review working"])}</p><p class="references">'+ '<br>'.join(f'<a href="{esc(u,quote=True)}">{esc(u)}</a>' for u in row['Primary references'].splitlines())+'</p></details></article>')
    assert len(rows)==279 and sum(r['Review scope'].startswith('Reviewed') for r in rows)==175
    (out/'question-bank.json').write_text(json.dumps({'release_date':'2026-10-22','rows':rows,'papers':load_papers()},ensure_ascii=False,indent=2)+'\n')
    doc = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OOW Instructor Answer Book</title><style>body{font:17px/1.55 Arial,sans-serif;background:#f2f5f7;color:#172c3a;margin:0}header,main{max-width:1000px;margin:auto;padding:24px}header{background:#fff}h1{margin:0}label{display:block;margin:12px 0}input,select,button{font:inherit;padding:8px}input{width:min(90%,600px)}article{background:white;border:1px solid #cbd7dc;border-radius:8px;padding:24px;margin:20px 0}h2{font-size:21px;margin:0}.meta{color:#536975;font-size:14px}pre{white-space:pre-wrap;font:inherit}.figure{position:relative;width:fit-content;max-width:100%;margin:20px 0}.figure img{display:block;max-width:100%;max-height:650px}.target{position:absolute;border:2px solid #b90018;background:#ffffffad;font-size:12px;color:#960015}summary{cursor:pointer;font-weight:bold;color:#125b65}.references{font-size:12px;overflow-wrap:anywhere}[hidden]{display:none!important}@media print{header label,header button{display:none}article{break-inside:avoid}details:not([open]){display:none}body{background:white}}</style><header><h1>Instructor answer book</h1><p>279 questions across eight papers. Contains keys: keep separate from the student app. The focused AI accuracy review covers 175 questions. Other rows are identified as outside that review. Placement boxes use percentage coordinates from the figure’s top-left.</p><label>Search questions, options and keys <input id="search" type="search"></label><label>Subject <select id="subject"><option value="">All subjects</option><option>Navigation</option><option>Stability &amp; Operations</option></select> Paper <select id="paper"><option value="">All papers</option><option>1</option><option>2</option><option>3</option><option>4</option></select> <select id="scope"><option value="">All review scopes</option><option value="True">Reviewed 175</option><option value="False">Outside focused review 104</option></select></label><button id="expand">Open visible answers</button> <button id="collapse">Close answers</button><p id="count"></p><p>CSV/workbook row numbers use the displayed question number. Stability &amp; Operations Paper 4 has 34 questions; its underlying IDs skip 18. Explanations and review working are available for the five reviewed papers. Exported keys for other papers are not newly certified.</p></header><main>'''+''.join(cards)+'''</main><script>const cards=[...document.querySelectorAll('article')];function filter(){let n=0;const s=document.querySelector('#search').value.toLowerCase();for(const a of cards){a.hidden=!(a.textContent.toLowerCase().includes(s)&&(!subject.value||a.dataset.subject===subject.value)&&(!paper.value||a.dataset.paper===paper.value)&&(!scope.value||a.dataset.reviewed===scope.value));if(!a.hidden)n++}document.querySelector('#count').textContent=n+' questions shown'}const subject=document.querySelector('#subject'),paper=document.querySelector('#paper'),scope=document.querySelector('#scope');document.querySelector('#search').oninput=filter;subject.onchange=paper.onchange=scope.onchange=filter;document.querySelector('#expand').onclick=()=>cards.filter(a=>!a.hidden).forEach(a=>a.querySelector('details').open=true);document.querySelector('#collapse').onclick=()=>cards.forEach(a=>a.querySelector('details').open=false);filter();</script></html>'''
    (out/'Instructor-Answer-Book.html').write_text(doc)
    for path in ('tools/review-audit.json','tools/additional-paper-review.json','docs/content-review.md'):
        shutil.copy2(ROOT/path,out/Path(path).name)
    (out/'READ-ME.txt').write_text('INSTRUCTOR MATERIAL - ANSWERS INCLUDED\n\nOpen Instructor-Answer-Book.html in a browser. All figures are embedded. Search, filter by subject/paper/review scope, and open answer panels.\n\nQuestion-bank.csv is UTF-8 with a BOM for Excel. Each row is one question; multiline cells preserve options, keys, units and tolerances. Import as UTF-8 comma-separated text if your spreadsheet uses a different default separator. The workbook offers the same data with filters. Neither file changes the app.\n\nQuestion numbers match the app. Paper ID plus Source question ID is the stable key; use Subject, Paper and Question for teaching. The five reviewed papers contain 175 questions; 104 retained questions are outside this focused AI accuracy review. Read content-review.md for findings and limits.\n\nDo not include this folder in student distribution. The offline app itself contains marking keys and is intended for practice, not secure examinations.\n')
    print(f'Exported {len(rows)} questions, including 175 reviewed, to {out}')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('output',type=Path)
    export(parser.parse_args().output.resolve())
