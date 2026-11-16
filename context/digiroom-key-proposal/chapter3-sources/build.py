from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree
from copy import deepcopy
import re,csv,textwrap,json
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as Align
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parents[1];R=B.parents[1];S=Path(__file__).resolve().parent
src=S/'annotated_input.docx'
# Accept the author's text edits; remove review markup for the clean delivery.
with ZipFile(src) as z:
 parts={n:z.read(n) for n in z.namelist()}
root=etree.fromstring(parts['word/document.xml']);ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for e in list(root.xpath('//w:del|//w:commentRangeStart|//w:commentRangeEnd|//w:commentReference',namespaces=ns)):e.getparent().remove(e)
for e in list(root.xpath('//w:ins',namespaces=ns)):
 par=e.getparent();ix=par.index(e)
 for ch in list(e):par.insert(ix,ch);ix+=1
 par.remove(e)
parts['word/document.xml']=etree.tostring(root)
clean=S/'accepted_input.docx'
with ZipFile(clean,'w',ZIP_DEFLATED) as z:
 for n,v in parts.items():
  z.writestr(n,v)
d=Document(clean);old=Document(B/'drafts/Digiroom_KEY_Chapters_1_and_2.docx');serial=10000
# Recover accidental typing in the annotated baseline cell.
for t in d.tables:
 for row in t.rows:
  for c in row.cells:
   if 'ooooooo' in c.text:c.text='Rp9,000bn revenue and Rp3,150bn GP across service, parts and body and paint'
def mark(p,key):
 global serial
 serial+=1;a=OxmlElement('w:bookmarkStart');a.set(qn('w:id'),str(serial));a.set(qn('w:name'),key);b=OxmlElement('w:bookmarkEnd');b.set(qn('w:id'),str(serial));p._p.extend([a,b])
def link(p,label,key):
 h=OxmlElement('w:hyperlink');h.set(qn('w:anchor'),key);r=OxmlElement('w:r');pr=OxmlElement('w:rPr')
 for tag,val in [('color','8F2030'),('u','single')]:
  x=OxmlElement('w:'+tag);x.set(qn('w:val'),val);pr.append(x)
 r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);h.append(r);p._p.append(h)
def write(p,text):
 for part in re.split(r'(\[A\d+\])',text):
  if re.fullmatch(r'\[A\d+\]',part):link(p,'Appendix '+part[1:-1],part[1:-1])
  else:p.add_run(part)
def para(text='',style='normal',before=None):
 p=d.add_paragraph(style=style);write(p,text)
 if before is not None:before.addprevious(p._p)
 return p
def table(headers,rows,before=None):
 t=d.add_table(rows=1,cols=len(headers));t.autofit=False
 for c,v in zip(t.rows[0].cells,headers):c.text=v
 for row in rows:
  for c,v in zip(t.add_row().cells,row):c.text=str(v)
 if before is not None:before.addprevious(t._tbl)
 return t
# Restore editable comparisons rather than raster pictures of prose.
for n,ix in [(2,2),(4,4),(5,5),(9,8),(11,13),(15,17),(16,18)]:
 start=next(p for p in d.paragraphs if p.style.name.startswith('Heading') and re.match(r'^A'+str(n)+r'\s{2}',p.text));el=start._p.getnext()
 while el is not None:
  if el.tag==qn('w:p') and el.xpath('./w:pPr/w:pStyle[contains(@w:val,"Heading")]'):break
  if el.tag==qn('w:p') and el.xpath('.//w:drawing'):
   nxt=el.getnext()
   caption=''.join(nxt.xpath('.//w:t/text()')) if nxt is not None and nxt.tag==qn('w:p') else ''
   if caption.startswith('Evidence comparison.'):
    cp=deepcopy(old.tables[ix]._tbl);el.addprevious(cp);el.getparent().remove(el)
    for ch in list(nxt):
     if ch.tag!=qn('w:pPr'):nxt.remove(ch)
    rp=OxmlElement('w:r');tp=OxmlElement('w:t');tp.text=caption.replace('Evidence comparison. ','');rp.append(tp);nxt.append(rp)
    break
  el=el.getnext()
