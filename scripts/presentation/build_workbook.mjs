import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const project = process.env.AUTO2000_PROJECT_ROOT || process.cwd();
const work = process.env.AUTO2000_PRESENTATION_WORK || path.join(project, 'scripts/presentation');
const outputDir = process.env.AUTO2000_OUTPUT_DIR || path.join(project, 'reports');
await fs.mkdir(outputDir,{recursive:true});
await fs.mkdir(path.join(work,'qa'),{recursive:true});
const data=JSON.parse(await fs.readFile(path.join(work,'workbook_inputs.json'),'utf8'));
const wb=Workbook.create();
const names=['Overview','Economics','Case P&L','Market access','Branch portfolio','Maps cohorts','YouTube','Method'];
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const C={navy:'#17324D',blue:'#2457C5',green:'#147546',gray:'#64748B',pale:'#F1F5F9',amber:'#FFF2CC',red:'#FDE9E7'};
const font='Arial';
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
function setup(s,title,last='H',rows=80){
 s.showGridLines=false;
 s.getRange(`A1:${last}${rows}`).format.font={name:font,size:10,color:'#111827'};
 s.getRange(`A1:${last}${rows}`).format.verticalAlignment='center';
 s.getRange(`A1:${last}${rows}`).format.rowHeight=20;
 s.getRange('A1:A80').format.columnWidth=3;
 s.getRange('B2').values=[[title]];
 s.getRange('B2').format.font={name:font,size:15,bold:true,color:'#111827'};
 s.getRange(`B3:${last}3`).format.borders={bottom:{style:'thin',color:C.navy}};
}
function note(s,cell,text){s.getRange(cell).values=[[text]];s.getRange(cell).format.font={name:font,size:9,italic:true,color:C.gray};}
function header(s,range){s.getRange(range).format={fill:C.navy,font:{name:font,size:10,bold:true,color:'#FFFFFF'},verticalAlignment:'center',horizontalAlignment:'center',wrapText:true,rowHeight:35};}
function rowsTable(s,start,rows,keys,labels,widths){
 const end=col(keys.length),hr=start;
 s.getRange(`B${hr}:${end}${hr}`).values=[labels];header(s,`B${hr}:${end}${hr}`);
 if(rows.length)s.getRange(`B${hr+1}:${end}${hr+rows.length}`).values=rows.map(r=>keys.map(k=>r[k]??null));
 for(let i=0;i<keys.length;i++)s.getRange(`${col(i+1)}${hr}:${col(i+1)}${hr+Math.max(rows.length,1)}`).format.columnWidth=widths[i]??20;
 s.freezePanes.freezeRows(hr);
 return {last:hr+rows.length,end};
}

// Overview contains the actual corpus and model results once.
{
 const s=sheets.Overview;setup(s,'Auto2000 integrated research workbook','L',38);s.tabColor=C.navy;
 note(s,'B4','Research cutoff 14 November 2026. Sources retain their original languages.');
 const rows=data.coverage;
 rowsTable(s,6,rows,['platform','source_rows','unique_records','duplicate_excess_rows','record_unit'],['Platform','Source rows','Unique IDs','Duplicate rows','Unit'],[18,17,17,17,23]);
 s.getRange('C7:E9').setNumberFormat('#,##0');
 s.getRange('F7:F9').format.horizontalAlignment='center';
 s.getRange('B12').values=[['Oil access after existing owned-channel routing']];s.getRange('B12').format.font={bold:true,size:12};
 s.getRange('B14:F14').values=[['Market','Paired model origins','Tail before','Tail after','Tail removed']];header(s,'B14:F14');
 for(let i=0;i<4;i++){
  const r=15+i,src=7+i;
  s.getRange(`B${r}:F${r}`).formulas=[[`='Market access'!B${src}`,`='Market access'!C${src}`,`='Market access'!D${src}`,`='Market access'!E${src}`,`='Market access'!F${src}`]];
 }
 s.getRange('C15:F18').setNumberFormat('0');
 note(s,'B21','Tail = model origins with an oil-access gap over five minutes. Origin counts are not demand.');
 s.getRange('B24').values=[['Commercial model']];s.getRange('B24').format.font={bold:true,size:12};
 s.getRange('B26:C28').values=[['Measure','Value'],['Three-year investment ceiling (IDR)',150000000000],['Model inputs','Enter commercial inputs on Economics']];header(s,'B26:C26');
 s.getRange('C27').setNumberFormat('"Rp "#,##0');
 s.getRange('B26:B28').format.columnWidth=38;s.getRange('C28').format.columnWidth=40;
 const ch=s.charts.add('bar',[s.getRange('B14:B18'),s.getRange('D14:D18'),s.getRange('E14:E18')]);
 ch.title='Model origins with oil-access gap over five minutes';ch.hasLegend=true;ch.titleTextStyle.typeface=font;ch.titleTextStyle.fontSize=13;ch.xAxis={axisType:'textAxis',textStyle:{typeface:font,fontSize:11}};ch.yAxis={numberFormatCode:'0',numberFormatSourceLinked:false,textStyle:{typeface:font,fontSize:11}};ch.setPosition('H6','P21');
 ch.series.items[0].fill=C.gray;ch.series.items[1].fill=C.navy;
}

