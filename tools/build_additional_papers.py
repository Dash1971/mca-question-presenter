"""Rebuild the five authored papers and their developer-only review record.

No private PDFs are required. Questions below are original; references identify
syllabus outcomes and public guidance, not copied examination questions.
"""
from __future__ import annotations
import json
import math
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'presenter' / 'web'
SOURCES = {
    'navigation': 'https://assets.publishing.service.gov.uk/media/678e2b6eea48a571517acf4f/034-83_OOW_Navigation_Sylabus__Version_-_June_2024___002_.pdf',
    'stability': 'https://assets.publishing.service.gov.uk/media/679a064d1c041dcc469daeab/034-84_OOW_Stability_and_Operations_Syllabus__Version_-_June_2024_.pdf',
    'tss': 'https://www.gov.uk/government/publications/mgn-364-mf-amendment-2-navigation-safety-traffic-separation-schemes-application-of-rule-10-and-navigation-in-the-dover-strait/mgn-364-mf-amendment-2-navigation-safety-traffic-separation-schemes-application-of-rule-10-and-navigation-in-the-dover-strait',
    'watch': 'https://www.gov.uk/government/publications/mgn-315-keeping-a-safe-navigational-watch-on-merchant-vessels',
    'enclosed': 'https://www.gov.uk/guidance/enclosed-spaces-on-sea-going-vessels',
    'marpol': 'https://www.imo.org/en/about/conventions/pages/international-convention-for-the-prevention-of-pollution-from-ships-(marpol).aspx',
    'ism': 'https://www.imo.org/en/ourwork/humanelement/pages/ismcode.aspx',
    'mlc': 'https://www.gov.uk/government/publications/msn-1877-m-maritime-labour-convention-2006-hours-of-work-and-entitlement-to-leave/msn-1877-m-amendment-2-mlc-2006-hours-of-work-and-entitlement-to-leave-application-of-the-hours-of-work-regulations-2018',
    'notices': 'https://www.gov.uk/government/collections/merchant-shipping-notices-msns',
    'complaints': 'https://www.ilo.org/dyn/normlex/en/f?p=NORMLEXPUB%3A91%3A0%3A%3A%3A%3AP91_SECTION%3AMLCA_AMEND_A5',
}
BANKS = []
questions = []
subject = ''
number = 0

def start(category, edition):
    global questions, subject, number
    questions, subject, number = [], category, edition
    BANKS.append({'id': f'{category}-{edition}', 'subject': category, 'number': edition,
                  'title': f'Paper {edition}', 'description': 'OOW Unlimited practice examination.', 'questions': questions})

def add(ref, title, prompt, kind, rationale, source=None, **kwargs):
    def readable(text):
        text = text.replace('the supplied training', 'the training')
        text = re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', text)
        text = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', text)
        text = re.sub(r'(?<=[A-Za-z])\.(?=[A-Z])', '. ', text)
        return text
    q = {'id': len(questions)+1, 'title': title, 'syllabus': ('034-83 ' if subject == 'navigation' else '034-84 ')+ref,
         'prompt': readable(prompt), 'kind': kind, 'rationale': readable(rationale), 'sources': [source or subject], **kwargs}
    if 'options' in q:
        q['options'] = [readable(option) for option in q['options']]
    questions.append(q)
    return q

def choices(ref, title, prompt, correct, wrong, rationale, source=None, **kwargs):
    good = correct if isinstance(correct, list) else [correct]
    options = good + wrong
    assert len(options) == len(set(options)) and len(options) >= 4
    random.Random(f'{subject}-{number}-{len(questions)+1}').shuffle(options)
    return add(ref,title,prompt,'multi' if isinstance(correct,list) else 'single',rationale,source,
               options=options,answer=sorted(options.index(text) for text in good),**kwargs)

def fields(ref,title,prompt,values,rationale,**kwargs):
    return add(ref,title,prompt,'fields',rationale,fields=[{'label': label, 'answer': str(round(value, places)),
               'tolerance': .5*10**(-places)} for label,value,places in values],**kwargs)

def match(ref,title,prompt,pairs,rationale,source=None):
    definitions = [definition for _,definition in pairs]
    random.Random(f'{subject}-{number}-{len(questions)+1}').shuffle(definitions)
    return add(ref,title,prompt,'match',rationale,source,terms=[term for term,_ in pairs],definitions=definitions,
               answers=[definitions.index(definition) for _,definition in pairs])

start('navigation',2)
choices('1a','Appraisal evidence','Before planning a coastal passage, which inputs need to be checked? Select all that apply.',
 ['Current charts and navigational warnings','Draught, manoeuvring limits and available depths','Forecast weather and tidal conditions'],['The previous voyage track alone'],
 'Appraisal considers the vessel, navigation information and expected conditions, rather than treating a previous track as sufficient.')
match('1a','Passage planning responsibilities','Match each passage-plan stage to its main task.',[
 ('Appraisal','Gather and assess relevant information'),('Planning','Develop the detailed route and limits'),('Execution','Put the approved plan into operation'),('Monitoring','Compare actual progress and conditions with the plan')],
 'The four stages have distinct functions; monitoring continues during execution.')
choices('1a','A changed passage plan','A proposed route change introduces a new shallow-water leg. What should happen before using that leg?',
 'Reappraise the risk, amend the plan and brief the bridge team under the ship’s procedures',
 ['Keep the original safety limits without checking them','Follow the new line as soon as it appears on ECDIS','Record the change only after arrival'],
 'An altered route needs the same depth, hazard and operational assessment as the original plan.')
choices('2c','Position-fixing references','Which features are generally suitable independent references for a coastal position fix? Select all that apply.',
 ['A correctly identified fixed lighthouse','An identifiable charted radar-conspicuous headland'],['A moving ship on AIS','An unidentified floating object'],
 'Fixed, positively identified charted objects can support position lines; moving or unidentified targets cannot define a fixed reference.')
choices('2d','Light characteristic','A chart labels a light Fl(3) W 10s. What does the characteristic indicate?',
 'A group of three white flashes in a ten-second period',['Three different white lights ten miles apart','One white flash every thirty seconds','A white light with three fixed sectors'],
 'Fl(3) is group flashing with three flashes; W is white and 10s is the complete repetition period.')
choices('2e','Uncertain landfall','At landfall, observed lights do not agree with the expected charted pattern. What is the best response?',
 'Treat the position as uncertain, verify it by independent means and call the Master as required',
 ['Alter toward the brightest light to obtain a clearer view','Accept the electronic position without cross-checking','Assume the chart has changed and continue toward the coast'],
 'A mismatch is a reason to reassess the fix and safety margin before closing dangers.',source='watch')
choices('2b','Planning near offshore installations','Which matters belong in a passage appraisal near an offshore wind farm? Select all that apply.',
 ['Current safety-zone information and local notices','Support-vessel traffic and available sea room','Possible effects on radar observations'],['An assumption that every gap between turbines is an approved route'],
 'The route must account for local restrictions, traffic and equipment limitations; a visual gap is not approval for a passage.')
choices('3b','Joining a traffic lane','When joining an IMO-adopted TSS traffic lane from its side, how should the vessel normally join?',
 'At as small an angle to the traffic flow as practicable',['At a heading at right angles in every case','Against the traffic flow until clear of the boundary','By following the separation line'],
 'Rule 10 distinguishes a small-angle side entry from a right-angle crossing.',source='tss')
choices('3b','Heading when crossing','A strong current makes course over ground differ from heading. When crossing an IMO-adopted TSS lane, which should be as nearly as practicable at right angles to the general traffic flow?',
 'The vessel’s heading',['The course over ground in every case','The direction of the tidal stream','The relative bearing of the nearest ship'],
 'Rule 10(c) specifies heading; current can make the resulting ground track oblique.',source='tss')
fields('4b','Resultant ground motion','A vessel heads due north at 10 kn through the water. A steady stream sets due east at 2 kn. Ignore leeway. Calculate true course over ground and speed over ground, to one decimal place.',
 [('Course over ground (degrees true)',math.degrees(math.atan2(2,10)),1),('Speed over ground (kn)',math.hypot(10,2),1)],
 'East and north components are 2 and 10 kn. COG = atan(2/10) = 11.3°; SOG = sqrt(104) = 10.2 kn.')
fields('4e','Counteracting a northerly stream','Required ground track is due east. Speed through water is 13 kn and stream is due north at 5 kn. Ignore leeway. Find true heading to one decimal place and speed made good to one decimal place.',
 [('Heading (degrees true)',90+math.degrees(math.asin(5/13)),1),('Speed made good (kn)',12,1)],
 'The water velocity needs a 5 kn southerly component. East component sqrt(13²−5²)=12; heading = 90°+asin(5/13)=112.6°.')