# Keep reader-facing source labels external or interview-based.
for t in d.tables:
 for row in t.rows:
  for c in row.cells:
   for p in c.paragraphs:
    if 'casebook' in p.text.lower():
     p.text=p.text.replace('The casebook lists booking and tracking in Digiroom.','Digiroom also provides booking and tracking.').replace('The casebook identifies the existing trade-in route via OLXmobbi.','The existing trade-in route connects to OLXmobbi.')
# Detailed issue tree: three branches, nine subproblems, explicit cause layer.
rows=[('BUY','Everyday fit is unclear','Garage clearance, seating and luggage are not checked against the household routine.'),('BUY','Affordability is hard to judge','Running costs, upfront cash and instalments are evaluated separately.'),('BUY','The real drive remains uncertain','Demonstrator availability and the household’s road or charging checks are unconfirmed.'),('SERVICE','The owner chooses another provider','Trust attaches to a particular job; specialist relationships already work.'),('SERVICE','The visit takes extra effort','Uneven job-specific access, unprepared parts and missed symptoms can add trips.'),('SERVICE','Scope or price is rejected','Repair explanations differ and the driver may lack authority for extra spending.'),('UPGRADE','The resale range is not actionable','No inspection-backed buyer commitment or clear offer expiry.'),('UPGRADE','Usable equity is unclear','Payoff, fees, replacement price and finance terms sit in separate steps.'),('UPGRADE','The deal stalls before handover','Appraisal, lender approval, deposits and unit holds run on different timelines.')]
fig,ax=plt.subplots(figsize=(11,7));ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
ax.text(.01,.98,'Business problem',weight='bold',fontsize=12);ax.text(.18,.98,'Branch',weight='bold',fontsize=12);ax.text(.34,.98,'Customer subproblem',weight='bold',fontsize=12);ax.text(.65,.98,'Underlying cause',weight='bold',fontsize=12)
ax.text(.015,.5,'Lost xEV\nsales and\npaid-service\nopportunities',fontsize=12,va='center',weight='bold')
for k,label in enumerate(['BUY','SERVICE','UPGRADE']):
 y=.82-k*.30;ax.text(.18,y,label,color='#8F2030',weight='bold',va='center',fontsize=12);ax.plot([.12,.155,.155,.175],[.5,.5,y,y],color='#52616B',lw=.8)
for i,(_,sub,cause) in enumerate(rows):
 y=.92-i*.10;group=i//3;gy=.82-group*.30
 ax.plot([.265,.30,.30,.33],[gy,gy,y,y],color='#52616B',lw=.7)
 ax.text(.34,y,textwrap.fill(sub,25),va='center',fontsize=11);ax.text(.65,y,textwrap.fill(cause,43),va='center',fontsize=11)
 if i<8:ax.plot([.34,.99],[y-.047,y-.047],color='#D9D9D9',lw=.5)
fig.savefig(S/'full_issue_tree.png',dpi=240,bbox_inches='tight');plt.close(fig)
pic=None
for i,p in enumerate(d.paragraphs):
 if p.text.startswith('Figure 8.'):
  pic=d.paragraphs[i-1];break
for e in list(pic._p):
 if e.tag!=qn('w:pPr'):pic._p.remove(e)