// The commercial schedule is intentionally unfilled where internal data are absent.
{
 const s=sheets.Economics;setup(s,'Three-prong commercial model','H',78);s.tabColor='#4B6D8D';
 s.getRange('B4').values=[['All monetary inputs and results are IDR. Blank inputs keep dependent results unavailable.']];
 s.getRange('B4').format.font={italic:true,size:9,color:C.gray};s.getRange('B4').format.columnWidth=66;
 s.getRange('D5:F5').values=[[2026,2027,2028]];header(s,'D5:F5');
 s.getRange('B6:B76').format.columnWidth=5;s.getRange('C6:C76').format.columnWidth=49;s.getRange('D6:F76').format.columnWidth=22;
 const prongs=[['New-to-Auto2000 xEV purchases',6],['Customer-paid workshop jobs',22],['Existing-customer xEV replacements',38]];
 const labels=['Completed transactions','Share incremental to Auto2000','GP per incremental transaction','Programme variable cost per completion','Displaced contribution per completion','Incremental fixed operating expense','Investment cash outflow','Incremental transactions','Incremental gross profit','Programme variable expense','Displaced contribution','Total programme operating expense','Operating contribution before depreciation','Cash contribution before tax and working capital'];
 for(const [name,b] of prongs){
  s.getRange(`C${b}:F${b}`).format.fill=C.pale;s.getRange(`C${b}`).values=[[name]];s.getRange(`C${b}`).format.font={bold:true,size:11};
  s.getRange(`C${b+1}:C${b+14}`).values=labels.map(x=>[x]);
  s.getRange(`D${b+1}:F${b+7}`).format.fill=C.amber;s.getRange(`D${b+1}:F${b+7}`).format.font={name:font,size:10,color:C.blue};
  s.getRange(`D${b+1}:F${b+1}`).setNumberFormat('#,##0');
  s.getRange(`D${b+2}:F${b+2}`).setNumberFormat('0.0%');
  s.getRange(`D${b+3}:F${b+14}`).setNumberFormat('#,##0;(#,##0);"-"');
  s.getRange(`D${b+8}:F${b+8}`).setNumberFormat('#,##0.0');
  for(const c of ['D','E','F']){
   const formulas={
    [b+8]:`=IF(COUNT(${c}${b+1}:${c}${b+2})<2,"Missing inputs",${c}${b+1}*${c}${b+2})`,
    [b+9]:`=IF(COUNT(${c}${b+8},${c}${b+3})<2,"Missing inputs",${c}${b+8}*${c}${b+3})`,
    [b+10]:`=IF(COUNT(${c}${b+1},${c}${b+4})<2,"Missing inputs",${c}${b+1}*${c}${b+4})`,
    [b+11]:`=IF(COUNT(${c}${b+1},${c}${b+5})<2,"Missing inputs",${c}${b+1}*${c}${b+5})`,
    [b+12]:`=IF(COUNT(${c}${b+10},${c}${b+6})<2,"Missing inputs",SUM(${c}${b+10},${c}${b+6}))`,
    [b+13]:`=IF(COUNT(${c}${b+9},${c}${b+12},${c}${b+11})<3,"Missing inputs",${c}${b+9}-${c}${b+12}-${c}${b+11})`,
    [b+14]:`=IF(COUNT(${c}${b+13},${c}${b+7})<2,"Missing inputs",${c}${b+13}-${c}${b+7})`
   };
   for(const [r,f] of Object.entries(formulas))s.getRange(`${c}${r}`).formulas=[[f]];
  }
  s.dataValidations.add({range:`D${b+2}:F${b+2}`,rule:{type:'decimal',operator:'between',formula1:0,formula2:1}});
 }
 s.getRange('C54:F54').format.fill=C.pale;s.getRange('C54').values=[['Portfolio totals']];s.getRange('C54').format.font={bold:true,size:11};
 const totals=[['Incremental gross profit',[15,31,47]],['Programme operating expense',[18,34,50]],['Operating contribution before depreciation',[19,35,51]],['Investment cash outflow',[13,29,45]],['Cash contribution before tax and working capital',[20,36,52]],['Displaced contribution deducted',[17,33,49]]];
 totals.forEach(([name,rs],i)=>{
  const r=55+i;s.getRange(`C${r}`).values=[[name]];
  for(const c of ['D','E','F']){const refs=rs.map(x=>c+x).join(',');s.getRange(`${c}${r}`).formulas=[[`=IF(COUNT(${refs})<3,"Missing inputs",SUM(${refs}))`]];}
 });
 s.getRange('D55:F60').setNumberFormat('#,##0;(#,##0);"-"');
 s.getRange('C62:D65').values=[['Three-year investment control','IDR'],['Case investment ceiling',150000000000],['Total entered investment',null],['Headroom against ceiling',null]];header(s,'C62:D62');
 s.getRange('D64').formulas=[['=IF(COUNT(D58:F58)<3,"Missing inputs",SUM(D58:F58))']];
 s.getRange('D65').formulas=[['=IF(ISNUMBER(D64),D63-D64,"Missing inputs")']];
 s.getRange('D63:D65').setNumberFormat('#,##0;(#,##0);"-"');
 s.getRange('D65').conditionalFormats.add('cellIs',{operator:'lessThan',formula:0,format:{fill:C.red,font:{bold:true,color:'#991B1B'}}});
 const notes=[
 'Inputs are blank because the evidence does not contain internal transaction volumes, incremental capture, contribution or programme costs.',
 'Completion means paid work or a delivered sale. Requests, app visits and confirmed appointments are earlier events.',
 'Incrementality uses the Auto2000 perimeter. Existing Auto2000 customers moving channels do not create incremental jobs.',
 'Customer-paid workshop jobs exclude free or prepaid entitlement for the specified work. Programme reimbursement requires a separate model.',
 'New-to-Auto2000 buyer purchases and existing-customer replacement purchases must be mutually exclusive.',
 'Operating contribution excludes programme depreciation. Cash contribution excludes tax and working capital. Add these before an investment return calculation.',
 'No terminal value, guarantee liability or resale recovery is assumed. Recognize these separately if a recommendation creates them.',
 'Set displaced contribution to zero if displacement is already reflected in incrementality. Allocate shared programme costs once.',
 'Amber cells are editable. Blue numbers are inputs. Black numbers are calculations. Zero is accepted as a valid numeric input.'
 ];
 s.getRange('C68:C76').values=notes.map(t=>[t]);s.getRange('C68:F76').format.rowHeight=72;s.getRange('C68:C76').format.wrapText=true;
 s.freezePanes.freezeRows(5);
}