choices('4d','Starboard leeway','With no current, the required track through the water is 090°T. Expected leeway is 4° to starboard of the heading. Which true heading should be steered?',
 '086°T',['090°T','094°T','004°T'], 'Heading 086° plus 4° starboard leeway gives water track 090°.')
fields('4h','Variation and deviation','The required true heading is 137°. Variation is 5°E and deviation 2°W. Ignore leeway and current. Calculate compass heading in whole degrees.',
 [('Compass heading (degrees)',134,0)],'Compass error = 5°E−2°=3°E. Compass heading = true−east error = 134°.')
choices('4h','Gyro error from a transit','A transit bears 058°T and simultaneously reads 060°G. What is the gyro error?',
 '2°W',['2°E','118°E','No error'], 'True minus gyro = −2°, hence 2° west.')
choices('4i','Changing gyro error','A ship must maintain 100°T. Gyro error changes from 2°E to 4°W. What gyro course is now needed?',
 '104°G',['094°G','098°G','100°G'], 'True = gyro + signed error. With −4° error, gyro = 104°, an increase of 6° from 098°.')
fields('4a','Advancing a DR position','A vessel steers 090°T at 12 kn through the water for 1 hour 30 minutes. Ignore current and leeway. How far east is the DR position advanced?',
 [('Eastward distance (nautical miles)',18,1)],'12 × 1.5 = 18 nautical miles east.')
choices('4a','Advancing a position line','For a running fix in a known tidal stream, which motion should be used to advance the earlier position line to the time of the later observation?',
 'The vessel’s estimated ground displacement between observations',['Only the water-log distance, ignoring the known stream','The movement of the observed shore object','The later compass bearing alone'],
 'Advancement represents vessel movement over the ground, incorporating current and leeway as applicable.')
fields('5b','Plane sailing triangle','A short passage has difference of latitude 36 nautical miles north and departure 48 nautical miles east. Use plane sailing. Find course to one decimal place and distance to one decimal place.',
 [('Course (degrees true)',math.degrees(math.atan2(48,36)),1),('Distance (nautical miles)',60,1)],
 'Distance = sqrt(36²+48²)=60; course = atan(48/36)=53.1°T.')
fields('5b','Parallel sailing distance','A ship travels east along latitude 60°N through 1°30′ of longitude. Use distance = difference of longitude in minutes × cosine(latitude). Find distance to one decimal place.',
 [('Distance (nautical miles)',45,1)],'90 minutes × cos60° = 45 nautical miles.')
fields('5b','Mercator sailing data','For a north-easterly rhumb-line passage, difference of longitude is 160′, difference of meridional parts 120 and difference of latitude 72′. Use tan(course)=DLo/DMP and distance=DLat/cos(course). Find course and distance to one decimal place.',
 [('Course (degrees true)',math.degrees(math.atan2(160,120)),1),('Distance (nautical miles)',120,1)],
 'tan C =160/120, so C=53.1°; cos C=.6 and distance=72/.6=120 nautical miles.')
choices('5c','Arrival across time zones','Departure is 2300 on 8 June at UTC+3. Passage duration is 10 hours. Destination time is UTC−5. What is the local ETA?',
 '0100 on 9 June',['0900 on 9 June','1700 on 8 June','2300 on 8 June'],
 'Departure is 2000 UTC on 8 June; arrival is 0600 UTC on 9 June, or 0100 at UTC−5.')
fields('5c','Required average speed','There are 84 nautical miles remaining and 7 hours until the required arrival time. What average speed over ground is required?',
 [('Required speed (kn)',12,1)],'84 / 7 = 12 kn.')
choices('6a','Taking over the watch','Before accepting the bridge watch, which matters should the relieving OOW understand? Select all that apply.',
 ['Position, planned track and nearby dangers','Traffic, weather and the status of navigation equipment','Standing orders and any specific instructions'],['Only the name of the outgoing OOW'],
 'An effective handover establishes the navigational situation and applicable instructions.',source='watch')
choices('6a','Master on the bridge','The Master arrives on the bridge without announcing a transfer of the con. What should the OOW assume?',
 'The OOW retains watchkeeping responsibility until clearly relieved and this is mutually understood',
 ['Responsibility transfers automatically on the Master entering','The lookout may be dismissed immediately','Bridge records can stop until the Master leaves'],
 'The Master’s presence alone does not constitute an understood transfer of responsibility.',source='watch')
fields('6d','Compass error from azimuth','A celestial observation has already been fully corrected to a true azimuth of 095.5°. The simultaneous compass bearing is 091.0°. Enter compass error as positive for east and negative for west, to one decimal place.',
 [('Signed compass error (degrees)',4.5,1)],'Compass error = true bearing−compass bearing = +4.5°, or 4.5°E.')
choices('6f','Steering failure communication','The rudder no longer follows bridge commands. Which actions belong in the immediate bridge response? Select all that apply.',
 ['Call the Master and advise the engine room','Maintain lookout and assess traffic and navigational danger','Use the ship’s emergency steering and communication procedures'],['Wait for the next routine log entry before reporting'],
 'Steering failure needs immediate coordinated assessment and the established contingency response.',source='watch')
choices('6e','Bridge record timing','Why should the time of a significant course alteration be entered accurately in bridge records?',
 'To allow the vessel’s movements and decisions to be reconstructed reliably',
 ['To replace the need to record position','To prove that no collision risk existed','To avoid checking the next waypoint'],
 'Accurate timing supports navigation monitoring, handover and reconstruction of events.',source='watch')
choices('7a','Ice blink','What is ice blink?', 'A pale reflection from ice on the underside of low cloud',
 ['A reliable AIS identification of every iceberg','A radar signal that always distinguishes ice from rain','The navigation light used by an icebreaker'],
 'Ice blink is an optical indication of ice beyond direct view; it does not establish an exact ice edge.')
choices('7b','Freezing spray precautions','With freezing spray accumulating, which actions should be considered under the Master’s assessment? Select all that apply.',
 ['Adjust course or speed where safe to reduce spray exposure','Monitor the extent of ice accumulation and its stability effects','Control access to exposed decks'],['Send unprotected crew onto an unsafe deck immediately'],
 'Ice accretion calls for reduced exposure, stability awareness and safe working precautions.')
choices('8a','Neap tide alignment','Neap tides generally occur near which lunar phases?', 'First and third quarter',
 ['New and full moon','Only the March equinox','Only the December solstice'], 'Near quarter moon, the solar and lunar tide-producing effects oppose in part, reducing range.')
fields('8b','Overhead clearance reference','A bridge clearance is charted as 30.0 m above HAT. HAT is 4.0 m above chart datum and current tide height is 2.0 m. A vessel’s air draught is 31.0 m. Ignoring all other allowances, find current bridge clearance and clearance above the vessel, to one decimal place.',
 [('Bridge clearance above current water (m)',32,1),('Clearance above vessel (m)',1,1)],
 'Bridge underside is 30+4=34 m above datum. Current clearance=34−2=32 m; above vessel=32−31=1 m.')
fields('8b','Water over a drying rock','A rock has drying height 1.4 m above chart datum. Tide height is 3.9 m. Ignoring wave action, how much water covers the rock?',
 [('Water depth (m)',2.5,1)],'Water depth = tide height−drying height =3.9−1.4=2.5 m.')
fields('9b','Rising-tide curve','Use the supplied training tidal curve. Low water is 0200 at 1.0 m; high water is 0800 at 5.0 m. What is the height at 0400? Give one decimal place.',
 [('Height of tide (m)',1.8,1)],'0400 is 2 hours after LW. The plotted rise fraction is .20; height=1+.20×4=1.8 m.',image='assets/tide-rise-2.svg')
choices('9c','Time to reach a tidal height','Use the supplied training tidal curve. Low water is 0200 at 1.0 m; high water is 0800 at 5.0 m. When does the rising tide first reach 4.2 m?',
 '0600',['0400','0500','0700'], 'Required fraction=(4.2−1)/4=.80; the curve reaches .80 at 4 hours after LW, or 0600.',image='assets/tide-rise-2.svg')
fields('9e','Reduction of a sounding','A sounding is 12.7 m below the water surface after all instrument and transducer corrections. Tide height is 2.3 m above chart datum. Reduce the sounding to chart datum.',
 [('Depth below chart datum (m)',10.4,1)],'12.7−2.3=10.4 m below chart datum.')

start('navigation',3)
choices('1a','Vessel limits in appraisal','Which vessel-specific information should influence passage appraisal? Select all that apply.',
 ['Loaded draught and required under-keel margins','Turning and stopping characteristics','Air draught where overhead restrictions exist'],['The vessel’s paint colour as the primary limiting factor'],
 'Vessel dimensions and manoeuvring characteristics constrain the usable route.')
