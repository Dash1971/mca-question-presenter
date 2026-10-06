"""One-off importer for the supplied mock. Requires PyMuPDF; never bundles source PDF."""
from __future__ import annotations

import json
import re
import sys
from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'presenter' / 'web'
ASSETS = WEB / 'assets'
# number: page, option y-start, option y-end, mode, answer (zero-based)
CONFIG = {
 6:(8,100,250,'multi',[0,1,2]),7:(8,550,710,'single',[4]),
 8:(9,425,640,'single',[1]),9:(10,125,310,'single',[3]),
 10:(11,300,715,'multi',[10,11]),11:(12,100,315,'multi',[0,1,2,4,5]),
 12:(12,495,690,'multi',[0,1,4]),13:(13,100,740,'multi',None),
 16:(16,420,650,'single',[4]),17:(17,90,355,'multi',[3,4,5,6]),
 18:(18,190,440,'fields',None),19:(19,365,610,'single',[5]),
 20:(20,95,250,'single',[1]),22:(22,255,480,'single',[2]),
 23:(23,85,360,'single',[0]),24:(24,175,710,'multi',[3,6,9]),
 25:(25,295,610,'multi',[0,3,6,7,8]),26:(26,100,250,'multi',[1,3]),
 27:(26,395,630,'multi',[1,3,4]),28:(27,105,390,'multi',[1,3,4,5]),
 29:(28,105,410,'multi',[0,1,2,5]),30:(29,105,385,'multi',[2,3,5]),
 31:(30,320,680,'multi',[1,2,3]),34:(33,370,650,'multi',None),
 35:(34,445,610,'single',[3]),
}
IMAGE_PAGES = {1:3,2:5,3:4,4:4,5:4,8:9,10:11,16:16,19:19,21:21,22:22,24:24,31:30,32:31,33:32,34:33,35:34}
TITLE = {
 1:'Southampton tide and under-keel clearance',2:'Heavy lift: position W and G',
 3:'Heavy lift: stage 1',4:'Heavy lift: stage 2',5:'Heavy lift: stage 3',
 6:'Heavy lift preparations',7:'Winter loading allowance',8:'Read the draught marks',
 9:'IMDG placard positions',10:'Identify IMDG labels',11:'Leaking Class 3 cargo',
 12:'High-loading stability',13:'Mariners’ Routeing Guides',14:'Routeing measures',
 15:'TSS Rule 10',16:'Magenta ECDIS symbol',17:'CATZOC features',
 18:'Grimsby tidal crossing',19:'Yellow ECDIS symbol',20:'ECDIS safety contour',
 21:'Chartlet annotations',22:'Ship clock adjustment',23:'Deck edge immersion',
 24:'CATZOC six-star symbol',25:'Navigational watch handover',
 26:'Master’s standing orders',27:'Approaching a TSS',28:'Restricted visibility',
 29:'Under-keel clearance at sea',30:'Tender vessel',31:'GZ curve',
 32:'Position G and M',33:'Limiting-latitude route',34:'Rule 10 traffic diagram',
 35:'Required speed to pilot station'
}
SYLLABUS = {1:'5b',2:'8f',3:'8f',4:'8f',5:'8f',6:'6a',7:'7d',8:'6a',9:'6a',10:'6a',11:'6a',12:'8f',13:'2b',14:'2b',15:'2a',16:'1d',17:'1d',18:'5a',19:'1d',20:'1a 1d',21:'2b',22:'4a',23:'8d',24:'1d',25:'6a',26:'6a',27:'6a',28:'6a',29:'6a',30:'8e',31:'8c 8e',32:'8b',33:'3b',34:'2a',35:'3b'}
MOVEMENT=['Moves downwards and to starboard','Moves vertically upwards','No change','Moves downwards and to port','Moves upwards and to starboard','Moves vertically downwards','Reduces','Moves horizontally to port','Moves horizontally to starboard','Increases','Moves upwards and to port']
GM_CHOICES=['Increases','Reduces','No change','Moves vertically upwards','Moves vertically downwards','Moves upwards and to port','Moves upwards and to starboard','Moves downwards and to port','Moves downwards and to starboard','Moves horizontally to port','Moves horizontally to starboard']
SPECIAL = {
 1:dict(page=3,kind='fields',prompt='A vessel enters Southampton on 6 May 2026 at 06:40. Charted bar depth 10 m; arrival draught 8.0 m. Use the tidal table to find height of tide and under-keel clearance.',fields=[{'label':'Height of tide (m)','answer':'1.2'},{'label':'UKC (m)','answer':'3.2'}],note='UKC = charted depth + height of tide − draught.'),
 2:dict(page=5,kind='place',prompt='Drag W1–W3 and G1–G3 onto the heavy-lift diagram for three stages: lifted on port, slewed to starboard, and landed ashore.',tokens=['W1','W2','W3','G1','G2','G3'],note='Placement exercise: compare the suspended load position with the ship’s resulting center of gravity at each stage.'),
 3:dict(page=6,kind='fields',prompt='Stage 1: the weight is initially lifted with the crane on the port side. Indicate the effect on G, GM, and list.',fields=[{'label':'Center of gravity','choices':MOVEMENT},{'label':'Metacentric height','choices':GM_CHOICES},{'label':'List','choices':['Port list','Starboard list','No list']}]),
 4:dict(page=7,kind='fields',prompt='Stage 2: the suspended weight is slewed to starboard over the quay. Indicate the effect on G, GM, and list.',fields=[{'label':'Center of gravity','choices':MOVEMENT},{'label':'Metacentric height','choices':GM_CHOICES},{'label':'List','choices':['Starboard list','No list','Port list']}],answers=['Moves horizontally to starboard','No change','Starboard list']),
 5:dict(page=7,kind='fields',prompt='Stage 3: the weight is landed on the quay. Indicate the effect on G, GM, and list.',fields=[{'label':'Center of gravity','choices':MOVEMENT},{'label':'Metacentric height','choices':GM_CHOICES},{'label':'List','choices':['Increases to port','To port, reducing','No list','Increases to starboard','To starboard, reducing']}]),
 14:dict(page=14,kind='match',prompt='Match each IMO routeing measure to its definition.',terms=['Traffic Separation Scheme (TSS)','Traffic Lane','Separation Zone or Line','Roundabout','Inshore Traffic Zone','Recommended Route','Deep-water Route','Precautionary Area','Area to be avoided'],definitions=['A routeing measure separating opposing streams of traffic by establishing traffic lanes','An area within defined limits in which one-way traffic is established','A zone or line separating traffic lanes proceeding in opposite or nearly opposite directions','A separation point or circular separation zone and circular traffic lane','The area between a TSS landward boundary and the adjacent coast','A route for ships in transit, often marked by centerline buoys','A route accurately surveyed for seabed clearance','An area requiring particular caution, possibly with a recommended traffic flow','An area where navigation is particularly hazardous and which should be avoided'],answers=list(range(9))),
 15:dict(page=15,kind='fields',prompt='Complete Rule 10: Proceed ___ in the direction of traffic flow. ___ the separation line/zone as far as practicable.',fields=[{'label':'First blank','choices':['stay close to','keeping to the centre','generally','parallel','keep clear of','keeping to the starboard side','if possible','in the correct lane','primarily']},{'label':'Second blank','choices':['stay close to','keeping to the centre','generally','parallel','keep clear of','keeping to the starboard side','if possible','in the correct lane','primarily']}],answers=['in the correct lane','keep clear of']),
 21:dict(page=21,kind='fields',prompt='Identify the three highlighted types of information on the chartlet (top, middle, bottom callouts).',fields=[{'label':x,'choices':['Prevailing winds/Wind Roses','Predominant Ocean currents','Ice limits','Load Lines zones','Recommended Routes','Traffic Separation Schemes','Depth Contours','Index Numbers','Zones of Confidence']} for x in ['Top callout','Middle callout','Bottom callout']],answers=['Prevailing winds/Wind Roses','Predominant Ocean currents','Load Lines zones']),
 32:dict(page=31,kind='place',prompt='Drag G and M onto the ship transverse-section diagram for stable equilibrium at a small heel.',tokens=['G','M'],note='G and M must lie on the appropriate centerline; for stable equilibrium M is above G.'),
 33:dict(page=32,kind='fields',prompt='A vessel from Tokyo to Los Angeles is limited to 48° N until 160° W. What type of route follows a limiting latitude, and what true course is required?',fields=[{'label':'Route type','choices':['Plane Sailing','Great Circle','Parallel Sailing','Mercator Sailing']},{'label':'Course (degrees true)','answer':'090'}],answers=['Parallel Sailing','090']),
}