{
 const s=sheets['Case P&L'];setup(s,'Supplied case financial baseline','I',26);
 note(s,'B4','FY2025 case assumptions, all powertrains. Monetary values below are IDR billion.');
 rowsTable(s,6,data.case,['business_line','revenue_idr_billion','gross_profit_idr_billion'],['Business line','Revenue','Gross profit'],[25,20,20]);
 s.getRange('E6:F6').values=[['Gross margin','Share of total GP']];header(s,'E6:F6');
 for(let r=7;r<=10;r++)s.getRange(`E${r}:F${r}`).formulas=[[`=D${r}/C${r}`,`=D${r}/SUM($D$7:$D$10)`]];
 s.getRange('B12:D12').values=[['Total',null,null]];s.getRange('C12:D12').formulas=[['=SUM(C7:C10)','=SUM(D7:D10)']];
 s.getRange('B14:D14').values=[['After-sales combined',null,null]];s.getRange('C14:D14').formulas=[['=SUM(C8:C10)','=SUM(D8:D10)']];
 s.getRange('E14:F14').formulas=[['=D14/C14','=D14/D12']];
 s.getRange('B17:C20').values=[['Unallocated operating expense',4620],['Operating profit',null],['Operating margin',null],['Investment ceiling 2026 to 2028',150]];
 s.getRange('C18').formulas=[['=D12-C17']];s.getRange('C19').formulas=[['=C18/C12']];
 s.getRange('C7:D18').setNumberFormat('#,##0;(#,##0);"-"');s.getRange('E7:F14').setNumberFormat('0.0%');s.getRange('C19').setNumberFormat('0.0%');
 s.getRange('B17:B20').format.columnWidth=39;s.getRange('E6:F14').format.columnWidth=19;
 note(s,'B23','Source: supplied IBSC casebook Exhibit 3, page 10; archived story_assets/economic_story.json EC01.');
 note(s,'B24','The 35% after-sales combined margin does not establish a programme or xEV-specific contribution margin.');
}

