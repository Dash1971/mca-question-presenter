'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const web = path.join(__dirname,'../presenter/web');
const core = require(path.join(web,'exam-core.js'));
const context = {window:{}};
vm.runInNewContext(fs.readFileSync(path.join(web,'paper.js'),'utf8'),context);
vm.runInNewContext(fs.readFileSync(path.join(web,'papers.js'),'utf8'),context);
const papers = JSON.parse(JSON.stringify(context.window.NEW_PAPERS)).map(p => ({...p,questions:p.id==='mock'?JSON.parse(JSON.stringify(context.window.PAPER)):p.questions}));
function keyResponse(q) {
  if(q.kind==='single'||q.kind==='multi')return {selected:[...q.answer]};
  if(q.kind==='fields')return {fields:q.answers || q.fields.map(f=>f.answer)};
  if(q.kind==='match')return {matches:[...q.answers]};
  if(q.kind==='place')return {points:Object.fromEntries(q.tokens.map(t=>[t,[(q.targets[t][0]+q.targets[t][2])/2,(q.targets[t][1]+q.targets[t][3])/2]]))};
}
for(const paper of papers) {
  test(`${paper.id}: every complete key grades correctly; blank and damaged responses do not`,()=>{
    const responses={};
    for(const q of paper.questions) {
      const response=keyResponse(q);assert.equal(core.grade(q,response),true,`key ${q.id}`);assert.equal(core.grade(q,{}),false,`blank ${q.id}`);responses[q.id]=response;
      if(q.kind==='multi')assert.equal(core.grade(q,{selected:[...q.answer,q.options.length]}),false);
      if(q.kind==='fields')assert.equal(core.grade(q,{fields:response.fields.map(()=> '')}),false);
      if(q.kind==='match')assert.equal(core.grade(q,{matches:response.matches.map(()=>null)}),false);
      if(q.kind==='place')assert.equal(core.grade(q,{points:{}}),false);
    }
    assert.deepEqual(core.result(paper,responses),{correct:paper.questions.length,total:paper.questions.length,percent:100});
    assert.equal(core.result(paper,{}).percent,0);
    assert.equal(core.result(paper,{[paper.questions[0].id]:keyResponse(paper.questions[0])}).percent,3);
  });
}
test('field grading respects signed decimals, zero, precision and all-or-nothing marking',()=>{
  const q={kind:'fields',fields:[{answer:'-1.25',tolerance:.005},{answer:'0'}]};
  assert.equal(core.grade(q,{fields:['-1.250','0.00']}),true);
  assert.equal(core.grade(q,{fields:['-1.25','']}),false);
  assert.equal(core.grade(q,{fields:['-1.20','0']}),false);
  assert.equal(core.grade(q,{fields:['-1.25m','0']}),false);
  assert.equal(core.grade(q,{fields:['-1.25','wrong']}),false);
});
test('multi-select never awards credit for a subset, extra or duplicated selections',()=>{
  const q={kind:'multi',answer:[0,2]};
  for(const selected of [[0],[0,1,2],[0,0],[0,2,2]])assert.equal(core.grade(q,{selected}),false);
  assert.equal(core.grade(q,{selected:[2,0]}),true);
});
test('clearing a matching dropdown removes answered status, including after JSON round-trip',()=>{
  const q={kind:'match',terms:['a','b'],answers:[1,0]};
  assert.equal(core.answered(q,{matches:[1,0]}),true);
  const response=JSON.parse(JSON.stringify({matches:[1,undefined]}));
  assert.equal(core.answered(q,response),false);assert.equal(core.grade(q,response),false);
});
test('placement marking requires every token inside its own target, and rejects non-numeric coordinates',()=>{
  const q={kind:'place',tokens:['A','B'],targets:{A:[0,0,10,10],B:[80,80,100,100]}};
  assert.equal(core.grade(q,{points:{A:[5,5],B:[90,90]}}),true);
  assert.equal(core.grade(q,{points:{A:[5,5],B:[10,10]}}),false);
  assert.equal(core.grade(q,{points:{A:['5','5'],B:[90,90]}}),false);
});
