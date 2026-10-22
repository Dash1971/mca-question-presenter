import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
if (!process.argv[2]) throw new Error('Usage: node tools/build_instructor_workbook.mjs OUTPUT_DIRECTORY');
const output = path.resolve(process.argv[2]);
const {rows} = JSON.parse(await fs.readFile(`${output}/question-bank.json`,'utf8'));
const keys = ['Subject','Paper','Question','Type','Syllabus reference','Title','Question text','Context','Options or fields','Correct answer','Explanation','Figure','Review scope','Review method','Review working','Primary references','Paper ID','Source question ID','Instructor status','Instructor comments'];
const matrix = [keys,...rows.map(row=>keys.map(key=>row[key]??''))];
const wb = Workbook.create(); const sheet=wb.worksheets.add('Questions');
sheet.showGridLines=false; sheet.tabColor='#203B50';
sheet.getRange('A1').write(matrix);
const all=sheet.getRange('A1:T280');
all.format.font={name:'Arial',size:10,color:'#172C3A'}; all.format.wrapText=true; all.format.verticalAlignment='top';
const widths=[26,8,10,10,19,34,72,45,72,65,72,35,30,34,72,85,22,18,25,55];
for(let i=0;i<widths.length;i++) sheet.getRangeByIndexes(0,i,280,1).format.columnWidth=widths[i];
sheet.getRange('A1:T1').format.fill='#203B50';sheet.getRange('A1:T1').format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};
sheet.getRange('A1:T1').format.rowHeight=34;sheet.getRange('A1:T1').format.horizontalAlignment='center';
sheet.getRange('B2:C280').setNumberFormat('0');sheet.getRange('R2:R280').setNumberFormat('0');
for(let r=1;r<matrix.length;r++){
  const lines=Math.max(...matrix[r].map((v,c)=>String(v).split('\n').reduce((n,s)=>n+Math.max(1,Math.ceil(s.length/(widths[c]*.88))),0)));
  sheet.getRangeByIndexes(r,0,1,20).format.rowHeight=Math.min(409,Math.max(44,lines*13+10));
}
sheet.getRange('S2:T280').format.fill='#FFF5CE';
sheet.getRange('S2:S280').dataValidation={rule:{type:'list',values:['Not checked','Accepted','Query','Correction needed']}};
sheet.freezePanes.freezeRows(1);sheet.freezePanes.freezeColumns(3);
const table=sheet.tables.add('A1:T280',true,'OOWQuestions');table.showFilterButton=true;
wb.recalculate();
const actual=all.values;
if(actual.length!==280||actual[279][16]!=='mock')throw new Error('Incomplete question bank');
for(let r=0;r<matrix.length;r++)for(let c=0;c<keys.length;c++)if(String(actual[r][c]??'')!==String(matrix[r][c]))throw new Error(`Cell mismatch ${r},${c}`);
console.log((await wb.inspect({kind:'table',range:'Questions!A1:F3',tableMaxRows:3,tableMaxCols:6,maxChars:1800})).ndjson);
// CSV preserves the authored worksheet values, including quotes and newlines.
const csv=actual.map(row=>row.map(value=>'"'+String(value??'').replaceAll('"','""')+'"').join(',')).join('\r\n')+'\r\n';
await fs.writeFile(`${output}/Question-bank.csv`,'\uFEFF'+csv,'utf8');
const preview=await wb.render({sheetName:'Questions',range:'A1:G3',scale:1.25,format:'png'});
await fs.writeFile(path.join(process.env.TMPDIR || '/tmp','mca-question-workbook-preview.png'),new Uint8Array(await preview.arrayBuffer()));
await (await SpreadsheetFile.exportXlsx(wb)).save(`${output}/Question-bank.xlsx`);
console.log('Exported 279 rows to CSV and filtered workbook.');