pic.add_run().add_picture(str(S/'full_issue_tree.png'),width=Cm(17))
# Make targeting the transition from diagnosis to solutions.
ch3=next(p for p in d.paragraphs if p.style.name=='Heading 1' and p.text.startswith('CHAPTER III:'))
mark(ch3,'recommendations')
p=para('With these causes in mind, Digiroom KEY targets the Practical Toyota Household: a driver who compares and organises the car, together with the person who approves spending. The research points to shared purchase decisions, successful WhatsApp service habits, and resale research that stops at a price range. The persona brings those findings together across acquisition, service, and upgrade. Its 36–50 age reference reflects the largest Digiroom MAU age band, not the ages of the three interviewees or a measured segment size. [A24]',before=ch3._p)
# Screenshot selectors retain actual captured interface states.
SS=R/'context/digiroom-key/prototype/screenshots';records=list(csv.DictReader(open(SS/'screenshot-index.csv',encoding='utf-8-sig')))
def shot(sid):
 opts=[r for r in records if r['screenshot_id']==sid and 'desktop' in r['capture_type']]
 if not opts:opts=[r for r in records if r['screenshot_id']==sid]
 return SS/opts[0]['png_path']
def image(path,caption,before=None,width=17):
 if str(path).startswith(str(SS)) and before is None:width=14
 p=para(before=before);p.alignment=Align.CENTER;p.paragraph_format.keep_with_next=True;p.add_run().add_picture(str(path),width=Cm(width))
 cap=para(caption,'KEY Figure Caption',before);return cap
# Chapter III standardised structure, two screenshots per pillar.
ch4=next(p for p in d.paragraphs if p.style.name=='Heading 1' and p.text.startswith('CHAPTER IV:'))
shots={'K03':('K-03','Figure 9. The household checks its garage against the selected car.'),'K15':('K-15','Figure 10. Sales confirms the demonstrator, time, and pickup arrangements.'),'E14':('E-14','Figure 11. The workshop confirms parts and the service slot.'),'E21':('E-21','Figure 12. The payer reviews the current estimate before added work proceeds.'),'Y04':('Y-04','Figure 13. The upgrade adviser brings the written offer, payoff, and fees together.'),'Y06':('Y-06','Figure 14. The owner reviews the current replacement terms.')}
for line in (S/'chapter3.txt').read_text().splitlines():
 if not line.strip():continue
 if line.startswith('@'):
  sid,caption=shots[line[1:]];
  if line[1:] in ['K03','E21','Y06']:
   caption=caption.replace('Figure 12.','Figure 10.').replace('Figure 14.','Figure 11.')
   image(shot(sid),caption+' Source: Digiroom KEY interface capture; sample transaction records.',ch4._p,width=15)
 elif line.startswith('### '):para(line[4:],'Heading 3',ch4._p)
 elif line.startswith('## '):p=para(line[3:],'normal',ch4._p);p.runs[0].bold=True;p.paragraph_format.keep_with_next=True
 elif line.startswith('# '):p=para(line[2:],'Heading 2',ch4._p);mark(p,'solution_'+str(len(d.element.xpath('.//w:bookmarkStart'))))
 else:para(line,before=ch4._p)
# Appendix helpers.
def app(n,title,note=''):
 p=para(f'A{n}  {title}','Heading 2');mark(p,'A'+str(n));p=para();link(p,'Return to recommendations','recommendations');p.add_run('  |  ');link(p,'Appendix index','appendix_index');p.paragraph_format.keep_with_next=True
 if note:para(note)
def flow(title,steps,name):
 fig,ax=plt.subplots(figsize=(9,2.4));ax.axis('off')
 for i,(a,b) in enumerate(steps):
  x=.02+i*.245;ax.text(x,.85,a,fontsize=12,color='#8F2030',weight='bold');ax.text(x,.67,textwrap.fill(b,18),fontsize=12,va='top')
  if i<3:ax.annotate('',xy=(x+.235,.78),xytext=(x+.20,.78),arrowprops={'arrowstyle':'->','color':'#52616B'})
 ax.set_title(title,loc='left',fontsize=13,pad=18);fig.savefig(S/(name+'.png'),dpi=220,bbox_inches='tight');plt.close(fig);return S/(name+'.png')