choices('1a','Contingency planning','Why identify abort points and alternative anchorages while planning?',
 'To prepare safe options if the intended passage cannot be continued', ['To guarantee the voyage will never be delayed','To avoid briefing the bridge team','To permit any anchorage to be used without checking depth'],
 'Contingencies give assessed alternatives when limits or conditions are not met.')
match('1a','Planning and monitoring tasks','Match each task to the most relevant passage-planning stage.',[
 ('Assess the latest weather forecast','Appraisal'),('Mark no-go areas and clearing limits','Planning'),('Set the agreed bridge team for a restricted leg','Execution'),('Compare successive fixes with the planned track','Monitoring')],
 'Information assessment precedes detailed planning; execution implements the plan and monitoring checks its progress.')
choices('2d','Sector light boundary','A sector light changes colour earlier than expected during approach. What should the OOW do?',
 'Check position and the charted sector limits and reassess the safe track', ['Assume the new colour proves the vessel is on the centreline','Use the colour change as a substitute for all position fixing','Continue regardless because sector boundaries cannot change'],
 'Sector indications must be interpreted against charted limits and independent position information.')
choices('2d','Light height and range','In a light description Fl W 10s 25m 15M, what does 15M indicate?',
 'A nominal range of 15 nautical miles',['A light elevation of 15 metres','A period of 15 minutes','A depth of 15 metres at the light'],
 'Capital M denotes the nominal light range in nautical miles; 25m is the charted elevation.')
choices('2c','Position-line geometry','Which pair of intersecting position lines generally has the least favourable fixing geometry?',
 'Two lines crossing at only 5°',['Two lines crossing at 85°','Two lines crossing at 90°','Two lines crossing at 95°'],
 'Nearly parallel lines magnify the positional effect of small observation errors.')
choices('2e','Unexpected landfall depth','An independently checked echo sounding is substantially shallower than the passage plan predicts near landfall. What is the prudent response?',
 'Reassess position, tide and clearance immediately and call the Master as required', ['Reduce the planned safety contour to make the alarm stop','Assume the seabed must be deeper ahead','Increase speed so the discrepancy lasts less time'],
 'An unexplained depth discrepancy can indicate a position or datum error and requires immediate assessment.',source='watch')
choices('3c','Routeing guidance use','Why consult a Mariners’ Routeing Guide during appraisal?',
 'To identify routeing measures, reporting arrangements and navigational considerations for the area',
 ['To replace the corrected largest-scale charts','To guarantee right of way in every traffic lane','To remove the need for local navigational warnings'],
 'A routeing guide supplements charts and other current information; it is not a substitute for them.')
choices('3b','Separation zone','When using an IMO-adopted TSS, what is the normal requirement concerning its separation line or zone?',
 'Keep clear so far as practicable, subject to the exceptions in Rule 10',
 ['Use it as an overtaking lane','Anchor there whenever a lane is busy','Navigate along it to reduce current effects'],
 'Rule 10 requires vessels using a scheme to keep clear of the separating measure so far as practicable.',source='tss')
fields('4b','Set and drift from a fix','After one hour, the vessel’s observed position is 3 nautical miles east and 4 nautical miles north of its DR position. Assume the difference is entirely due to a steady stream. Calculate set in degrees true and drift in knots, to one decimal place.',
 [('Set (degrees true)',math.degrees(math.atan2(3,4)),1),('Drift (kn)',5,1)],
 'Stream displacement is 3 east and 4 north in one hour; drift=5 kn and set=atan(3/4)=36.9°T.')
fields('4e','Counteracting an easterly stream','A vessel makes 10 kn through the water. Stream sets east at 6 kn. Ignore leeway. Find heading to make a due-north ground track and the speed made good, to one decimal place.',
 [('Heading (degrees true)',360-math.degrees(math.asin(.6)),1),('Speed made good (kn)',8,1)],
 'A 6 kn westward water component cancels the stream; north component=sqrt(100−36)=8. Heading=360−asin(.6)=323.1°T.')
fields('4f','Opposing current passage time','The heading and intended track are due east. Speed through water is 15 kn and current sets due west at 2 kn. Ignore leeway. How many hours are required for a 65 nautical mile leg?',
 [('Passage time (hours)',5,1)],'Ground speed=15−2=13 kn; time=65/13=5 hours.')
choices('4c','Leeway direction','A vessel heads 225°T with 3° leeway to starboard and no current. What is the track through the water?',
 '228°T',['222°T','225°T','048°T'],'Starboard leeway adds 3° clockwise to the heading: 228°T.')
fields('4h','Compass to true','Compass heading is 270°. Variation is 8°W and deviation 3°E. What is true heading in whole degrees?',
 [('True heading (degrees)',265,0)],'Signed compass error=−8+3=−5°. True=270−5=265°.')
choices('4a','Relative bearing','A vessel’s true heading is 350°. A fixed object is observed at relative bearing 030° clockwise from the bow. What is its true bearing?',
 '020°T',['030°T','320°T','350°T'],'350+30=380°, reduced to 020°T.')
fields('4a','Chartwork coordinates','In the supplied training grid, O is the start and P is 8 nautical miles east and 6 nautical miles north of O. Find bearing of P from O and distance OP to one decimal place.',
 [('Bearing (degrees true)',math.degrees(math.atan2(8,6)),1),('Distance (nautical miles)',10,1)],
 'Bearing=atan(8/6)=53.1°T; distance=sqrt(8²+6²)=10 nm.',image='assets/chartwork-grid.svg')
fields('4g','Speed to maintain the plan','At 0915, the planned waypoint is 27 nautical miles away. It must be reached at 1130. What average speed made good is required?',
 [('Required speed (kn)',12,1)],'Time available=2.25 hours; 27/2.25=12 kn.')
choices('5a','Mercator distance scale','When measuring a short distance on a Mercator chart, which latitude scale should normally be used?',
 'The latitude scale near the latitude of the measured distance', ['The longitude scale regardless of latitude','Only the equatorial latitude scale','The scale from an unrelated chart'],
 'Mercator scale changes with latitude; local latitude scale is used for a nearby distance.')
fields('5b','Crossing the date line along a parallel','A vessel follows latitude 60°N eastwards from 179°E to 179°W across 180°. Using parallel sailing, find the shorter eastward distance to one decimal place.',
 [('Distance (nautical miles)',60,1)],'Shorter longitude difference is 2°=120′. Distance=120 cos60°=60 nm.')
fields('5b','North-easterly plane sailing','Using plane sailing, a course of 060°T produces 60 nautical miles of northing. Find distance and departure to one decimal place.',
 [('Distance (nautical miles)',120,1),('Departure east (nautical miles)',120*math.sin(math.radians(60)),1)],
 'DLat=D cosC; D=60/.5=120 nm. Departure=120 sin60°=103.9 nm.')
fields('5b','Mercator sailing across 180°','A north-easterly passage runs from longitude 179°E to 175°W by the shorter route. DMP is 480 and DLat is 300′ north. Use tan C=DLo/DMP and D=DLat/cos C. Calculate course and distance to one decimal place.',
 [('Course (degrees true)',math.degrees(math.atan2(360,480)),1),('Distance (nautical miles)',375,1)],
 'Eastward DLo=6°=360′. C=atan(.75)=36.9°; distance=300/.8=375 nm.')
choices('5c','ETA over a month end','At 2300 UTC on 31 July, 54 nautical miles remain at a steady 9 kn over ground. What is the ETA?',
 '0500 UTC on 1 August',['0500 UTC on 31 July','0400 UTC on 1 August','0600 UTC on 1 August'],
 '54/9=6 hours; six hours after 2300 on 31 July is 0500 on 1 August.')
choices('6a','Unfit relieving officer','The relieving officer appears too fatigued to keep a safe watch. What should the outgoing OOW do?',
 'Retain the watch and inform the Master rather than hand over to an unfit officer', ['Hand over because the watch period has ended','Let the lookout take charge of navigation','Leave the bridge and record the concern later'],
 'The watch must not be handed to a person apparently incapable of carrying it out effectively.',source='watch')
choices('6a','Sole lookout conditions','For an OOW acting as sole lookout in daylight, which conditions are relevant? Select all that apply.',
 ['A careful assessment establishes that it is safe','Relevant traffic, weather, visibility and bridge workload are considered','Assistance can be summoned immediately'],['Daylight makes a separate risk assessment unnecessary'],
 'Daylight sole lookout is conditional on an assessment and immediate availability of assistance.',source='watch')
choices('6d','Gyro error from corrected amplitude','An amplitude observation has been fully corrected to a true bearing of 268°. The simultaneous gyro bearing is 270°. What is gyro error?',
 '2°W',['2°E','538°E','No error'],'True−gyro=−2°, meaning 2°W.')