{
 const s=sheets['Market access'];setup(s,'Residual oil-access gaps by market','I',24);
 note(s,'B4','Latest corrected scenario. Existing owned channels allowed only within the specified job scope.');
 rowsTable(s,6,data.markets,['market','paired_origins_n','oil_tail_before_owned_network_n','oil_tail_after_owned_network_n','removed_tail_n','endpoints_n','unique_15min_service_origins_n'],['Market','Paired origins','Tail before','Tail after','Tail removed','Endpoints','Unique general-service origins'],[18,17,17,17,17,17,24]);
 s.getRange('C7:H10').setNumberFormat('0');
 note(s,'B13','Source: analysis/geography/tables/market_portfolio.csv and latest corrected 29-endpoint branch table.');
 note(s,'B14','These cells are a finite model. Pooling them does not estimate population, vehicle stock or customer demand.');
 note(s,'B15','Unique general-service origins use a 15-minute access threshold if a general branch is removed, not the oil-channel universe.');
}
{
 const s=sheets['Branch portfolio'];setup(s,'Branch geometry and intervention families','L',42);
 rowsTable(s,6,data.branches,['market','branch_name','assigned_grid_origins_n','oil_gap_gt5_before_owned_network_n','oil_gap_gt5_after_owned_network_n','origins_losing_15min_general_branch_access_if_removed_n','second_general_branch_penalty_median_min','_spacer','decision_family'],['Market','Branch','Assigned origins','Oil tail before','Oil tail after','General-access origins lost','Second-branch penalty minutes','','Decision family'],[17,31,17,17,17,21,22,3,68]);
 s.getRange('D7:H35').setNumberFormat('0');s.getRange('H7:H35').setNumberFormat('0.00');
 s.getRange('C7:C35').format.wrapText=true;s.getRange('J7:J35').format.wrapText=true;s.getRange('B7:J35').format.rowHeight=50;s.getRange('I6:I35').format.fill='#FFFFFF';
 note(s,'B38','Source: analysis/geography/tables/branch_portfolio.csv. Geometry does not measure branch capacity or justify closures.');
}
{
 const s=sheets['Maps cohorts'];setup(s,'Google Maps retrieval cohorts by place','N',80);
 rowsTable(s,6,data.maps,['branch_title','city','cohort','unique_reviews','with_text','stars_1','stars_2','stars_3','stars_4','stars_5','closed'],['Place','City','Retrieval cohort','Unique reviews','With text','1 star','2 stars','3 stars','4 stars','5 stars','Closed'],[38,25,31,17,17,12,12,12,12,12,13]);
 s.getRange(`E7:K${6+data.maps.length}`).setNumberFormat('#,##0');
 s.getRange(`L7:L${6+data.maps.length}`).format.horizontalAlignment='center';
 s.getRange(`B7:D${6+data.maps.length}`).format.wrapText=true;s.getRange(`B7:L${6+data.maps.length}`).format.rowHeight=32;
 note(s,`B${data.maps.length+9}`,'Source: analysis/social/maps_branch_cohort_summary.csv. Cohort membership overlaps for 266 IDs; do not sum cohort counts as unique people.');
}
{
 const s=sheets.YouTube;setup(s,'YouTube comments actually returned','J',20);
 rowsTable(s,6,data.youtube,['video_id','title','rows','top_level','replies','channel_owner_rows'],['Video ID','Video title','Comments and replies','Top-level comments','Replies','Channel-owner rows'],[20,75,23,23,17,23]);
 s.getRange('C7:C9').format.wrapText=true;s.getRange('B7:G9').format.rowHeight=48;s.getRange('D7:G9').setNumberFormat('0');
 note(s,'B13','Source: analysis/social/youtube_video_summary.csv. No Toyota video cohort was returned in these exports.');
 note(s,'B14','Comment counts are not verified-owner counts. Two channel-owner messages occur in the three-row Setir Kanan cohort.');
}
{
 const s=sheets.Method;setup(s,'Definitions and update method','D',22);s.tabColor='#94A3B8';
 const rows=[
 ['Unit of evidence','A post, review or comment is a source record. Records do not identify verified owners or completed jobs unless the content supports that interpretation.'],
 ['Retrieval flags','Keyword flags support retrieval and review. They are not validated sentiment or thematic prevalence estimates.'],
 ['Review cohorts','Newest/recent and lowest-ranking diagnostic reviews remain separate. The latter reveal failure cases but do not estimate complaint incidence.'],
 ['Geographic baseline','The most recent corrected endpoint and operator scenario supersedes earlier uncorrected results. Model origins are not people or Toyota owners.'],
 ['Financial perimeter','Incrementality belongs to Auto2000. A shift between existing owned channels is not automatically new revenue or contribution.'],
 ['Financial source','The case P&L is a supplied FY2025 competition assumption. It is neither audited public accounts nor an xEV-only segment.'],
 ['Reproduction','Run the documented repository cleaning, geography and research scripts. Regenerate this workbook after refreshing the source tables.'],
 ['Missing values','Missing operational inputs remain blank. Dependent financial results display Missing inputs. Numeric zero remains valid.'],
 ['Source register','The repository manifests and evidence index retain complete source paths, acquisition provenance, hashes and original-language records.']
 ];
 rowsTable(s,6,rows.map(r=>({topic:r[0],meaning:r[1]})),['topic','meaning'],['Topic','Definition'],[29,105]);s.getRange('C7:C15').format.wrapText=true;s.getRange('B7:C15').format.rowHeight=46;
}

