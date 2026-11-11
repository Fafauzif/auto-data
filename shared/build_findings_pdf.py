"""Build the readable research book from curated reports and structured cards.
No external retrieval. Intermediate renders must remain outside the release.
"""
from pathlib import Path
import re,json,csv,html,hashlib,datetime
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,KeepTogether,CondPageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
PDF=OUT/'Auto2000_Research_Findings.pdf'
FONT=Path('/usr/share/fonts/truetype/open-sans')
for name,filename in [('Body','OpenSans-Regular.ttf'),('Bold','OpenSans-Bold.ttf'),('Italic','OpenSans-Italic.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/filename)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
NAVY=colors.HexColor('#244A68');ORANGE=colors.HexColor('#A65E31');GRAY=colors.HexColor('#536575');LIGHT=colors.HexColor('#EEF3F6')
styles=getSampleStyleSheet()
for name in styles.byName:
 styles[name].fontName='Body';styles[name].textColor=colors.HexColor('#17232C')
styles.add(ParagraphStyle(name='BodyTextBook',fontName='Body',fontSize=10.2,leading=14.5,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallBook',fontName='Body',fontSize=8.2,leading=11.4,spaceAfter=5,textColor=GRAY))
styles.add(ParagraphStyle(name='TableBook',fontName='Body',fontSize=8.2,leading=11.3,spaceAfter=1))
styles.add(ParagraphStyle(name='TableHeadBook',fontName='Bold',fontSize=8.4,leading=11.4,textColor=colors.white))
styles.add(ParagraphStyle(name='ChapterBook',fontName='Bold',fontSize=19,leading=24,spaceBefore=8,spaceAfter=15,keepWithNext=True,textColor=NAVY))
styles.add(ParagraphStyle(name='SectionBook',fontName='Bold',fontSize=13.1,leading=17,spaceBefore=12,spaceAfter=8,keepWithNext=True,textColor=NAVY))
styles.add(ParagraphStyle(name='SubBook',fontName='Bold',fontSize=10.7,leading=14.2,spaceBefore=9,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='CoverTitleBook',fontName='Bold',fontSize=31,leading=38,textColor=NAVY,spaceAfter=24))
styles.add(ParagraphStyle(name='CoverSubBook',fontName='Body',fontSize=15,leading=22,spaceAfter=18,textColor=GRAY))
styles.add(ParagraphStyle(name='TOCBook',fontName='Body',fontSize=10,leading=14,spaceBefore=7,spaceAfter=5,leftIndent=0,firstLineIndent=0,rightIndent=25))
styles.add(ParagraphStyle(name='BulletBook',parent=styles['BodyTextBook'],leftIndent=10,firstLineIndent=-8,bulletIndent=0))
for name in ('BodyTextBook','SmallBook','BulletBook'):
 styles[name].allowWidows=0;styles[name].allowOrphans=0
W,H=A4;M=45;CW=W-2*M;story=[];chapters=[];input_files=[]
def clean(s):
 s=str(s).replace('\u2014',', ').replace('\u2013','-').replace('\u2011','-').replace('\u00a0',' ')
 s=s.replace('\u2192',' to ').replace('\u2194',' versus ').replace('\u2212','-')
 s=re.sub(r'\b(of|for|including|from|than|within|above|below|over|under)(?=\d)',r'\1 ',s)
 s=re.sub(r'\b(returned|HTTP|PDF|page|Figure|Table)(?=\d)',r'\1 ',s)
 s=re.sub(r'(\d)(?=months\b|years\b|remaining\b|rows\b|individuals\b|respondents\b|million\b)',r'\1 ',s)
 return s
def inline(s):
 s=html.escape(clean(s));s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s);s=re.sub(r'`([^`]+)`',r'\1',s)
 s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',lambda m:f'<link href="{m.group(2)}" color="#244A68">{m.group(1)}</link>',s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1 (\2)',s)
 return s
def p(s,style='BodyTextBook'):
 obj=Paragraph(inline(s),styles[style]);story.append(obj);return obj
def labeled(label,text,style='BodyTextBook'):return p('**'+label+'** '+str(text),style)
def chapter(title):
 if story:story.append(PageBreak())
 q=p(title,'ChapterBook');q._chapter_number=len(chapters)+1;chapters.append(title)
def figure(path,caption):
 path=Path(path)
 if not path.exists():raise FileNotFoundError(path)
 im=Image(str(path));scale=min(CW/im.imageWidth,350/im.imageHeight);im.drawWidth=im.imageWidth*scale;im.drawHeight=im.imageHeight*scale
 story.append(KeepTogether([Spacer(1,5),im,Paragraph(inline(caption),styles['SmallBook']),Spacer(1,7)]));input_files.append(path)
def table(rows):
 if not rows:return
 n=len(rows[0])
 if n>5:
  # Wide source records become readable cards instead of tiny column grids.
  for row in rows[1:]:
   p(str(row[0]),'SubBook')
   for key,val in zip(rows[0][1:],row[1:]):labeled(key,val)
  return
 widths=[CW/n]*n
 if n==3:widths=[CW*.23,CW*.45,CW*.32]
 if n==2:widths=[CW*.30,CW*.70]
 cells=[[Paragraph(inline(c),styles['TableHeadBook' if i==0 else 'TableBook']) for c in row] for i,row in enumerate(rows)]
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1,splitInRow=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#D8E0E6')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.extend([t,Spacer(1,10)])
def md(path,skip_first_title=True):
 path=Path(path);input_files.append(path);lines=path.read_text().splitlines();i=0;buffer=[];fence=False
 def flush():
  if buffer:p(' '.join(buffer));buffer.clear()
 while i<len(lines):
  line=lines[i].strip()
  if line.startswith('```'):flush();fence=not fence;i+=1;continue
  if fence:
   if line:p(line,'SmallBook')
   i+=1;continue
  if line.startswith('|'):
   flush();rows=[]
   while i<len(lines) and lines[i].lstrip().startswith('|'):
    cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
    if not all(set(c)<=set('-: ') for c in cells):rows.append(cells)
    i+=1
   if rows and all(len(row)==len(rows[0]) for row in rows):table(rows)
   else:
    for row in rows:p(' | '.join(row),'SmallBook')
   continue
  if line.startswith('!['):
   flush();m=re.match(r'!\[(.*?)\]\((.*?)\)',line)
   if m:figure((path.parent/m.group(2)).resolve(),m.group(1))
  elif line.startswith('# '):
   flush()
   if not skip_first_title:p(line[2:],'SectionBook')
   skip_first_title=False
  elif line.startswith('## '):flush();p(line[3:],'SectionBook')
  elif line.startswith('### '):flush();p(line[4:],'SubBook')
  elif line.startswith(('- ','* ')):flush();p('- '+line[2:],'BulletBook')
  elif not line:flush()
  else:buffer.append(line)
  i+=1
 flush()
class Book(SimpleDocTemplate):
 def afterFlowable(self,flow):
  if isinstance(flow,Paragraph) and hasattr(flow,'_chapter_number'):
   key='chapter-'+str(flow._chapter_number);self.canv.bookmarkPage(key);self.canv.addOutlineEntry(flow.getPlainText(),key,0)
   self.notify('TOCEntry',(0,flow.getPlainText(),self.page,key))
def furniture(c,d):
 c.saveState();c.setStrokeColor(colors.HexColor('#D9E3EA'));c.setLineWidth(.6)
 if d.page>1:
  c.line(M,H-29,W-M,H-29);c.setFont('Body',8);c.setFillColor(GRAY);c.drawString(M,H-21,'AUTO2000 DIGIROOM  |  RESEARCH FINDINGS')
 c.setFont('Body',8);c.setFillColor(GRAY);c.drawString(M,24,'Public-source research | 11 November 2026');c.drawRightString(W-M,24,str(d.page));c.restoreState()
def build():
 p('AUTO2000 DIGIROOM','CoverTitleBook')
 p('Research findings, original analyses and open strategic choices','CoverSubBook')
 p('A readable guide to the complete evidence package','SectionBook')
 p('Prepared 11 November 2026. Covers sales, service, spare parts, body and paint; separates HEV, PHEV and BEV; preserves the user\'s choice among solutions.')
 p('The main conclusion is more precise than a call for more app activity: existing capabilities need to be evaluated at consequential customer decisions and operational handoffs. Public evidence can locate plausible gaps and reject blanket assumptions. It does not establish an incremental profit effect.')
 p('The large raw appendices contain auxiliary research data as well as direct automotive evidence. Their rows, repeated label views, time-series measurements and derived calculations are different units. They are never presented as millions of independent Auto2000 customers.')
 p('Observation confidence is stated locally. Mechanisms, transferability and commercial effects retain their uncertainty. No implementation, rollout or winning strategy is selected.','SmallBook')
 chapter('Reading route and contents')
 p('Read the executive synthesis and core findings first. The deeper analyses show which conclusions changed under additional tests. The insight and solution catalogues are reference sections; each keeps its counterevidence and limits. Raw files, code, manifests and the extensive master AI context are in the accompanying ZIP.')
 toc=TableOfContents();toc.levelStyles=[styles['TOCBook']];story.append(toc)
 chapter('What changed after the deeper tests')
 md(ROOT/'reports/EXTENSION_SYNTHESIS.md')
 chapter('Core findings and business diagnosis')
 md(ROOT/'reports/RESEARCH_REPORT.md')
 chapter('MECE accounting and mechanism counterevidence')
 md(ROOT/'workstreams/extension_hypotheses/REPORT.md')
 chapter('Review evidence: cohorts, dates and attribution')
 md(ROOT/'workstreams/extension_reviews/EXTENSION_REVIEW_REPORT.md')
 chapter('Charging geography: robustness and boundary corrections')
 md(ROOT/'workstreams/extension_geography/GEOGRAPHY_ROBUSTNESS_REPORT.md')
 for name,caption in [('01_nearest_candidate_robustness.png','Original sensitivity analysis: candidate filtering changes close-range proximity.'),('02_boundary_ratio_sensitivity.png','Original boundary-alignment sensitivity. Ratios use all passenger-car stock, not BEV demand.'),('03_units_and_point_locations.png','Source units and location clustering are different measurements.')]:figure(ROOT/'workstreams/extension_geography'/name,caption)
 chapter('Website, mobile and ownership journeys')
 md(ROOT/'workstreams/extension_journeys/EXTENSION_JOURNEY_REPORT.md')
 chapter('Commercial logic, entitlements and retained risk')
 md(ROOT/'workstreams/extension_economics/EXTENSION_ECONOMICS_REPORT.md')
 for name,caption in [('portfolio_shapley_bridge.png','Symmetric accounting decomposition, not causal attribution.'),('dated_service_estimate_comparison.png','Published dated service estimates under matched ordinal occasions. These are not realized invoices or dealer margins.')]:figure(ROOT/'workstreams/extension_economics/figures'/name,caption)
 chapter('Lifecycle coverage, decision rights and existing alternatives')
 md(ROOT/'workstreams/extension_stakeholders/MECE_STAKEHOLDER_REPORT.md')
 chapter('Battery telemetry: observed signals and hidden health references')
 md(ROOT/'workstreams/extension_battery/BATTERY_TELEMETRY_REPORT.md')
 for path in sorted((ROOT/'workstreams/extension_battery').glob('*.png')):figure(path,'Original analysis of the explicitly selected auxiliary telemetry subset. See figure and chapter for signal units and limits.')
 chapter('Sixteen cross-source insight cards')
 data=json.loads((ROOT/'reports/INSIGHT_BOOK.json').read_text());input_files.append(ROOT/'reports/INSIGHT_BOOK.json')
 p('These preserve the first-wave insight cards. The preceding extension chapters qualify them where new tests changed the interpretation, especially geographic convenience and lifecycle coverage. Observation certainty does not transfer automatically to the possible mechanism.')
 for x in data['insights']:
  story.append(CondPageBreak(160));p(x['insight_id']+' | '+x['title'],'SectionBook')
  labeled('Observation.',x['scoped_observation']);labeled('Possible mechanism.',x['possible_mechanism']);labeled('Strongest rival.',x['strongest_rival_or_counterevidence']);labeled('Conditional implication.',x['conditional_business_implication'])
  labeled('Limits.',' '.join(x['limits']),'SmallBook');labeled('Confidence.',x['observation_confidence']+' '+x['mechanism_confidence'],'SmallBook');labeled('Evidence references.',', '.join(x['evidence_refs']),'SmallBook')
 chapter('Twenty-seven solution concepts for your choice')
 data=json.loads((ROOT/'reports/SOLUTION_MENU.json').read_text());input_files.append(ROOT/'reports/SOLUTION_MENU.json')
 p('These are the 27 consolidated first-wave concepts, organized into seven families. They are alternatives and coordination or contract layers, not 27 additive profit pools. The extension lifecycle review adds a separately identified recall-related research candidate and documents other coverage gaps. None is selected as a winner.')
 family=None
 for x in data['options']:
  if x['family']!=family:family=x['family'];p(family,'SectionBook')
  story.append(CondPageBreak(145));p(x['solution_id']+' | '+x['title'],'SubBook');labeled('Customer decision.',x['customer_question']);labeled('Existing baseline.',x['existing_capability_baseline']);labeled('Possible addition.',x['specific_possible_difference']);labeled('Rival and failure condition.',x['strongest_rival']+' '+x['failure_condition']);labeled('Decision-owner tradeoff.',x['stakeholder_tradeoff']);labeled('Commercial test.',x['conditional_commercial_mechanism']+' '+x['record_costs_and_gp']);labeled('Dependency.',x['critical_dependency'],'SmallBook').keepWithNext=True;labeled('Evidence.',', '.join(x['support_evidence_ids'])+'; boundaries: '+', '.join(x['counter_or_boundary_evidence_ids']),'SmallBook')
 chapter('Data, reproduction and limits')
 md(ROOT/'DATA_GUIDE.md')
 p('Archive variants and privacy','SectionBook');md(ROOT/'README_PUBLIC_MIRROR.md')
 p('Quality-control boundary','SectionBook');p('Arithmetic, references, hashes and document rendering were checked by AI agents. No human annotation, field visit, customer interview, completed live booking, private vehicle-record access or causal Auto2000 experiment is claimed. Numerical pass counts describe assertions checked; they are not a validation score for the commercial mechanism.')
 p('Open the complete context pack for continuation','SectionBook');p('context/Auto2000_Master_AI_Context_Updated.md preserves the full working context, source and file map, changes to the original friend hypotheses, detailed evidence capsules and unresolved questions. It is deliberately more extensive than this readable report. The original supplied context is marked as historical, with current conclusions taking precedence.')
 book=Book(str(PDF),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=47,bottomMargin=43,title='Auto2000 Digiroom research findings',author='Research synthesis',subject='Public-source diagnosis, robustness analyses and open solution choices')
 book.multiBuild(story,onFirstPage=furniture,onLaterPages=furniture)
 from pypdf import PdfReader
 reader=PdfReader(str(PDF));text='\n'.join(pg.extract_text() or '' for pg in reader.pages)
 assert len(reader.pages)>15 and all((pg.extract_text() or '').strip() for pg in reader.pages)
 receipt={'file':str(PDF.relative_to(ROOT)),'pages':len(reader.pages),'words_extracted':len(text.split()),'bytes':PDF.stat().st_size,'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'chapters':chapters,'input_files':[str(f.relative_to(ROOT)) for f in input_files],'all_pages_have_text':True,'visual_inspection_pending':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (ROOT/'reports/PDF_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({k:v for k,v in receipt.items() if k not in ('input_files','chapters')}))
if __name__=='__main__':build()