choices('6f','Total power failure','The bridge loses main electrical power at night. Which actions are appropriate parts of the immediate response? Select all that apply.',
 ['Call the Master and communicate with the engine room','Establish which steering and navigation services remain available','Maintain lookout and assess nearby traffic and hazards'],['Assume the vessel will keep its original track indefinitely'],
 'The bridge must establish the ship’s actual condition and coordinate the blackout response.',source='watch')
choices('6c','Steering check meaning','What makes a steering operational check meaningful?',
 'Confirming actual rudder response and required control and communication arrangements', ['Watching only the wheel move without checking rudder response','Checking only that the steering switch is labelled','Assuming the previous voyage test remains sufficient'],
 'A functional check verifies response and relevant arrangements, not merely control movement.',source='watch')
choices('7c','Radar limitations near ice','Which statement about radar detection of ice is correct?',
 'Small or low ice may be difficult to detect, so radar must be supported by other information and lookout', ['Every iceberg gives a strong echo at the same range','AIS identifies all floating ice','Rain clutter elimination guarantees ice detection'],
 'Low profile, sea state and reflectivity can limit radar detection; absence of an echo is not proof of no ice.')
choices('7c','Using ice reports','A ship receives a recent ice-edge report. How should it be used?',
 'Together with its observation time, expected ice movement, current reports and actual conditions', ['As an exact stationary boundary for the rest of the voyage','As permission to dispense with the lookout','As evidence that the area outside the reported line is always ice-free'],
 'Ice moves and information ages; report timing and corroborating observations matter.')
match('8b','Reference levels and heights','Match each abbreviation or term to its meaning.',[
 ('HAT','Highest astronomical tide under average meteorological conditions'),('LAT','Lowest astronomical tide under average meteorological conditions'),('Drying height','Height above chart datum of a feature that dries'),('Air draught','Height from current waterline to the vessel’s highest relevant point')],
 'Tidal reference levels and vessel heights use different origins and must not be interchanged.')
fields('8b','Tidal range','Predicted high water is 5.4 m and the associated low water is 1.2 m, on the same datum. Find the tidal range.',
 [('Range (m)',4.2,1)],'Range=5.4−1.2=4.2 m.')
fields('8b','Allowing for squat','The actual water depth is 9.1 m and the ship’s static draught is 8.1 m. Squat adds 0.4 m to draught. Ignore all other effects. Calculate the resulting under-keel clearance.',
 [('Under-keel clearance (m)',.6,1)],'UKC=9.1−8.1−.4=.6 m.')
fields('9b','Falling-tide interpolation','Use the supplied falling-tide training curve. High water is 0930 at 6.0 m; low water is 1530 at 2.0 m. Read the curve by straight-line interpolation between its plotted points. What is the height at 1200?',
 [('Height of tide (m)',4.5,1)],'At 2.5 hours after HW, fall fraction interpolates from .25 at hour 2 to .50 at hour 3: .375. Height=6−4×.375=4.5 m.',image='assets/tide-fall-3.svg')
choices('9c','Latest tide-window time','Use the falling-tide training curve. High water is 0930 at 6.0 m; low water is 1530 at 2.0 m. During this falling tide, when does the height reach the required minimum of 2.8 m?',
 '1330',['1130','1230','1430'], 'Fall fraction=(6−2.8)/4=.8, reached four hours after HW at 1330.',image='assets/tide-fall-3.svg')
choices('9d','Prediction and observed level','Actual sea level at a port is lower than the prediction during unusual weather. What should the OOW do?',
 'Use reliable observed information and reassess the planned depth margins', ['Treat the prediction as an exact guarantee','Ignore the discrepancy if the tide table is current','Add the discrepancy to draught with the wrong sign automatically'],
 'Predictions describe astronomical tides; meteorological effects and observations must inform clearance assessments.')

start('navigation',4)
choices('1a','Extent of a passage plan','What is the intended extent of an appropriate voyage passage plan?',
 'The complete voyage from berth to berth, including pilotage legs', ['Only the open-sea part outside pilotage waters','Only the departure manoeuvre','Only waypoints that are visible on radar'],
 'Appraisal and planning cover the whole intended voyage, including departures and approaches.')
choices('1a','Under-keel appraisal','Which matters can affect the depth margin used in passage appraisal? Select all that apply.',
 ['Tide and uncertainty in actual water level','Squat and vessel motion','Accuracy of charted depth and position'],['The assumption that static draught is the only relevant factor'],
 'Clearance appraisal considers dynamic vessel effects and uncertainty as well as static draught.')
choices('1a','Weather-driven alteration','Conditions make a planned exposed leg unsuitable. Which response best follows passage-planning principles?',
 'Reappraise alternatives, amend the plan with the Master and brief those implementing it',
 ['Choose an unassessed shortcut on the plotter','Continue because the original route was approved','Delete the old route so no record of the decision remains'],
 'A plan is reassessed when the underlying conditions change.')
choices('2d','Chart information currency','Which is the appropriate preparation for a chart needed on passage?',
 'Check the appropriate edition and apply relevant current corrections and warnings', ['Assume the chart is current because it was purchased recently','Apply only corrections to the destination harbour','Rely on an old plotted track instead of checking chart information'],
 'Edition status, corrections and current warnings together affect chart reliability.')
choices('2c','A buoy as the only reference','Why is an isolated buoy generally weaker than a fixed shore object as the sole reference for a position fix?',
 'It can be displaced from its charted position', ['Its colour is always invisible in daylight','Its charted position changes every second by definition','It cannot have a radar reflector'],
 'A floating aid can be off station; independent checks are needed.')
choices('2e','A missing expected light','A charted light is not seen at landfall. What is the appropriate interpretation?',
 'The absence needs investigation; position, visibility, range and light status may all be relevant',
 ['The vessel must be outside the light’s nominal range','The danger marked by the light has disappeared','The coast must be clear if no light is seen'],
 'Failure to see an expected aid is not a unique position solution and does not remove the danger.')
choices('2b','Radar near turbines','Which passage-planning precaution is appropriate where wind turbines may affect radar observations?',
 'Allow for possible clutter or false echoes and plan suitable independent checks', ['Treat every echo in the wind farm as a ship','Switch radar off throughout the passage','Use turbine echoes as the only position reference'],
 'Equipment limitations should be anticipated and cross-checks planned.')
choices('3b','Other COLREG duties in a TSS','A vessel is proceeding correctly in its TSS lane. What does Rule 10 imply about its other COLREG obligations?',
 'They still apply; compliance with Rule 10 gives no general exemption', ['All ships crossing must keep clear regardless of other rules','The lane user can maintain speed regardless of collision risk','Lookout obligations cease inside the lane'],
 'Rule 10(a) expressly does not relieve a vessel of obligations under other rules.',source='tss')
match('3b','Different TSS manoeuvres','Match each manoeuvre with the normal Rule 10 approach.',[
 ('Crossing a traffic lane','Heading as nearly at right angles to traffic flow as practicable'),('Joining from a lane’s side','Join at as small an angle to traffic flow as practicable'),('Proceeding within a lane','Follow the general direction of flow in the appropriate lane')],
 'Crossing, joining and lane-following have different requirements.',source='tss')
fields('4b','Westerly heading with southerly stream','A vessel heads 270°T at 12 kn through the water; stream sets 180°T at 5 kn. Ignore leeway. Find true course and speed over ground to one decimal place.',
 [('Course over ground (degrees true)',270-math.degrees(math.atan2(5,12)),1),('Speed over ground (kn)',13,1)],
 'Ground vector is 12 west and 5 south: COG=270−atan(5/12)=247.4°; SOG=13 kn.')
fields('4e','Making good east','With 10 kn through the water and a 6 kn northerly stream, find the heading required to make good due east and the speed made good. Ignore leeway; give one decimal place.',
 [('Heading (degrees true)',90+math.degrees(math.asin(.6)),1),('Speed made good (kn)',8,1)],
 'Water vector must be 8 east and 6 south; heading=126.9°T, ground speed=8 kn.')
choices('4d','Port leeway','Heading is 045°T and leeway is 4° to port. With no current, what is track through the water?',
 '041°T',['049°T','045°T','221°T'],'Port leeway is anticlockwise from heading:45−4=41°T.')
fields('4h','Compass course across north','Required true heading is 358°. Variation is 2°W and deviation 5°W. Calculate compass heading in whole degrees, in the range 000° to 359°.',
 [('Compass heading (degrees)',5,0)],'Total error=7°W; compass=358+7=365°, reduced to005°.')
choices('4h','Gyro error across north','A transit bears 002°T and simultaneously reads 355°G. What is gyro error?',
 '7°E',['7°W','353°E','3°W'],'002°T is equivalent to362°;362−355=+7°, or7°E.')