app(24,'The Practical Toyota Household','Research-informed composite persona. Source: supplied persona artwork, owner interviews, and Digiroom audience baseline. This is a design synthesis, not a fourth interview participant or a representative market estimate.')
image(S/'persona.png','Figure A24.1. The target household across buying, service, and replacement.')
table(['Persona element','Research basis','Design implication'],[['Driver and payer roles','Yaris Q02/Q06; Wuling Q02','Share the current decision with the person authorised to act.'],['WhatsApp for service','Yaris Q09; Wuling Q09','Preserve assisted entry; add useful status and approval.'],['Resale research','Yaris Q10; Atto N5/N6 contrast','Carry a price range into an inspected offer.'],['36–50 reference; 41% MAU','Digiroom audience baseline','Audience context only; interviews do not validate this age segment.']])
app(25,'Technology stack and implementation boundary')
table(['Layer','Demonstrated stack','Role'],[['Application','React 19; TypeScript; Vite 7','Responsive interface and typed domain logic.'],['3D studio','Three.js; React Three Fiber; Drei','Vehicle, garage and cabin scenes.'],['Maps','Leaflet; OpenStreetMap tiles; bundled atlas','Job-specific workshop comparisons with tile fallback.'],['Sharing and display','QR code; LZ String; Lucide icons','Visit brief sharing and interface presentation.'],['State','Browser localStorage; journey state transitions','One active case per journey in the sample account.'],['Verification tooling','Vitest; Testing Library; Playwright','Unit and browser checks reported in the prototype handoff.']])
para('Source: Digiroom KEY application source and build handoff. Package versions describe the supplied implementation, not a claim about the latest software releases.')
app(26,'Production integrations and transaction architecture')
image(flow('From customer action to an accountable outcome',[('Customer','Prepare, request, review, approve.'),('Case service','Store identity, stage, version and permission.'),('Branch systems','Confirm stock, parts, slot and work.'),('Finance','Reconcile payment, settlement and delivery.')],'architecture'),'Figure A26.1. Proposed production architecture; system interfaces require implementation.')
table(['Integration','Record exchanged','Confirmation owner'],[['Identity and CRM','Customer, vehicle, consent and access grants','Digital and CRM'],['Dealer operations','Demonstrator, unit hold, slot, parts and work order','Sales or service adviser'],['Appraisal and lending','Inspected offer, payoff, validity and finance decision','Appraiser and lender'],['Payments and settlement','Receipt, deposit, refund, old-loan settlement','Authorised finance operator']])
para('The current interface uses local sample records. Live identity, cross-device approval, appointments, inventory, lending, messaging and payments are production integrations; no active third-party connection is implied by a screenshot.')
app(27,'Research preparation and source separation')
image(flow('Public-account and interview evidence preparation',[('Retain','Preserve source cohort, date and original language.'),('Deduplicate','Use platform IDs; retain collection membership.'),('Interpret','Read relevant episodes and counterexamples.'),('Apply','Link the scoped finding to a design decision.')],'research'),'Figure A27.1. Evidence preparation; records remain separate from customer and transaction counts.')
# Detailed screenshot appendix, two complementary states per exhibit.
exhibits=[(28,'Household garage and cabin checks',['K-03','K-06'],'Garage clearance and passenger configuration make household questions explicit.'),(29,'Weekly costs and household quote',['K-09','K-23'],'Charging inputs and the household quote address different parts of affordability.'),(30,'Drive availability and confirmation',['K-14','K-15'],'The adviser checks availability before the household relies on a drive.'),(31,'Drive results and delivery progression',['K-19','K-30'],'Saved household results carry into the dated offer and delivery record.'),(32,'Eligible outlets and job selection',['E-01','E-02'],'The same Bandung origin set is compared with and without eligible OtoXpert destinations.'),(33,'Workshop readiness and customer confirmation',['E-14','E-15'],'The adviser confirms resources and the customer sees the agreed slot. The workflow in A41 defines arrival acknowledgement.'),(34,'Payer approval and estimate changes',['E-21','E-22'],'The current estimate and the recorded decision remain tied to a version.'),(35,'Service completion and receipt',['E-26','E-27'],'Collection and payment close the accepted work; unresolved items retain a next action.'),(36,'Inspection request and written offer',['Y-01','Y-04'],'A market indication moves to an inspected offer with payoff and fees.'),(37,'Net equity and current upgrade terms',['Y-04','Y-06'],'Sample amounts distinguish the offer, loan payoff, fees and usable equity.'),(38,'Replacement reservation and owner decision',['Y-05','Y-07'],'Adviser commitments and owner acceptance refer to the current deal.'),(39,'Settlement and replacement delivery',['Y-10','Y-11'],'The record follows settlement and handover through to replacement delivery.')]
for n,title,ids,note in exhibits:
 app(n,title)
 for j,sid in enumerate(ids,1):
  image(shot(sid),f'Figure A{n}.{j}. '+next(r['suggested_caption'] for r in records if r['screenshot_id']==sid)+' Source: captured Digiroom KEY interface; sample records.')
 para(note)
