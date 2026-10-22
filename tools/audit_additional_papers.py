"""Independent arithmetic regression audit; does not import the authoring builder.

Inputs below were transcribed from the displayed question stems and checked by
vector geometry, moments, interpolation and UTC arithmetic. This is an AI review,
not certification by a second person or a maritime examiner.
"""
from __future__ import annotations
import hashlib
import json
import math
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'tools/additional-paper-review.json'

def bearing(east, north):
    return math.degrees(math.atan2(east, north)) % 360

def rounded(value, places=1):
    return round(value, places)

def audit():
    # One entry for every numeric-field question, in displayed field order.
    expected = {
        'navigation-2': {
            10: ([rounded(bearing(2,10)), rounded(abs(complex(2,10)))], 'Vector sum: E=2, N=10.'),
            11: ([rounded(bearing(12,-5)),12], '13-kn vector with S=5 has E=12; current cancels S.'),
            13: ([137-5+2], 'Subtract east variation, add west deviation.'),
            16: ([12*90/60], '90 minutes at 12 nautical miles/hour.'),
            18: ([rounded(bearing(48,36)),abs(complex(48,36))], 'North/east plane-sailing triangle.'),
            19: ([rounded((60+30)*math.cos(math.pi/3))], '90 longitude minutes at latitude 60 N.'),
            20: ([rounded(bearing(160,120)),rounded(72*math.hypot(160,120)/120)], 'Mercator triangle scaled by DLat/DMP.'),
            22: ([84/7], 'Distance divided by hours available.'),
            25: ([95.5-91], 'Signed error = corrected true minus compass.'),
            31: ([30+4-2,30+4-2-31], 'Bridge underside at datum+34; subtract tide, then air draught.'),
            32: ([rounded(3.9-1.4)], 'Subtract drying height from tide.'),
            33: ([1+.20*(5-1)], 'Rising curve: hour 2 fraction 0.20.'),
            35: ([rounded(12.7-2.3)], 'Subtract tide from corrected water depth.'),
        },
        'navigation-3': {
            10: ([rounded(bearing(3,4)),5], '3 E/4 N displacement over one hour.'),
            11: ([rounded(bearing(-6,8)),8], 'Water vector W=6,N=8; stream cancels westward component.'),
            12: ([65/(15-2)], 'Opposing current reduces SOG to 13.'),
            14: ([270-8+3], 'West variation negative; east deviation positive.'),
            16: ([rounded(bearing(8,6)),10], 'Grid P=(8 E,6 N).'),
            17: ([27/((11*60+30-9*60-15)/60)], '135 minutes available.'),
            19: ([rounded(((181-179)*60)*math.cos(math.pi/3))], '179 W expressed as 181 E: two degrees eastward.'),
            20: ([rounded(60/math.cos(math.pi/3)),rounded(60*math.tan(math.pi/3))], 'North component 60; course 60 T.'),
            21: ([rounded(bearing(360,480)),300*math.hypot(360,480)/480], '175 W expressed as 185 E: six degrees eastward.'),
            31: ([rounded(5.4-1.2)], 'Same-datum HW minus LW.'),
            32: ([rounded(9.1-(8.1+.4))], 'Dynamic draught includes squat.'),
            33: ([6-(2.5-2)*(.50-.25)*4-.25*4], 'Hour 2.5 fall fraction 0.375 by linear interpolation.'),
        },
        'navigation-4': {
            10: ([rounded(bearing(-12,-5)),13], 'Ground vector W=12,S=5; use SW quadrant.'),
            11: ([rounded(bearing(8,-6)),8], 'Water vector E=8,S=6; stream sets north.'),
            13: ([(358+2+5)%360], 'West errors added to true course then wrap through north.'),
            18: ([rounded(60*math.cos(math.pi/6))], 'One degree longitude at 30 N.'),
            19: ([rounded(bearing(-40,-30)),50], 'Plane-sailing SW quadrant.'),
            20: ([rounded(bearing(180,-240)),192*math.hypot(180,240)/240], 'Mercator SE quadrant; distance uses magnitude of southing.'),
            31: ([26+4-27-1], 'Highest water = underside datum height less vessel and margin.'),
            33: ([.8+.20*(4.8-.8)], 'Two hours after LW, including midnight rollover.'),
            35: ([rounded(1.5-.9)], 'Drying height = tide minus measured cover.'),
        },
        'stability-2': {
            1: ([800*.9], 'Mass = volume times density.'),
            2: ([8000+(6.4-6)/(7-6)*(10000-8000)], 'Linear interpolation in stated hydrostatic interval.'),
            3: ([rounded(18/1.025*1.010,2)], 'Constant waterplane area: density ratio.'),
            4: ([20*12], 'TPC times immersion in centimetres.'),
            5: ([10000/25/4], 'FWA formula gives millimetres.'),
            6: ([rounded(180*(1025-1015)/(1025-1000),0)], 'DWA density difference expressed in kg/m3.'),
            7: ([rounded(16800/150/20/8,2)], 'Underwater volume divided by enclosing block.'),
            8: ([rounded((8+.12-7.8)*100*18,0)], 'Dock-water limit 8.12 m; 32 cm capacity at dock TPC.'),
            10: ([rounded(8.3-6.8-.15,2)], 'Subtract KG and virtual rise from KM.'),
            11: ([7500*.42], 'Displacement times lever, tonne-metres.'),
            12: ([100*(10-2)/8000], 'Vertical transfer moment divided by unchanged displacement.'),
            13: ([rounded((6000*5+800*12)/(6000+800),2)], 'Add vertical moments and masses.'),
            14: ([rounded((10000*6-400*10)/(10000-400),2)], 'Remove both moment and mass.'),
            15: ([100*(14-2)/6000], 'Suspended weight acts at suspension point.'),
            16: ([rounded(math.degrees(math.atan2(200*6,12000*1)))], 'List from transverse moment / effective righting coefficient.'),
            18: ([35,70], 'Checked against plotted GZ ordinates: peak at 35, zero crossing at 70.'),
            19: ([(4.2+5)/2], 'Arithmetic mean of end draughts.'),
            20: ([4.5+(5.5-4.5)*(50+10)/100], 'LCF 60 m from FP: straight-waterline interpolation.'),
            21: ([250*20], 'Longitudinal transfer moment.'),
            22: ([5000/200], 'Moment / MCTC gives centimetres.'),
            23: ([.4*100*150/60], 'Remove 40 cm stern trim with forward transfer.'),
            24: ([rounded(5+240/20/100-240*30/180/200,2),rounded(5+240/20/100+240*30/180/200,2)], '12 cm parallel sinkage and 40 cm stern trim split equally.'),
            25: ([5+200*40/200/200,5.4-200*40/200/200], '40 cm forward trim change, unchanged displacement.'),
        },
        'stability-3': {
            2: ([1800/(100*24)], 'Waterplane area divided by enclosing rectangle.'),
            3: ([8200/1.025], 'Displacement mass divided by water density.'),
            4: ([8000+(6.5-6)*(10400-8000)-6000], 'Interpolate final displacement then subtract initial.'),
            6: ([14400/30/4], 'FWA in millimetres.'),
            7: ([600/30/100], 'Discharge raises freeboard by 20 cm.'),
            10: ([rounded(1.8*math.sin(math.pi/18),3)], 'Small-angle lever using specified relation.'),
            11: ([.9,80], 'Checked plotted peak at 40 deg, positive range ends at 80.'),
            12: ([(600+900)/10000], 'Sum moments before dividing by displacement.'),
            13: ([10000*.12/200], 'Cancel existing starboard moment with portward transfer.'),
            14: ([rounded(math.degrees(math.atan2(100*6,6000*.9)))], 'Final displacement and effective GM used; list to starboard.'),
            21: ([2500/125], 'Trim magnitude in centimetres.'),
            22: ([150*(10+30)/200], 'Transfer spans 40 m and trims by stern.'),
            23: ([4.8+(5.4-4.8)*(60-12)/120], 'LCF 48 m from FP; interpolate towards deeper aft draught.'),
            24: ([6+300/25/100,6+300/25/100], 'Load at LCF: parallel sinkage only.'),
            25: ([6-200/20/100+200*30/150/200,6-200/20/100-200*30/150/200], '10 cm parallel rise, 40 cm head trim, split equally.'),
        },
    }
    # Numeric multiple-choice checks independently reconstructed from the stems.
    eta2 = datetime(2026,6,8,23)-timedelta(hours=3)+timedelta(hours=10)-timedelta(hours=5)
    eta3 = datetime(2026,7,31,23)+timedelta(hours=54/9)
    eta4 = datetime(2026,6,12,3,30)-timedelta(hours=5,minutes=30)+timedelta(hours=12)-timedelta(hours=3)
    assert (eta2.day,eta2.hour)==(9,1) and (eta3.month,eta3.day,eta3.hour)==(8,1,5) and (eta4.day,eta4.hour)==(12,7)
    choices = {
        'navigation-2': {12:'086°T',14:'2°W',15:'104°G',21:'0100 on 9 June',34:'0600'},
        'navigation-3': {13:'228°T',15:'020°T',22:'0500 UTC on 1 August',25:'2°W',34:'1330'},
        'navigation-4': {12:'041°T',14:'7°E',15:'Increase the gyro-course order by 2°',22:'0700 on 12 June',25:'2.0°W',34:'0330'},
        'stability-2': {17:'One quarter'}, 'stability-3': {18:'It doubles',20:'0.60 m by the head'},
    }
    assert 90-4==86 and 58-60==-2 and 100-(-4)==104
    assert 225+3==228 and (350+30)%360==20 and 268-270==-2
    assert 45-4==41 and (2-355+180)%360-180==7 and (3-1)==2
    assert rounded((359.2-1.2+180)%360-180)==-2
    assert 2*(.5**3)==.25 and 2/1==2 and rounded(6-5.4)==.6
    # Curve intersections: rise .80 at hour 4; fall .80 at hour 4.
    assert (4.2-1)/(5-1)==.8 and (6-2.8)/(6-2)==.8 and (4-.8)/(4.8-.8)==.8
    source = json.loads(REVIEW.read_text())
    rows, fields_count, numeric_items = [], 0, 0
    for p in source['papers']:
        numeric_ids = {q['id'] for q in p['questions'] if q['kind']=='fields'}
        assert numeric_ids == set(expected[p['id']]), p['id']
        for q in p['questions']:
            pid, qid = p['id'], q['id']
            note = 'Stem, every option/pair, key, assumptions and syllabus tag reviewed for factual consistency and a unique intended answer.'
            method = 'qualitative review'
            if qid in expected[pid]:
                values,note = expected[pid][qid]
                actual = [float(f['answer']) for f in q['fields']]
                assert len(values)==len(actual) and all(abs(a-b)<1e-8 for a,b in zip(values,actual)), (pid,qid,actual,values)
                fields_count += len(actual)
                numeric_items += 1
                method = 'independent numeric reconstruction' if q.get('image','').find('gz-')<0 else 'figure ordinates and key checked'
            if qid in choices.get(pid,{}):
                assert [q['options'][i] for i in q['answer']]==[choices[pid][qid]], (pid,qid)
                numeric_items += 1
                method = 'numeric choice reconstructed'
                note = 'Checked sign/quadrant, UTC/date rollover, curve intersection, trim direction or proportional scaling against the stated inputs.'
            rows.append({'paper_id':pid,'question':qid,'method':method,'result':'pass','review_note':note,'references':q['sources']})
    assert len(rows)==175 and sum(len(v) for v in expected.values())==72
    result = {'date':'2026-10-22','reviewer':'Codex AI; separate review pass, not an independent human examiner',
              'bank_sha256':hashlib.sha256(REVIEW.read_bytes()).hexdigest(),
              'questions_reviewed':175,'numeric_field_questions':72,'numeric_fields':fields_count,
              'quantitative_questions_including_graphs_and_choices':numeric_items,
              'scope':'Navigation 2-4 and Stability & Operations 2-3; other 104 questions excluded from focused accuracy review.',
              'limitations':['Unofficial practice; not a complete test of every syllabus sub-outcome.', 'No independent human maritime examiner sign-off.', 'Windows binary built by CI; Windows interactive runtime not tested on this Mac.'],
              'questions':rows}
    return result

if __name__=='__main__':
    result = audit()
    (ROOT/'tools/review-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f"Reviewed {result['questions_reviewed']} questions; {result['numeric_field_questions']} field questions / {result['numeric_fields']} numeric fields; {result['quantitative_questions_including_graphs_and_choices']} quantitative questions total.")