choices('4i','Maintaining true course','Gyro error changes from 3°E to 1°E. What change to the gyro-course order maintains the same true heading?',
 'Increase the gyro-course order by 2°',['Decrease the gyro-course order by 2°','No change is required','Increase the gyro-course order by 4°'],
 'Gyro=true−east error. A reduction of east error by2° requires gyro order to increase2°.')
choices('4a','Observation timing','Why should ranges or bearings used for a fix be taken as nearly simultaneously as practicable?',
 'The vessel moves between observations, potentially displacing the position lines', ['All instruments become inaccurate after one second','Shore objects move at the vessel’s speed','Simultaneous observations remove all chart error'],
 'Time separation causes lines to refer to different vessel positions unless properly advanced.')
choices('4a','Running-fix uncertainty','Which factor particularly affects a running fix compared with a simultaneous fix?',
 'Uncertainty in the vessel’s ground movement between the observations', ['The colour of the plotting pencil alone','The shore object being fixed to land','The fact that bearings use angular units'],
 'A running fix adds an estimated advancement between observations, introducing motion uncertainty.')
fields('5b','Westward parallel passage','A ship follows latitude 30°N westwards through 1° of longitude. Using parallel sailing, find distance to one decimal place.',
 [('Distance (nautical miles)',60*math.cos(math.radians(30)),1)],'D=60 cos30°=51.96 nm, rounded52.0 nm.')
fields('5b','South-westerly plane sailing','A short plane-sailing leg has 30 nautical miles southing and 40 nautical miles westward departure. Calculate true course and distance to one decimal place.',
 [('Course (degrees true)',180+math.degrees(math.atan2(40,30)),1),('Distance (nautical miles)',50,1)],
 'South-west quadrant:course=180+atan(40/30)=233.1°T;distance=50 nm.')
fields('5b','South-easterly Mercator passage','For a south-easterly rhumb line, DLo is 180′ east, DMP is 240 and DLat is 192′ south. Use tan(quadrantal course)=DLo/DMP. Find true course and distance to one decimal place.',
 [('Course (degrees true)',180-math.degrees(math.atan2(180,240)),1),('Distance (nautical miles)',240,1)],
 'Quadrantal course=36.87° east of south;true course143.1°.Distance=192/.8=240 nm.')
choices('5a','Rhumb-line property','Which property distinguishes a rhumb line on a Mercator chart?',
 'It crosses meridians at a constant angle and is plotted as a straight line', ['It is always shorter than the great-circle route','It crosses every parallel at a different heading','It can exist only along the equator'],
 'A rhumb line has constant true direction; a great circle is the shortest spherical route and normally changes direction.')
choices('5c','Half-hour time zone','Departure is 0330 on 12 June at UTC+5 hours 30 minutes. Passage duration is 12 hours. Arrival port is UTC−3. What is local ETA?',
 '0700 on 12 June',['0700 on 13 June','1800 on 12 June','2200 on 11 June'],
 'Departure=2200 UTC11 June;arrival=1000 UTC12 June;UTC−3 gives0700 on12 June.')
choices('6b','Developing restricted visibility','Visibility deteriorates unexpectedly. Which bridge actions are appropriate? Select all that apply.',
 ['Call the Master under standing orders','Reassess safe speed and collision risk','Ensure an effective lookout and apply the required restricted-visibility procedures'],['Wait for a close-quarters situation before acting'],
 'Restricted visibility requires prompt assessment, the appropriate bridge team and applicable procedures.',source='watch')
choices('6f','Closed-loop communication','Which exchange best illustrates closed-loop communication of an engine order?',
 'The receiver repeats the order and the sender checks that the repeat is correct', ['The sender assumes an unheard order was accepted','The receiver says nothing and changes an unrelated control','A third person records the order after the watch ends'],
 'Repeat-back and verification reduce misunderstanding during routine and emergency communications.',source='watch')
choices('6d','Compass check using Polaris','A Polaris observation has already been corrected to true bearing 359.2°. Gyro bearing is001.2°. What is gyro error?',
 '2.0°W',['2.0°E','358.0°E','No error'], 'Treat359.2° as−0.8° near north;true−gyro=−2.0°.')
choices('6e','Correcting a bridge record','A bridge-log entry contains an error. What is the appropriate general approach?',
 'Make a traceable correction under the ship’s recordkeeping procedure', ['Erase the original entry so the alteration cannot be seen','Rewrite the entire page without a correction record','Leave an identified material error uncorrected'],
 'Records should retain an auditable history of corrections, with the appropriate attribution and timing.',source='watch')
choices('6a','Relief during a manoeuvre','An alteration to avoid traffic is in progress at watch-change time. What is the normal handover approach unless the Master directs otherwise?',
 'Complete the action and establish a clear situation before transferring the watch', ['Transfer immediately regardless of the developing manoeuvre','Let the incoming OOW infer the alteration without a briefing','Leave the bridge as soon as the scheduled time arrives'],
 'A manoeuvre or other avoidance action should normally be completed before the watch is handed over.',source='watch')
choices('7a','Interpreting a sign of ice','A pale glow is observed under low cloud toward the horizon in an ice region. What does this indicate?',
 'Possible ice blink requiring corroboration and caution', ['A guaranteed ice-free channel','The exact range of an iceberg','Proof that radar settings are correct'],
 'An optical indication suggests possible nearby ice but does not establish its precise location or extent.')
choices('7b','Upper-deck ice accretion','Why is accumulating ice on upper decks a concern for the bridge team?',
 'It adds high weight and can adversely affect stability as well as safe deck access', ['It always lowers the centre of gravity','It removes the need to assess wind effects','It guarantees more freeboard'],
 'Ice high in the vessel raises weight and potentially KG while also creating operational hazards.')
choices('8a','Astronomical range and actual tide','Which statement correctly distinguishes spring-tide prediction from actual observed water level?',
 'Spring tides generally have larger astronomical range, but weather can still modify the observed level',
 ['Spring tides guarantee the largest observed water level on every occasion','Weather has no effect during a spring tide','The word spring refers only to the season'],
 'Sun–Moon alignment affects astronomical range; meteorological effects remain possible.')
fields('8b','Maximum tide for an overhead passage','A bridge has charted clearance26.0 m above HAT. HAT is4.0 m above datum. Air draught is27.0 m and required overhead margin is1.0 m. Ignoring other effects, what is the greatest tide height permitting this margin?',
 [('Maximum tide height above datum (m)',2,1)],'Bridge underside is30 m above datum;30−tide−27>=1, so tide<=2.0 m.')
choices('8b','Air-draught origin','For an overhead-clearance calculation, air draught is measured from:',
 'The vessel’s current waterline to its highest relevant point', ['The keel to the top of the mast','Chart datum to the bridge underside','The sea bed to the masthead'],
 'Air draught is the above-water height of the vessel; it is not keel-to-mast height.')
fields('9b','Tide over midnight','Use the supplied rising-tide training curve. Low water is2330 on12 September at0.8 m; high water is0530 on13 September at4.8 m. Find height at0130 on13 September, to one decimal place.',
 [('Height of tide (m)',1.6,1)],'0130 is2 hours after LW;fraction=.20.Height=.8+4×.20=1.6 m.',image='assets/tide-rise-2.svg')
choices('9c','Required height after midnight','Use the supplied rising-tide training curve. Low water is2330 at0.8 m; high water six hours later is4.8 m. At what time next day does the rising tide first reach4.0 m?',
 '0330',['0130','0230','0430'],'Fraction=(4−.8)/4=.80;four hours after2330 is0330 next day.',image='assets/tide-rise-2.svg')
fields('9e','A drying depth from sounding','A corrected sounding shows0.9 m of water above a feature when tide height is1.5 m above chart datum. Find the feature’s drying height, to one decimal place.',
 [('Drying height above chart datum (m)',.6,1)],'Reduced depth=.9−1.5=−.6 m, meaning a drying height of.6 m above datum.')

start('stability',2)
fields('1a','Density and mass','A liquid cargo occupies800 m³ and has density0.90 t/m³. Calculate its mass in tonnes.',
 [('Cargo mass (t)',720,1)],'Mass=density×volume=.90×800=720 t.')
fields('1d','Hydrostatic interpolation','Training hydrostatic data at the stated water density give displacement8,000 t at6.0 m mean draught and10,000 t at7.0 m. Assume linear interpolation over this interval. Find displacement at6.4 m.',
 [('Displacement (t)',8800,0)],'8000+.4×(10000−8000)=8800 t.')
fields('1d','TPC at dock-water density','TPC is18.0 t/cm in seawater of density1.025 t/m³. At the same waterplane area, calculate TPC in dock water of density1.010 t/m³, to two decimal places.',
 [('Dock-water TPC (t/cm)',18*1.010/1.025,2)],'TPC scales with density at constant waterplane area:18×1.010/1.025=17.74 t/cm.')