app(40,'Commercial outcomes and KPI definitions')
table(['Journey','Outcome and denominator','Supporting measures'],[['Know Your Fit','Additional delivered xEVs to customers new to Auto2000; eligible acquisition opportunities','Confirmed and completed drives; offers; delivery conversion; demonstrator cost.'],['Easy Service','Additional completed customer-paid work orders per eligible paid/mixed opportunity','Readiness; approval time; rework; adviser time; independent-workshop recovery.'],['Your Next Toyota','Additional repeat xEV deliveries among eligible existing customers','Inspections; accepted offers; reserved units; settled deals; refunds.'],['Useful digital return','Voluntary revisit for a distinct ownership task','Confirmation review; current approval; completion record; subsequent decision.']])
para('Count each delivery or work order once across channels. Separate new-to-Auto2000 from first Toyota or first xEV, and covered service from customer-paid work. Numerical targets and GP assumptions are reserved for Chapter IV.')
app(41,'Operating workflows and decision rights')
for name,steps in [('Acquisition',[('Household','Save routine and drive questions.'),('Sales','Confirm car, time and handovers.'),('Buyer','Review dated quote and finance.'),('Delivery','Record fulfilled retail purchase.')]),('Service',[('Owner','Choose job and eligible outlet.'),('Workshop','Confirm resources and estimate.'),('Payer','Approve the current scope.'),('Handover','Reconcile work and receipt.')]),('Replacement',[('Appraiser','Issue inspected buy offer.'),('Lender','Confirm payoff and finance.'),('Sales','Hold replacement; align dates.'),('Settlement','Reconcile both handovers.')])]:
 image(flow(name,steps,name.lower()),name+' workflow. Roles confirm the states they control.')
app(42,'Permissions and exception controls')
table(['Event','Required control','Customer response'],[['Extra work','Approve the current estimate version before starting','Approve, decline or retain original scope.'],['Shared payer link','Purpose-limited access; identity check; expiry and revocation','Review only relevant work and charges.'],['Unavailable demonstrator','Check calendar; offer alternate model-matched slot','Accept another time or drive format.'],['Expired appraisal or lost unit','Invalidate old terms and disclose refund route','Review revised terms or pause.'],['Unavailable map tiles','Use bundled geography and outlet list','Inspect the same modelled comparison without live tiles.']])
app(43,'Drive eligibility and stale approval exceptions')
for sid in ['X-04','X-19']:
 image(shot(sid),next(r['suggested_caption'] for r in records if r['screenshot_id']==sid)+' Source: captured Digiroom KEY interface; sample records.')
# Compact appendix index additions.
index_anchor=next(p for p in d.paragraphs if p.text.startswith('A1  Aftersales'))
for n,title in [(24,'Customer persona'),(25,'Technology stack'),(26,'Production integrations'),(27,'Research preparation')]+[(n,t) for n,t,_,_ in exhibits]+[(40,'KPI definitions'),(41,'Operating workflows'),(42,'Access and exceptions'),(43,'Exception screenshots')]:
 p=para(before=index_anchor._p);link(p,f'A{n}  {title}','A'+str(n))