wb.recalculate();
const inspections={overview:await wb.inspect({kind:'table',range:'Overview!B6:F18',include:'values,formulas',tableMaxRows:15,tableMaxCols:5,maxChars:5000}),economics:await wb.inspect({kind:'table',range:'Economics!C54:F65',include:'values,formulas',tableMaxRows:12,tableMaxCols:4,maxChars:5000}),errors:await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'Formula error scan',maxChars:3000})};
await fs.writeFile(path.join(work,'qa/workbook_inspection.json'),JSON.stringify(inspections,null,2));
// Test a complete zero case, a positive case, missing versus zero, and loss of incrementality.
const e=sheets.Economics;
const tests=[];
for(const base of [6,22,38])e.getRange(`D${base+1}:F${base+7}`).values=Array.from({length:7},()=>[0,0,0]);
wb.recalculate();tests.push({name:'All numeric zeros are valid',actual:e.getRange('D55:F59').values,expected:'all zero'});
e.getRange('D7:D13').values=[[100],[0.2],[1000000],[10000],[0],[2000000],[10000000]];
wb.recalculate();tests.push({name:'Incremental contribution case',actual:e.getRange('D14:D20').values,expected:[20,20000000,1000000,0,3000000,17000000,7000000]});
e.getRange('D11').values=[[50000]];wb.recalculate();tests.push({name:'Capacity displacement is deducted once',actual:e.getRange('D19:D20').values,expected:[12000000,2000000]});
e.getRange('D8').values=[[0]];wb.recalculate();tests.push({name:'Zero incrementality preserves programme and displacement cost',actual:e.getRange('D19:D20').values,expected:[-8000000,-18000000]});
e.getRange('D8').values=[[null]];wb.recalculate();tests.push({name:'Missing incrementality does not become zero',actual:e.getRange('D19:D20').values,expected:['Missing inputs','Missing inputs']});
for(const t of tests){if(t.expected==='all zero')assert(t.actual.flat().every(v=>v===0),t.name);else assert.deepEqual(t.actual.flat(),t.expected,t.name);t.passed=true;}
for(const base of [6,22,38])e.getRange(`D${base+1}:F${base+7}`).values=Array.from({length:7},()=>[null,null,null]);
wb.recalculate();
await fs.writeFile(path.join(work,'qa/economics_formula_tests.json'),JSON.stringify(tests,null,2));

// Render every sheet's opening view with fitted source columns.
const renders={'Overview':'B2:P29','Economics':'C5:F20','Case P&L':'B2:F24','Market access':'B2:H16','Branch portfolio':'B2:J13','Maps cohorts':'B2:L12','YouTube':'B2:G14','Method':'B2:C15'};
for(const [name,range] of Object.entries(renders)){
 const img=await wb.render({sheetName:name,range,scale:1.5,format:'png'});
 await fs.writeFile(path.join(work,'qa',name.replaceAll(' ','_').replaceAll('&','and')+'.png'),new Uint8Array(await img.arrayBuffer()));
}
const file=await SpreadsheetFile.exportXlsx(wb);await file.save(path.join(outputDir,'Auto2000_Integrated_Decision_Workbook.xlsx'));
console.log(JSON.stringify({output:path.join(outputDir,'Auto2000_Integrated_Decision_Workbook.xlsx'),sheets:names,tests},null,2));