fields('1h','Weight for a small immersion','TPC remains constant at20 t/cm during loading. What weight can be loaded to increase draught by12 cm?',
 [('Weight to load (t)',240,0)],'Weight=TPC×centimetres=20×12=240 t.')
fields('1c','Calculating fresh water allowance','At the relevant displacement of10,000 t, salt-water TPC is25 t/cm. Use FWA(mm)=displacement/(4×TPC). Calculate FWA.',
 [('Fresh water allowance (mm)',100,0)],'FWA=10000/(4×25)=100 mm.')
fields('1c','Calculating dock water allowance','FWA is180 mm. Dock-water density is1.015 t/m³ and seawater density1.025 t/m³. Use DWA=FWA×(1.025−dock density)/.025. Calculate DWA.',
 [('Dock water allowance (mm)',72,0)],'DWA=180×.010/.025=72 mm.')
fields('1g','Block coefficient from dimensions','Underwater volume is16,800 m³, length between perpendiculars150 m, moulded breadth20 m and draught8 m. Calculate block coefficient to two decimal places.',
 [('Block coefficient',.7,2)],'CB=volume/(L×B×draught)=16800/(150×20×8)=.70.')
fields('1k','Loading with dock-water allowance','Summer salt-water draught is8.00 m. DWA is0.12 m. Present draught in dock water is7.80 m and dock-water TPC stays18 t/cm. Ignoring voyage consumption and trim, calculate maximum additional cargo to the corresponding dock-water load limit.',
 [('Additional cargo (t)',576,0)],'Permitted dock-water draught=8+.12=8.12 m;increase=.32 m=32 cm;cargo=32×18=576 t.')
match('2c','Initial equilibrium conditions','Match the initial transverse condition to its metacentric relationship.',[
 ('Stable','M above G: positive GM'),('Neutral','M and G coincide: zero GM'),('Unstable','M below G: negative GM')],
 'Initial stability depends on the signed separation of M and G.')
fields('2k','Effective GM','KM is8.30 m and KG6.80 m. Free-surface correction is0.15 m. Calculate effective GM to two decimal places.',
 [('Effective GM (m)',1.35,2)],'Effective GM=KM−KG−FSC=8.30−6.80−.15=1.35 m.')
fields('2b','Righting moment','Displacement is7,500 t and GZ at the specified heel angle is0.42 m. Calculate moment of statical stability in tonne-metres.',
 [('Moment (tonne-metres)',3150,0)],'Moment=displacement×GZ=7500×.42=3150 tonne-metres.')
fields('2i','A vertical shift within the ship','On an8,000 t vessel,100 t is moved vertically from2.0 m to10.0 m above keel. Displacement is unchanged. Calculate the rise of the ship’s G.',
 [('Rise of G (m)',.1,2)],'GG=weight×vertical distance/displacement=100×8/8000=.10 m.')
fields('2k','KG after loading high cargo','Initial displacement is6,000 t at KG5.00 m. Load800 t at KG12.00 m. Ignoring free-surface effects, calculate final KG to two decimal places.',
 [('Final KG (m)',(6000*5+800*12)/6800,2)],'Final vertical moment=30000+9600=39600 tm;final displacement6800 t;KG=5.8235 m, rounded5.82 m.')
fields('2k','KG after discharging high cargo','A vessel displaces10,000 t at KG6.00 m. Discharge400 t from KG10.00 m. Calculate final KG to two decimal places.',
 [('Final KG (m)',(10000*6-400*10)/9600,2)],'Remaining moment=60000−4000=56000 tm;displacement9600 t;KG=5.8333 m, rounded5.83 m.')
fields('2i','Suspending an onboard weight','A100 t onboard weight is lifted clear of its support at KG2.0 m and hangs freely from a crane suspension point14.0 m above keel. Vessel displacement remains6,000 t. Find the virtual rise of the ship’s G.',
 [('Virtual rise of G (m)',.2,2)],'Once freely suspended, the load acts at its point of suspension. Rise=100×(14−2)/6000=.20 m.')
fields('2m','List from a transverse shift','A vessel of displacement12,000 t has effective GM1.00 m. A200 t weight shifts6.0 m transversely from the centreline. Assume small-angle theory and unchanged GM. Calculate the resulting angle of list to one decimal place.',
 [('Angle of list (degrees)',math.degrees(math.atan(200*6/(12000*1))),1)],
 'tan(list)=w×d/(displacement×GM)=1200/12000=.1;list=5.7°.')
choices('2r','Longitudinal tank division','A rectangular slack tank is divided by an effective centreline longitudinal bulkhead into two equal, unconnected slack tanks. At equal liquid density and length, the total free-surface moment becomes what fraction of the undivided value?',
 'One quarter',['One half','The same','Twice'],
 'FSM is proportional to length×breadth³. Two tanks of half breadth give2×(1/2)³=1/4 of the original moment.')
fields('2e','Reading a stability curve','Use the supplied training GZ curve. Read the angle of maximum GZ and the angle where positive stability ends. Give whole degrees.',
 [('Angle of maximum GZ (degrees)',35,0),('Angle of vanishing stability (degrees)',70,0)],
 'The plotted maximum is at35° and the positive curve returns to zero at70°.',image='assets/gz-paper-2.svg')
fields('3a','Arithmetic mean draught','Forward draught is4.20 m and aft draught5.00 m. Calculate arithmetic mean draught.',
 [('Arithmetic mean draught (m)',4.6,2)],'AMD=(4.20+5.00)/2=4.60 m.')
fields('3b','True mean draught at LCF','Forward draught is4.50 m and aft draught5.50 m over100 m LBP. LCF lies10 m aft of amidships. Assume a straight waterline and take true mean draught as draught at LCF. Calculate it to two decimal places.',
 [('True mean draught (m)',5.1,2)],'LCF is60 m aft of FP;draught there=4.50+(60/100)×1.00=5.10 m.')
fields('3a','A trimming moment','A250 t weight shifts20 m longitudinally. Calculate the magnitude of its trimming moment.',
 [('Trimming moment (tonne-metres)',5000,0)],'Moment=250×20=5000 tonne-metres.')
fields('3c','Change of trim from moment','A trimming moment of5,000 tonne-metres acts on a vessel with constant MCTC200 tonne-metres per centimetre. Calculate change of trim in centimetres.',
 [('Change of trim (cm)',25,1)],'Change of trim=5000/200=25 cm.')
fields('3e','Correcting stern trim','A vessel is trimmed0.40 m by the stern. MCTC stays150 tonne-metres/cm. What weight must be moved60 m forward to remove the trim, with displacement unchanged?',
 [('Weight to move (t)',100,0)],'Moment needed=40×150=6000 tm;weight=6000/60=100 t, moved forward.')
fields('3c','Draughts after an off-centre load','A vessel is initially on even keel at5.00 m. LBP120 m;LCF amidships;TPC20 t/cm;MCTC180 tonne-metres/cm, all constant. Load240 t at30 m aft of LCF. Find final forward and aft draughts to two decimal places.',
 [('Final forward draught (m)',4.92,2),('Final aft draught (m)',5.32,2)],
 'Parallel sinkage=240/20=12 cm. Stern trim=240×30/180=40 cm, split20 cm at each end. F=5+.12−.20=4.92;A=5+.12+.20=5.32.')
fields('3d','Changing an existing trim','Forward draught is5.00 m and aft draught5.40 m. LCF is amidships and MCTC stays200 tonne-metres/cm. Shift200 t from20 m aft of LCF to20 m forward. Find final draughts to two decimal places.',
 [('Final forward draught (m)',5.2,2),('Final aft draught (m)',5.2,2)],
 'Forward moment=200×40=8000 tm;trim change40 cm by head. Each end changes20 cm;F5.20,A5.20. No parallel change for an onboard shift.')
choices('4b','Enclosed-space casualty','A person collapses inside an enclosed space. Which immediate actions are appropriate? Select all that apply.',
 ['Raise the alarm and summon the trained rescue response','Prevent an unplanned, unprotected entry','Follow the ship’s enclosed-space rescue procedure'],['Enter immediately without equipment because the casualty is visible'],
 'A spontaneous unprotected rescue can create further casualties; summon and prepare an organised response.',source='enclosed')
choices('4a','Mooring-line hazard','A mooring line is heavily loaded during a rising tide. What should the deck watch do?',
 'Keep people clear of hazardous line paths and arrange controlled adjustment under the ship’s procedures', ['Step across the tensioned line to inspect it','Stand in a bight so the line can be eased quickly','Release all lines simultaneously without coordination'],
 'Tensioned lines and changing leads are hazardous; adjustment must be controlled and people kept clear.')
choices('4b','Hot-work permit','What is the purpose of a hot-work permit system?',
 'To verify assessed hazards, isolations, precautions and authorisation before the work proceeds',
 ['To replace the risk assessment completely','To permit welding in any tank without testing','To remove the need for fire precautions once signed'],
 'A permit provides controlled authorisation with defined conditions; it does not eliminate changing hazards.')