def clean(value):
    return re.sub(r'\s+', ' ', value.replace('\xa0',' ')).strip()


def main(pdf_path: Path) -> None:
    doc=fitz.open(pdf_path)
    if len(doc)!=34: raise ValueError('Expected the 34-page supplied mock PDF')
    ASSETS.mkdir(parents=True,exist_ok=True)
    images={}
    for n,page_no in sorted(IMAGE_PAGES.items()):
        if page_no in images: continue
        page=doc[page_no-1]
        if page_no==33:
            pix=page.get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(62,74,535,340),alpha=False)
            image=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        else:
            xref=page.get_images(full=True)[0][0]
            image=Image.open(BytesIO(doc.extract_image(xref)['image'])).convert('RGB')
        target=ASSETS/f'figure-p{page_no:02}.webp'
        image.save(target,'WEBP',quality=88,method=5)
        images[page_no]=f'assets/{target.name}'
    records=[]
    for n in range(1,36):
        rec={'id':n,'title':TITLE[n],'syllabus':SYLLABUS[n]}
        if n in SPECIAL:rec.update(SPECIAL[n])
        else:
            page_no,start,end,mode,key=CONFIG[n]
            page=doc[page_no-1]
            blocks=page.get_text('blocks')
            opts=[clean(b[4]) for b in blocks if 78<=b[0]<=105 and start<=b[1]<end and clean(b[4])]
            heading_y=max((b[1] for b in blocks if clean(b[4]).startswith(f'{n} Syllabus')),default=27)
            prompt_end=start-3 if n not in (22,35) else end
            prompt=[clean(b[4]) for b in blocks if 55<=b[0]<=77 and b[1]>heading_y and b[1]<prompt_end and clean(b[4]) and not clean(b[4]).startswith('Ref:')]
            prompt=' '.join(prompt)
            prompt=re.sub(r'(?:Select all correct answers(?: that apply)?|Select only the correct answers|Select the correct answer):?\s*$', '',prompt).strip()
            rec.update(page=page_no,kind=mode,prompt=prompt,options=opts)
            if key is not None:rec['answer']=key
            if n==18:
                rec['fields']=[{'label':'Earliest crossing','choices':opts[:4]},{'label':'Latest crossing','choices':opts[4:]}]
                rec.pop('options')
                rec['note']='The source PDF omits the tidal stimulus for this question. The required tide height is 5.5 m; a crossing window cannot be verified from this file.'
            if n==13:rec['note']='The source response is only partially marked; this wording has not been independently keyed.'
            if n==34:rec['note']='The source export does not identify every correct vessel; use the chart and review with an instructor.'
        if n in IMAGE_PAGES:rec['image']=images[IMAGE_PAGES[n]]
        if n in (26,27,28,29):rec['context']='North Sea watch: visibility 4 NM with snow showers; moderate traffic approaching a TSS. The Master orders a call below 2 NM or if collision risk arises. At 2200 a target is on a steady bearing at 4 NM; shallow patches lie ahead.'
        records.append(rec)
    # No candidate, creator, result, selected response, or source PDF is stored.
    payload='window.PAPER='+json.dumps(records,ensure_ascii=False,separators=(',',':'))+';\n'
    if re.search(r'Candidate|Created by|Partially Correct|Wrong\. 0',payload,re.I):
        raise ValueError('Personal or result text leaked into question data')
    (WEB/'paper.js').write_text(payload,encoding='utf-8')
    print('Wrote',len(records),'questions and',len(images),'figures')
    for q in records:
        if q.get('kind') in ('single','multi') and len(q.get('options',[]))<3:
            print('CHECK OPTIONS',q['id'],q.get('options'))

if __name__=='__main__':
    main(Path(sys.argv[1]))
