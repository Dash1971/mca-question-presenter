'use strict';
const $ = id => document.getElementById(id);
const {answered, result: calculateResult} = window.ExamCore;
const STORE = 'mca-oow-exams-v2';
const SUBJECTS = [
  {id:'navigation', title:'Navigation', code:'034-83', icon:'✦'},
  {id:'stability', title:'Stability & Operations', code:'034-84', icon:'⚓'}
];
const papers = (window.NEW_PAPERS || []).map(p => ({...p, questions:p.id === 'mock' ? window.PAPER : p.questions}));
let saved = {}, ui = {}, storageAvailable = true;
try {
  const value = JSON.parse(localStorage.getItem(STORE) || '{}');
  if (value && typeof value === 'object' && !Array.isArray(value)) saved = value;
  ui = JSON.parse(localStorage.getItem(STORE + '-ui') || '{}') || {};
} catch (_) { storageAvailable = false; }
let openSubjects = new Set(Array.isArray(ui.openSubjects) ? ui.openSubjects : []);
let paperIndex = 0, current = 0, view = 'library', zoom = 1, activeToken = null, dragToken = null;
const paper = () => papers[paperIndex];
const subject = () => SUBJECTS.find(item => item.id === paper().subject);
function attempt() {
  const id = paper().id;
  if (!saved[id] || typeof saved[id] !== 'object' || Array.isArray(saved[id])) saved[id] = {};
  const value = saved[id];
  if (!value.responses || typeof value.responses !== 'object' || Array.isArray(value.responses)) value.responses = {};
  if (!Array.isArray(value.flags)) value.flags = [];
  value.submitted = value.submitted === true;
  return value;
}
function response(q) {
  const responses = attempt().responses;
  if (!responses[q.id] || typeof responses[q.id] !== 'object' || Array.isArray(responses[q.id])) responses[q.id] = {};
  const value = responses[q.id];
  for (const name of ['selected', 'fields', 'matches']) if (!Array.isArray(value[name])) value[name] = [];
  if (!value.points || typeof value.points !== 'object' || Array.isArray(value.points)) value.points = {};
  return value;
}
function persist() {
  try { localStorage.setItem(STORE, JSON.stringify(saved)); localStorage.setItem(STORE + '-ui', JSON.stringify({openSubjects:[...openSubjects]})); }
  catch (_) { storageAvailable = false; }
  if ($('save-status')) $('save-status').textContent = storageAvailable ? '✓ Saved on this device' : 'Progress stays in this session';
}
function node(tag, text, cls) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (cls) element.className = cls;
  return element;
}
function button(text, action, cls) {
  const element = node('button', text, cls);
  element.type = 'button';
  if (typeof action === 'function') element.onclick = action;
  else if (action) element.dataset.action = action;
  return element;
}
function announce(text) { $('announcements').textContent = text; }
function doneCount() { return paper().questions.filter(q => answered(q, attempt().responses[q.id])).length; }
function questionGrid(container) {
  container.replaceChildren();
  paper().questions.forEach((q, i) => {
    const done = answered(q, attempt().responses[q.id]), flagged = attempt().flags.includes(q.id);
    const b = button(String(i + 1), () => { if (!attempt().submitted) showQuestion(i); }, 'qnum' + (done ? ' answered' : '') + (flagged ? ' flagged' : ''));
    b.setAttribute('aria-label', `Question ${i + 1}, ${done ? 'answered' : 'unanswered'}${flagged ? ', flagged for review' : ''}`);
    if (i === current) b.setAttribute('aria-current', 'true');
    b.disabled = attempt().submitted;
    container.append(b);
  });
}
function legend() {
  const element = node('div', undefined, 'legend');
  element.innerHTML = '<span><b aria-hidden="true"></b>Answered</span><span><i aria-hidden="true">◆</i>Flagged for review</span>';
  return element;
}
function renderSidebar() {
  const rail = $('sidebar'); rail.replaceChildren();
  if (view === 'library') {
    rail.append(node('p', 'Your practice library', 'rail-title'));
    const all = button('All papers', 'library', 'rail-library'); all.append(node('span', String(papers.length))); all.setAttribute('aria-current','page');
    rail.append(all);
    const info = node('div', undefined, 'rail-info');
    info.innerHTML = '<strong>OOW Unlimited</strong>Navigation · 034-83<br>Stability &amp; Operations · 034-84<br><br>Offline practice<br>No account needed'; rail.append(info); return;
  }
  rail.append(button('← All papers', 'library', 'text-button'), node('p','Current paper','rail-title'), node('p',subject().title,'current-paper'), node('p',`${paper().title} · ${paper().questions.length} questions`,'paper-meta'));
  const count = doneCount(), total = paper().questions.length;
  const progress = node('div',undefined,'progress-label'); progress.append(node('span',`${count} of ${total} answered`),node('span',`${Math.round(count / total * 100)}%`));
  const track = node('div',undefined,'progress-track'), fill = node('div',undefined,'progress-fill'); fill.style.width = `${count / total * 100}%`; track.append(fill);
  const nav = node('nav',undefined,'question-grid'); nav.setAttribute('aria-label','Questions'); questionGrid(nav);
  const note = node('p', storageAvailable ? 'Your place and responses are saved on this device.' : 'Browser storage is unavailable. Keep this page open to retain this session.', 'rail-info');
  rail.append(progress,track,nav,legend(),note);
}
function setView(next) {
  view = next;
  for (const name of ['library','exam','review','result']) $(name + '-screen').hidden = name !== view;
  renderSidebar();
}
function showLibrary() {
  setView('library');
  const area = $('library-screen'); area.replaceChildren();
  const heading = node('h1','Your exam library'); heading.id = 'library-title';
  area.append(node('div','OOW Unlimited · practice exams','eyebrow'),heading,node('p','Choose a subject to see the available exams.','subheading'));
  const groups = node('div',undefined,'subjects');
  SUBJECTS.forEach(item => {
    const list = papers.filter(p => p.subject === item.id).sort((a,b) => a.number - b.number);
    const section = node('section',undefined,'subject'), title = node('h2',undefined,'subject-heading');
    const toggle = button(undefined,undefined,'subject-toggle'); toggle.id = item.id + '-toggle'; toggle.setAttribute('aria-controls',item.id + '-papers'); toggle.setAttribute('aria-expanded',String(openSubjects.has(item.id)));
    const titleText = node('span',undefined,'subject-text'); titleText.append(node('span',item.title,'subject-name'),node('span',`${list.length} exams · ${item.code}`,'subject-meta'));
    const symbol=node('span',item.icon,'subject-icon'); symbol.setAttribute('aria-hidden','true'); const chevron=node('span',openSubjects.has(item.id)?'⌃':'⌄','subject-chevron'); chevron.setAttribute('aria-hidden','true');
    toggle.append(symbol,titleText,chevron); title.append(toggle);
    const content = node('div',undefined,'subject-papers'); content.id = item.id + '-papers'; content.hidden = !openSubjects.has(item.id); content.setAttribute('role','region'); content.setAttribute('aria-labelledby',toggle.id);
    list.forEach(p => {
      const row = node('article',undefined,'paper-row'), text = node('div');
      const a = saved[p.id], started = a?.responses && p.questions.some(q => answered(q,a.responses[q.id]));
      text.append(node('h3',p.title),node('p',`${p.questions.length} questions · 1 mark per question`,'paper-meta'));
      row.append(text,button(a?.submitted ? 'View result →' : started ? 'Resume paper →' : 'Start paper →',() => openPaper(p.id)));
      content.append(row);
    });
    toggle.onclick = () => {
      const open = content.hidden;
      content.hidden = !open; toggle.setAttribute('aria-expanded',String(open)); chevron.textContent = open ? '⌃' : '⌄';
      if (open) openSubjects.add(item.id); else openSubjects.delete(item.id);
      persist();
    };
    section.append(title,content); groups.append(section);
  });
  area.append(groups,node('p','One mark per question · answers withheld · progress saved on this device','fine-print'));
  history.replaceState(null,'',location.pathname + location.search);
  window.scrollTo(0,0);
}
function openPaper(id) {
  const index = papers.findIndex(p => p.id === id); if (index < 0) return;
  paperIndex = index;
  const a = attempt(); current = Number.isInteger(a.current) ? Math.min(Math.max(0,a.current),paper().questions.length-1) : 0;
  openSubjects.add(paper().subject);
  if (a.submitted) showResult(); else showQuestion(current);
}
function showQuestion(index) {
  if (attempt().submitted) { showResult(); return; }
  current = Math.max(0,Math.min(paper().questions.length-1,index)); attempt().current = current;
  zoom = 1; activeToken = null; dragToken = null;
  setView('exam');
  const q = paper().questions[current], value = response(q);
  $('paper-title').textContent = paper().title; $('paper-subject').textContent = `${subject().code} · ${subject().title}`;
  $('meta').textContent = `Question ${current + 1} of ${paper().questions.length} · 1 mark`;
  $('title').textContent = q.title; $('prompt').textContent = q.prompt + (q.warning ? '\n\nNote: ' + q.warning : '');
  $('context').hidden = !q.context; $('context').textContent = q.context || '';
  $('visual').hidden = !q.image; $('placed-tokens').replaceChildren();
  if (q.image) { $('figure').src = q.image; $('figure').alt = q.imageAlt || `Figure for question ${current + 1}: ${q.title}`; applyZoom(); } else $('figure').removeAttribute('src');
  const area = $('interaction'); area.replaceChildren();
  if (q.kind === 'single' || q.kind === 'multi') renderChoices(q,value,area);
  if (q.kind === 'fields') renderFields(q,value,area);
  if (q.kind === 'match') renderMatch(q,value,area);
  if (q.kind === 'place') renderPlace(q,value,area);
  $('prev').disabled = current === 0; $('next').disabled = current === paper().questions.length-1;
  updateProgress(); persist();
  history.replaceState(null,'',`#${paper().id}-q${q.id}`);
  window.scrollTo(0,0);
}
function updateProgress() {
  renderSidebar(); questionGrid($('mobile-question-nav'));
  $('mobile-summary').textContent = `Questions · ${doneCount()} of ${paper().questions.length} answered`;
  const flagged = attempt().flags.includes(paper().questions[current].id);
  $('flag').setAttribute('aria-pressed',String(flagged)); $('flag').textContent = flagged ? '⚑ Flagged for review' : '⚑ Flag for review';
}
function renderChoices(q,value,area) {
  area.append(node('p',q.kind === 'multi' ? 'Select all answers that apply.' : 'Select one answer.','answer-hint'));
  const box = node('fieldset',undefined,'choices'), label = node('legend','Answer options','sr-only'); box.append(label);
  q.options.forEach((option,i) => {
    const choice=node('label',undefined,'choice' + (value.selected.includes(i) ? ' selected' : ''));
    const input=document.createElement('input'); input.type = q.kind === 'single' ? 'radio' : 'checkbox'; input.name = 'answer'; input.value = String(i); input.checked = value.selected.includes(i);
    input.onchange = () => {
      if (attempt().submitted) return;
      value.selected = q.kind === 'single' ? [i] : input.checked ? [...value.selected.filter(v => v !== i),i] : value.selected.filter(v => v !== i);
      box.querySelectorAll('input').forEach(x => x.closest('label').classList.toggle('selected',x.checked)); persist(); updateProgress();
    };
    choice.append(input,node('span',String.fromCharCode(65+i),'choice-letter'),node('span',option)); box.append(choice);
  }); area.append(box);
}
function renderFields(q,value,area) {
  q.fields.forEach((field,i) => {
    const wrapper=node('div',undefined,'field'), label=node('label',field.label), id=`field-${i}`; label.htmlFor=id;
    let input;
    if (field.choices) { input=document.createElement('select'); input.append(new Option('Choose…','')); field.choices.forEach(x => input.append(new Option(x,x))); }
    else { input=document.createElement('input'); input.type='text'; input.inputMode='decimal'; input.autocomplete='off'; input.placeholder='Enter answer'; }
    input.id=id; input.value=value.fields[i] ?? '';
    input.addEventListener(field.choices ? 'change' : 'input',() => { if (!attempt().submitted) { value.fields[i]=input.value; persist(); updateProgress(); } });
    wrapper.append(label,input); area.append(wrapper);
  });
}
function renderMatch(q,value,area) {
  q.terms.forEach((term,i) => {
    const row=node('div',undefined,'match-row'), label=node('label',term), select=document.createElement('select'); select.id=`match-${i}`; label.htmlFor=select.id;
    select.append(new Option('Choose definition…','')); q.definitions.forEach((definition,j) => select.append(new Option(definition,String(j))));
    select.value=Number.isInteger(value.matches[i]) ? String(value.matches[i]) : '';
    select.onchange=() => {if (!attempt().submitted) {value.matches[i]=select.value === '' ? null : Number(select.value);persist();updateProgress();}};
    row.append(label,select); area.append(row);
  });
}
function renderPlace(q,value,area) {
  area.append(node('p','Select a label, then click its position on the figure. Drag labels to adjust, or select a placed label to remove it.','answer-hint'));
  const tray=node('div',undefined,'token-tray');
  q.tokens.forEach(token => {
    const b=button(token,() => {activeToken=token;tray.querySelectorAll('button').forEach(x=>{x.classList.toggle('active',x.textContent===token);x.setAttribute('aria-pressed',String(x.textContent===token));});announce(`${token} selected. Choose its position on the figure.`);});
    b.setAttribute('aria-pressed','false'); b.draggable=true; b.ondragstart=e=>{dragToken=token;e.dataTransfer.setData('text/plain',token);}; tray.append(b);
  });
  area.append(tray); drawPoints(q,value);
}
function drawPoints(q,value) {
  $('placed-tokens').replaceChildren();
  Object.entries(value.points).forEach(([token,point]) => {
    if (!q.tokens.includes(token) || !Array.isArray(point) || !point.every(Number.isFinite)) return;
    const b=button(token,e=>{e.stopPropagation();if(attempt().submitted)return;delete value.points[token];persist();drawPoints(q,value);updateProgress();},'placed');
    b.style.left=`${point[0]}%`;b.style.top=`${point[1]}%`;b.draggable=true;b.setAttribute('aria-label',`Remove ${token} placement`);
    b.ondragstart=e=>{dragToken=token;e.dataTransfer.setData('text/plain',token);}; $('placed-tokens').append(b);
  });
}
function placeAt(e) {
  const q=paper().questions[current]; if(view!=='exam'||q.kind!=='place'||attempt().submitted)return;
  const token=dragToken||activeToken; if(!q.tokens.includes(token))return;
  const rect=$('figure').getBoundingClientRect();if(!rect.width||!rect.height)return;
  const x=Math.max(0,Math.min(100,(e.clientX-rect.left)/rect.width*100)),y=Math.max(0,Math.min(100,(e.clientY-rect.top)/rect.height*100));
  response(q).points[token]=[Math.round(x*10)/10,Math.round(y*10)/10];activeToken=null;dragToken=null;persist();drawPoints(q,response(q));updateProgress();
  $('interaction').querySelectorAll('[aria-pressed]').forEach(b=>{b.setAttribute('aria-pressed','false');b.classList.remove('active');});
}
function applyZoom() {
  const image=$('figure'), available=$('figure-viewport').clientWidth-24;
  if (available<=0) return;
  const base=Math.min(image.naturalWidth||800,available);image.style.width=`${Math.round(base*zoom)}px`;image.style.maxWidth='none';$('zoom-label').textContent=`${Math.round(zoom*100)}%`;
}
function showReview() {
  if (attempt().submitted) {showResult();return;}
  setView('review'); const area=$('review-screen');area.replaceChildren();
  const title=node('h1','Ready to submit?');title.id='review-title';
  area.append(node('div',`${subject().title} · ${paper().title}`,'eyebrow'),title,node('p','Check your questions before finishing this attempt.','subheading'));
  const panel=node('div',undefined,'check-panel'),tallies=node('div',undefined,'tallies');
  const missing=paper().questions.length-doneCount();
  for(const [count,label] of [[doneCount(),'Answered'],[missing,'Unanswered'],[attempt().flags.length,'Flagged']]){const item=node('div');item.append(node('strong',String(count)),node('span',label));tallies.append(item);}
  const grid=node('nav',undefined,'question-grid');grid.setAttribute('aria-label','Review questions');questionGrid(grid);panel.append(tallies,grid,legend());
  if(missing)panel.append(node('p',`${missing} unanswered question${missing===1?'':'s'} will score zero.`,'notice'));
  panel.append(node('p','Submission is final for this attempt. You will see your percentage and number correct.','fine-print'));
  const actions=node('div',undefined,'check-actions');actions.append(button('Submit paper','submit','primary'),button('Keep working','back'));panel.append(actions);area.append(panel);window.scrollTo(0,0);
}
function showResult() {
  setView('result');const area=$('result-screen');area.replaceChildren();const score=calculateResult(paper(),attempt().responses);
  const title=node('h1','Attempt complete');title.id='result-title';area.append(node('div',`${subject().title} · ${paper().title}`,'eyebrow'),title,node('p','Your submitted attempt is locked.','subheading'));
  const panel=node('div',undefined,'result-panel');panel.setAttribute('aria-label','Final result');panel.append(node('div','Final mark','eyebrow'),node('p',`${score.percent}%`,'score'),node('p',`${score.correct} of ${score.total} correct`,'result-detail'),node('p','Submitted · responses locked','save-status'));
  const actions=node('div',undefined,'check-actions');actions.append(button('Choose another paper →','library','primary'),button('New attempt','restart'));panel.append(actions,node('p','Correct answers and individual question results are withheld.','result-note'));area.append(panel);history.replaceState(null,'',`#${paper().id}-q${paper().questions[current].id}`);window.scrollTo(0,0);
}
$('prev').onclick=()=>showQuestion(current-1);$('next').onclick=()=>showQuestion(current+1);
$('flag').onclick=()=>{if(attempt().submitted)return;const flags=attempt().flags,id=paper().questions[current].id;attempt().flags=flags.includes(id)?flags.filter(x=>x!==id):[...flags,id];persist();updateProgress();};
$('figure').onload=applyZoom;
for(const [id,delta] of [['zoom-in',.25],['zoom-out',-.25]])$(id).onclick=()=>{zoom=Math.max(.5,Math.min(3,zoom+delta));applyZoom();};
$('zoom-reset').onclick=()=>{zoom=1;applyZoom();};window.addEventListener('resize',applyZoom);
$('figure-viewport').addEventListener('click',placeAt);$('figure-viewport').addEventListener('dragover',e=>e.preventDefault());$('figure-viewport').addEventListener('drop',e=>{e.preventDefault();dragToken=e.dataTransfer.getData('text/plain');placeAt(e);});
function restartDialog(){ $('restart-paper').textContent=`${subject().title} · ${paper().title}`;$('restart-dialog').showModal(); }
function performAction(action) {
  if(action==='library')showLibrary();
  if(action==='review')showReview();
  if(action==='back')showQuestion(current);
  if(action==='submit' && !attempt().submitted && view==='review'){attempt().submitted=true;persist();showResult();announce('Paper submitted. Your attempt is locked.');}
  if(action==='restart')restartDialog();
  if(action==='cancel-restart')$('restart-dialog').close();
  if(action==='confirm-restart'){saved[paper().id]={responses:{},flags:[],current:0,submitted:false};persist();$('restart-dialog').close();showQuestion(0);}
}
// Do not let a newly rendered button handle the click that created it.
// Delegation is limited to stable data-action controls; question buttons bind directly.
document.addEventListener('click',e=>{const b=e.target.closest('button[data-action]');if(b&&!b.disabled)performAction(b.dataset.action);});
document.addEventListener('keydown',e=>{if(view!=='exam'||['INPUT','SELECT','TEXTAREA','BUTTON','SUMMARY'].includes(document.activeElement?.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();showQuestion(current+1);}if(e.key==='ArrowLeft'){e.preventDefault();showQuestion(current-1);}});
const hash=location.hash.match(/^#([a-z0-9-]+)-q(\d+)$/);
if(hash && papers.some(p=>p.id===hash[1])) {paperIndex=papers.findIndex(p=>p.id===hash[1]);const index=paper().questions.findIndex(q=>q.id===Number(hash[2]));current=Math.max(0,index);if(attempt().submitted)showResult();else showQuestion(current);}
else showLibrary();