match('4d','Integrity and closures','Match each description to its meaning.',[
 ('Watertight','Prevents passage of water in either direction under the designed head'),('Weathertight','Prevents water penetration in the sea conditions for which the closure is designed'),('Heavy-weather preparation','Check and secure the required closures before exposure increases')],
 'Watertight and weathertight are different performance requirements; correct closures must be maintained.')
choices('5a','Bunkering preparation','Which checks are appropriate before starting fuel transfer? Select all that apply.',
 ['Agree communication and the emergency stop procedure','Confirm receiving tanks, available capacity and valve alignment','Arrange spill-prevention and containment measures'],['Begin at maximum rate before confirming the receiving tank'],
 'Transfer must begin only after receiving capacity, communication and spill controls have been checked.')
choices('6a','Garbage annex','Which MARPOL Annex deals with pollution by garbage?', 'Annex V',
 ['Annex I','Annex II','Annex IV'],'Annex V concerns garbage;Annex I oil,II noxious liquid substances in bulk andIV sewage.',source='marpol')
choices('5b','Packaged dangerous goods','Before handling packaged dangerous goods, which information or controls should be checked? Select all that apply.',
 ['Cargo identity, markings and relevant dangerous-goods documentation','Stowage, segregation and securing requirements','Applicable emergency information and protective measures'],['Identify an unknown substance by smelling it closely'],
 'Cargo identification, approved stowage/segregation and emergency information guide safe handling.')
choices('6b','Purpose of the safety management system','Which statement best describes a safety management system under the ISM Code?',
 'A structured system for safe ship operations and pollution prevention with defined responsibilities and procedures',
 ['A commercial schedule that replaces the Master’s judgement','An optional list used only after an accident','A document that removes the need for drills'],
 'The ISM framework organises responsibilities and safeguards for safety and environmental protection.',source='ism')
choices('6d','Normal minimum rest','For an adult seafarer subject to the UK normal minimum-rest rules, with no authorised exception or emergency, which minimum pair applies?',
 '10 hours in any24 hours and77 hours in any7 days',['8 hours in any24 hours and56 hours in any7 days','12 hours in any24 hours and60 hours in any7 days','6 hours in any24 hours and72 hours in any7 days'],
 'The normal UK regime requires at least10 hours rest in any24 hours and77 in any7 days.',source='mlc')
match('6c','M-notice functions','Match each notice series to its general function.',[
 ('MSN','Conveys mandatory requirements where specified under legislation'),('MGN','Gives marine safety or related guidance'),('MIN','Gives information commonly limited to a particular time or audience')],
 'The notice series have different functions;the legal effect depends on the notice and enabling legislation.',source='notices')

start('stability',3)
choices('1b','Law of flotation','For a freely floating vessel in equilibrium, which statement is correct?',
 'The vessel’s weight equals the weight of the water it displaces', ['The vessel’s volume always equals its mass numerically','The ship must have neutral transverse stability','The water displaced has zero weight'],
 'Buoyancy balances the vessel’s weight in floating equilibrium.')
fields('1g','Waterplane coefficient','Waterplane area is1,800 m². Length is100 m and breadth24 m for this coefficient calculation. Find waterplane coefficient to two decimal places.',
 [('Waterplane coefficient',.75,2)],'CW=Awp/(L×B)=1800/(100×24)=.75.')
fields('1a','Displacement volume','A vessel displaces8,200 t in seawater of density1.025 t/m³. Calculate displaced volume in cubic metres.',
 [('Displaced volume (m³)',8000,0)],'Volume=mass/density=8200/1.025=8000 m³.')
fields('1e','Large draught change','At the relevant density, training hydrostatic data give6,000 t at5.0 m,8,000 t at6.0 m and10,400 t at7.0 m. Interpolate linearly within each interval. From5.0 m initially, what cargo mass raises mean draught to6.5 m? Ignore other weight changes.',
 [('Cargo mass to load (t)',3200,0)],'Final displacement=8000+.5×2400=9200 t;cargo=9200−6000=3200 t. Use displacement data across the large draught change.')
choices('1b','Moving to less-dense water','A vessel moves into less-dense water without changing weight. What must happen to displaced volume?',
 'It increases so the weight of displaced water still equals the vessel’s weight', ['It decreases because the ship has lost mass','It stays fixed regardless of density','It becomes equal to deadweight'],
 'At fixed mass,displaced volume=mass/density,so reducing density increases volume.')
fields('1c','Fresh-water immersion allowance','Displacement is14,400 t and salt-water TPC30 t/cm. Use FWA(mm)=displacement/(4×TPC). Calculate FWA.',
 [('FWA (mm)',120,0)],'14400/(4×30)=120 mm.')
fields('1i','Freeboard after discharge','With constant TPC30 t/cm,600 t of cargo is discharged. Ignore trim. By how many metres does freeboard increase?',
 [('Freeboard increase (m)',.2,2)],'Draught decreases600/30=20 cm;freeboard increases.20 m.')
choices('1j','Selecting a load-line limit','Which checks are relevant when deciding the permitted loading limit for a voyage? Select all that apply.',
 ['Applicable load-line zones and seasonal periods','The appropriate assigned load-line marks','Water density and the relevant fresh/dock-water allowance'],['Use the deepest mark regardless of zone and season'],
 'The permissible loading condition depends on assigned marks,the voyage area/season and water-density allowances.')
choices('2c','Neutral initial stability','Under ideal initial-stability theory, what condition corresponds to neutral initial stability?',
 'GM is zero',['GM is always strongly positive','G is necessarily below the keel','Displacement is zero'],
 'When G and M coincide,initial GM is zero and the initial restoring tendency vanishes.')
fields('2a','Small-angle righting lever','Effective GM is1.80 m. Use GZ=GM×sin(heel) at the given small angle of10°. Calculate GZ to three decimal places.',
 [('Righting lever GZ (m)',1.8*math.sin(math.radians(10)),3)],'GZ=1.8 sin10°=.3125667 m,rounded.313 m.')
fields('2e','Different GZ curve','Use the supplied training curve. Read maximum GZ to one decimal place and the angle of vanishing stability in whole degrees.',
 [('Maximum GZ (m)',.9,1),('Angle of vanishing stability (degrees)',80,0)],
 'The plotted maximum GZ is.9 m at40° and the positive range ends at80°.',image='assets/gz-paper-3.svg')
fields('2p','Combined free-surface moments','At displacement10,000 t, two slack tanks have free-surface moments600 and900 tonne-metres. Calculate the total virtual rise of G to two decimal places.',
 [('Virtual rise of G (m)',.15,2)],'FSC=(600+900)/10000=.15 m.')
fields('2n','Removing an off-centre G','A vessel displaces10,000 t and G is0.12 m to starboard of the centreline. What distance must a200 t onboard weight move to port to bring G to the centreline? Ignore all other changes.',
 [('Required portward shift (m)',6,1)],'Moment required=10000×.12=1200 tm;distance=1200/200=6.0 m to port.')
fields('2m','List after an off-centre load','After loading, final displacement is6,000 t and effective GM0.90 m. The only transverse heeling moment is from a100 t load placed6.0 m to starboard of the centreline. Using tan(list)=heeling moment/(displacement×GM),calculate list to one decimal place.',
 [('Starboard list (degrees)',math.degrees(math.atan(600/5400)),1)],'tan(list)=100×6/(6000×.9)=.111111;list=6.3°starboard.')
match('2j','Directions of movement of G','Ignoring free surface,match each operation to the direction in which G moves.',[
 ('Load a weight above the existing G','Upwards towards the added weight'),('Discharge a weight above the existing G','Downwards away from the removed weight'),('Shift an onboard weight to port','Towards port parallel to the shift')],
 'Adding weight moves G towards it;removing weight moves G away;an onboard transfer moves G parallel to the transfer.')
choices('2j','A freely suspended load','For stability assessment after a ship’s crane has lifted a load clear,where is that freely suspended load treated as acting?',
 'At its point of suspension',['At its original stowage position','At the keel directly below the hook','At the sea surface regardless of crane geometry'],
 'The effective action is at the suspension point,not at the hanging load’s own centre.')
choices('2o','Suspected angle of loll','A vessel with suspected negative initial GM heels without an established off-centre weight. What is the appropriate principle for deciding a correction?',
 'Have the Master assess the stability condition and restore positive stability using the approved information',
 ['Assume it is an ordinary list and shift a large weight across immediately','Treat the heel as proof of a large positive GM','Ignore free-surface effects because the vessel is heeled'],
 'Loll is associated with negative GM;an unassessed transverse shift can be dangerous. Use the approved stability information to address the underlying condition.')