# Apply exact formatting preferences to all final objects.
app_started=False
for p in d.paragraphs:
 if p.text=='APPENDICES':app_started=True
 pf=p.paragraph_format;pf.space_after=Pt(0);pf.space_before=Pt(0)
 if p.style.name.startswith('Heading'):
  pf.space_before=Pt(6);pf.space_after=Pt(6);pf.keep_with_next=True
 elif p.style.name=='KEY Figure Caption':pf.space_after=Pt(3);pf.first_line_indent=Cm(0)
 elif p._p.xpath('.//w:drawing'):pf.first_line_indent=Cm(0);pf.keep_with_next=True;pf.space_before=Pt(3)
 elif p.text.startswith(('Return to','Interview ')):pf.first_line_indent=Cm(0);pf.keep_with_next=True
 else:
  pf.first_line_indent=Cm(.75) if p.text and not p.text.startswith(('Figure ','Source:','Sources:','Exhibit ','A1 ','A2 ')) else Cm(0)
  pf.alignment=Align.JUSTIFY
 for r in p.runs:
  r.font.name='Times New Roman'
  if not p.style.name.startswith('Heading'):r.font.size=Pt(12)
# Appendix tables: ten point, full grid, repeated headers.
for t in d.tables:
 pr=t._tbl.tblPr
 for e in list(pr.findall(qn('w:tblBorders'))):pr.remove(e)
 borders=OxmlElement('w:tblBorders')
 for side in ['top','bottom','left','right','insideH','insideV']:
  e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'9EA7AD');borders.append(e)
 pr.append(borders)
 for i,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  if i==0:row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
  for c in row.cells:
   c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for p in c.paragraphs:
    p.alignment=Align.LEFT;p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.space_after=Pt(2);p.paragraph_format.space_before=Pt(2)
    for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(10);r.bold=i==0
for t in d.tables:
 for r in t._tbl.xpath('.//w:r'):
  pr=r.get_or_add_rPr();sz=pr.find(qn('w:sz'))
  if sz is None:sz=OxmlElement('w:sz');pr.append(sz)
  sz.set(qn('w:val'),'20')
# Remove inherited TOC and regenerate from final headings; page numbers updated after render.
toc=d.paragraphs[0];el=toc._p.getnext()
while el is not None and ''.join(el.xpath('.//w:t/text()'))!='EXECUTIVE SUMMARY':
 nxt=el.getnext();el.getparent().remove(el);el=nxt
cursor=toc._p
entries=[]
for p in list(d.paragraphs):
 if p._p is toc._p:continue
 if p.style.name=='Heading 1' or (p.style.name=='Heading 2' and p.text in ['Solution Overview','1. Know Your Fit','2. Easy Service','3. Your Next Toyota']):
  keys=p._p.xpath('./w:bookmarkStart');key=keys[0].get(qn('w:name')) if keys else 'toc_'+str(len(entries));
  if not keys:mark(p,key)
  entries.append((p.text,key))
for label,key in entries:
 p=para();link(p,label,key);p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.space_after=Pt(4);cursor.addnext(p._p);cursor=p._p
# Capture headings/styles after author's corrections; full tree is linked to detailed evidence.
for pp in d.paragraphs:
 if pp.text.startswith('Source: anonymised') and 'driver interview' in pp.text and 'Atto' not in pp.text:
  pp.text=pp.text.replace('anonymised  driver','anonymised BYD Atto driver')
d.core_properties.title='Digiroom KEY Chapters 1 to 3';d.core_properties.comments=''
OUT=B/'drafts/Digiroom_KEY_Chapters_1_to_3.docx';d.save(OUT)
print('Saved',OUT,'chapter words',len((S/'chapter3.txt').read_text().split()))