choices('2r','Density and free surface','For the same slack-tank geometry and free-surface shape,what happens to its free-surface moment if liquid density doubles?',
 'It doubles',['It halves','It is unchanged','It falls to zero'],
 'Free-surface moment is proportional to liquid density for fixed free-surface geometry.')
match('3a','Longitudinal centres','Match each abbreviation to its definition.',[
 ('LCF','Longitudinal centroid of the waterplane area'),('LCG','Longitudinal position of the vessel’s centre of gravity'),('LCB','Longitudinal position of the centre of the displaced volume')],
 'LCF concerns waterplane area,LCG mass and LCB displaced volume.')
choices('3a','Direction of trim','Forward draught is6.00 m and aft draught5.40 m. What is the trim?',
 '0.60 m by the head',['0.60 m by the stern','5.70 m by the head','No trim'],
 'Forward draught exceeds aft by.60 m,so trim is.60 m by the head.')
fields('3a','MCTC application','Constant MCTC is125 tonne-metres/cm. A2,500 tonne-metre trimming moment is applied. Find magnitude of change of trim in centimetres.',
 [('Change of trim (cm)',20,1)],'2500/125=20 cm.')
fields('3c','Longitudinal transfer distance','A150 t weight moves from10 m forward of LCF to30 m aft of LCF. MCTC stays200 tonne-metres/cm. Find the sternward change of trim in centimetres.',
 [('Change of trim by stern (cm)',30,1)],'Transfer distance=10+30=40 m;moment=6000 tm;trim change=6000/200=30 cm by stern.')
fields('3b','Forward LCF and mean draught','Forward draught4.80 m;aft5.40 m;LBP120 m;LCF12 m forward of amidships. Assume a straight waterline and true mean draught equal to draught at LCF. Calculate TMD to two decimal places.',
 [('True mean draught (m)',5.04,2)],'LCF is48 m aft of FP.Draught at LCF=4.8+(.6×48/120)=5.04 m.')
fields('3c','Loading at LCF','A vessel is initially on even keel at6.00 m. Load300 t exactly at LCF;TPC stays25 t/cm. Ignore changes in hydrostatic characteristics. Find final forward and aft draughts to two decimal places.',
 [('Final forward draught (m)',6.12,2),('Final aft draught (m)',6.12,2)],
 'No trimming moment at LCF;parallel sinkage=300/25=12 cm.Both draughts become6.12 m.')
fields('3c','Discharge aft of LCF','A vessel is initially on even keel at6.00 m.LCF is amidships;LBP100 m;TPC20 t/cm;MCTC150 tonne-metres/cm,all constant.Discharge200 t from30 m aft of LCF.Find final forward and aft draughts to two decimal places.',
 [('Final forward draught (m)',6.1,2),('Final aft draught (m)',5.7,2)],
 'Parallel rise=200/20=10 cm.Trim change=200×30/150=40 cm by head,split20 cm each end.F=6−.10+.20=6.10;A=6−.10−.20=5.70 m.')
choices('4e','Gangway as draught changes','During discharge alongside,a gangway becomes excessively steep.What should the deck watch do?',
 'Arrange a safe adjustment or alternative access and keep the access route properly controlled',
 ['Allow access to continue because the gangway was safe at arrival','Remove lighting to discourage use','Leave the problem to visitors to manage'],
 'Access arrangements need continuing monitoring as draught,tide and ship position change.')
choices('4a','Stress during cargo operations','Which practices help control hull stress during cargo and ballast operations? Select all that apply.',
 ['Check intermediate as well as final loading conditions','Follow the approved loading sequence and relevant limits','Monitor actual cargo and ballast distribution'],['Check only the final displacement and ignore the loading sequence'],
 'Intermediate conditions can exceed structural limits even when the final condition is acceptable.')
choices('4c','Fire during a port watch','A fire is discovered near cargo operations.What is an appropriate immediate response?',
 'Raise the alarm and initiate the ship’s emergency response,including safe suspension of affected operations',
 ['Continue cargo operations until smoke reaches the bridge','Enter the area alone without raising the alarm','Keep the incident unreported to avoid delay'],
 'Alarm and a coordinated response are essential;affected operations must be controlled safely.')
choices('4a','Unexpected ballast transfer','An unplanned ballast transfer is observed during cargo operations.Which actions are appropriate? Select all that apply.',
 ['Establish what transfer is occurring and coordinate its safe control','Check the loading plan,stability and stress implications','Notify the responsible personnel and record the relevant changes'],['Assume any transfer is harmless if the ship remains upright'],
 'Ballast changes affect draught,stability,trim and stress and must remain coordinated with the plan.')
choices('5a','Plastic waste at sea','Under MARPOL Annex V,which statement about disposal of plastic garbage into the sea is correct?',
 'It is prohibited,including beyond the normal distance limits used for some other garbage',
 ['It is permitted after12 nautical miles in all cases','It is permitted if the plastic is chopped up','It is required when reception facilities are inconvenient'],
 'Annex V prohibits discharge of plastics into the sea.',source='marpol')
choices('6a','Sewage annex','Which MARPOL Annex principally addresses pollution by sewage from ships?',
 'Annex IV',['Annex I','Annex III','Annex VI'],
 'Annex IV addresses sewage;I oil,III harmful substances in packaged form andVI air pollution.',source='marpol')
choices('5a','Fuel routed to the wrong tank','Fuel transfer is found to be entering an unintended tank.Which actions are appropriate? Select all that apply.',
 ['Stop or safely suspend transfer and communicate with the supplying station','Confirm tank levels and the valve arrangement before any restart','Assess and respond to any overflow or pollution risk'],['Change valves blindly while maintaining full transfer rate'],
 'A misrouting must be brought under control before overflow;communication and verified alignment are essential.')
choices('6b','Master’s safety authority','Commercial instructions would conflict with the Master’s decision needed for safety and pollution prevention.How should the safety-management arrangements treat the Master’s authority?',
 'Recognise the Master’s overriding authority and responsibility for those decisions',
 ['Make the commercial schedule automatically take precedence','Allow the charterer to cancel safety procedures verbally','Require the bridge to continue regardless of navigational danger'],
 'The ISM framework requires the SMS to address the Master’s overriding authority regarding safety and pollution prevention.',source='ism')
choices('6d','Onboard complaints','Which principle belongs in an MLC-compliant onboard complaint procedure?',
 'Seafarers can raise complaints through the procedure without victimisation',
 ['Complaints may be punished merely for being made','All complaints must remain undisclosed to the seafarer who made them','The procedure must forbid access to external competent authorities'],
 'MLC complaint arrangements protect the right to complain and should safeguard against victimisation.',source='complaints')
choices('6d','Daily rest pattern','Assume an adult seafarer is subject to the normal UK rest rules,with no exception or emergency,and that weekly totals and intervals between rest periods comply.Which pattern meets both the10-hour daily minimum and the normal split-rest rule?',
 'One6-hour rest period and one4-hour rest period',['Two5-hour rest periods','One6-hour period and two2-hour periods','One7-hour period and one2-hour period'],
 'Normal rest may be divided into no more than two periods,one at least6 hours.Total6+4=10;5+5 lacks a6-hour period;6+2+2 has three periods;7+2 totals only9.',source='mlc')


def build():
    base = json.loads((WEB/'papers.js').read_text().removeprefix('window.NEW_PAPERS=').rstrip(' ;\n'))
    by_id = {p['id']:p for p in base if p['id'] in ('mock','navigation-1','stability-1')}
    for id_, category, edition in [('mock','stability',4),('navigation-1','navigation',1),('stability-1','stability',1)]:
        by_id[id_].update(subject=category,number=edition,title=f'Paper {edition}',description='OOW Unlimited practice examination.')
    review = {'syllabus_version':'June 2024; used from March 2025 examinations', 'references':SOURCES,'papers':BANKS}
    assert len(BANKS)==5
    for p in BANKS:
        assert len(p['questions'])==35,(p['id'],len(p['questions']))
        assert {int(q['syllabus'].split()[1][0]) for q in p['questions']} == set(range(1,10 if p['subject']=='navigation' else 7)),p['id']
        app_paper={**p,'questions':[{k:v for k,v in q.items() if k not in ('rationale','sources')} for q in p['questions']]}
        by_id[p['id']]=app_paper
    ordered=[by_id[f'navigation-{i}'] for i in range(1,5)]+[by_id[f'stability-{i}'] for i in range(1,4)]+[by_id['mock']]
    (WEB/'papers.js').write_text('window.NEW_PAPERS='+json.dumps(ordered,ensure_ascii=False,indent=2)+';\n')
    (ROOT/'tools'/'additional-paper-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
    print('Built5 additional papers,175 questions;8 papers in total.')

if __name__=='__main__':
    build()
