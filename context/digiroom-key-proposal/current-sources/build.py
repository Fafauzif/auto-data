from pathlib import Path
from copy import deepcopy
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as Align
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
import re,csv
W=Path('draft_work')
d=Document(next(Path('upload').glob('*MKPR*')))
source=list(d.paragraphs)
toc=d._element.body.find(qn('w:sdt'))
head=[source[i].text for i in range(26,41,2)]
head[0]=head[0].removesuffix('4')
head[-1]=head[-1].removeprefix('1. ')
head[5]='A Toyota sold in early 2026 can reach its first paid scheduled service after the investment window closes, so near-term paid work starts with eligible cars already on the road.'
anchor=source[43]
for ix in list(range(1,19))+list(range(20,43))+list(range(46,51))+list(range(52,70))+[71]:
 elem=source[ix]._element
 if elem.getparent() is not None:elem.getparent().remove(elem)
for section in d.sections:
 section.top_margin,section.bottom_margin,section.left_margin,section.right_margin=Cm(4),Cm(3),Cm(2),Cm(2)
from docx.enum.style import WD_STYLE_TYPE
d.styles.add_style('KEY Figure Caption',WD_STYLE_TYPE.PARAGRAPH)
caption=d.styles['KEY Figure Caption']
caption.base_style=d.styles['normal']
caption.font.italic=True
caption.paragraph_format.space_after=Pt(6)
import re
d.core_properties.title='Digiroom KEY | Auto2000'
d.core_properties.subject='IBSC 2026 semifinal proposal'
d.core_properties.author=''
red='8F2030';gray='53626B'; idx=2000
def mark(p,key):
 global idx
 idx+=1
 n=OxmlElement('w:bookmarkStart');n.set(qn('w:id'),str(idx));n.set(qn('w:name'),key)
 e=OxmlElement('w:bookmarkEnd');e.set(qn('w:id'),str(idx))
 p._p.insert(1 if p._p.pPr is not None else 0,n);p._p.append(e)
def hlink(p,t,key=None,url=None):
 h=OxmlElement('w:hyperlink')
 if key:h.set(qn('w:anchor'),key)
 if url:h.set(qn('r:id'),p.part.relate_to(url,RELATIONSHIP_TYPE.HYPERLINK,is_external=True))
 r=OxmlElement('w:r');pr=OxmlElement('w:rPr');c=OxmlElement('w:color');c.set(qn('w:val'),red);pr.append(c)
 u=OxmlElement('w:u');u.set(qn('w:val'),'single');pr.append(u)
 r.append(pr);v=OxmlElement('w:t');v.text=t;r.append(v);h.append(r);p._p.append(h)
def p(t='',sty='normal',template=None):
 a=anchor.insert_paragraph_before(style=sty) if anchor is not None else d.add_paragraph(style=sty)
 if template is not None and template._p.pPr is not None:
  if a._p.pPr is not None:a._p.remove(a._p.pPr)
  a._p.insert(0,deepcopy(template._p.pPr))
 for piece in re.split(r'(\[A\d+\])',t):
  if re.fullmatch(r'\[A\d+\]',piece):
   key=piece[1:-1];hlink(a,'Appendix '+key,key)
  else:
   run=a.add_run(piece)
   if template is not None and template.runs and template.runs[0]._r.rPr is not None:
    run._r.insert(0,deepcopy(template.runs[0]._r.rPr))
 return a
def title(t,key=None,lvl=1,new=False,template=None):
 a=p(t,'Heading '+str(lvl),template)

 if key:mark(a,key)
 return a
def picture(n,cap,width=16.45):
 a=p();a.alignment=Align.CENTER;a.paragraph_format.space_after=Pt(3);a.paragraph_format.keep_with_next=True
 a.add_run().add_picture(str(W/'charts'/f'{n}.png'),width=Cm(width))
 z=p(cap,'KEY Figure Caption');z.paragraph_format.space_after=Pt(7)
 for r in z.runs:r.italic=True
 return z
def table(labels,rows,ws,nums=()):
 t=d.add_table(rows=0,cols=len(labels));t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for c,w in zip(t.columns,ws):c.width=Cm(w)
 for i,items in enumerate([labels,*rows]):
  row=t.add_row()
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  if i==0: row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
  for j,(c,v,w) in enumerate(zip(row.cells,items,ws)):
   c.width=Cm(w);q=c.paragraphs[0];q.alignment=Align.RIGHT if j in nums else Align.LEFT
   q.paragraph_format.space_before=Pt(3);q.paragraph_format.space_after=Pt(3)
   rr=q.add_run(str(v));rr.bold=i==0
   if i==0:
    k=OxmlElement('w:shd');k.set(qn('w:fill'),'F3E8EA');c._tc.get_or_add_tcPr().append(k)
   else:
    k=OxmlElement('w:tcBorders');z=OxmlElement('w:bottom');z.set(qn('w:val'),'single');z.set(qn('w:sz'),'4');z.set(qn('w:color'),'E0E4E6');k.append(z);c._tc.get_or_add_tcPr().append(k)
 if anchor is not None:anchor._p.addprevious(t._tbl)
 return t
mark(source[51],'references')
def preserve(i,key=None,new=False):
 a=source[i]
 anchor._p.addprevious(a._p)

 if key:mark(a,key)
 return a
preserve(20,'intro',True)
preserve(21)
sections=(W/'body.txt').read_text().strip().split('\n@\n')
def body(t,template):
 a=p(t,'normal',template)
 a.style=d.styles['normal']
 a.paragraph_format.keep_with_next=False
 a.paragraph_format.keep_together=False
 a.paragraph_format.alignment=Align.JUSTIFY
 return a
for para in sections[0].splitlines():body(para,source[22])
preserve(23)
body('Auto2000 needs Digiroom to help buyers choose an xEV, help owners finish eligible service work, and make the next Toyota easier to buy. Each is a distinct customer decision with a completed transaction at the end.',source[24])
preserve(25,'analysis',True)
depth=(W/'analysis_depth.txt').read_text().strip().split('\n@\n')
caps=[
 'Figure 1. Booking channels and Digiroom activity. Activity is measured among monthly active users (IBSC, 2026, p. 11).',
 'Figure 2. Reported workshop handoffs and the record that brings the job to completion. [A4]',
 'Figure 3. Selected accounts illustrate household fit and vehicle availability. [A5]',
 'Figure 4. Dated credit-calculator comparison for the Innova Zenix 2.0 G Hybrid. [A6]',
 'Figure 5. Four-market comparison against the same oil-service benchmark. [A7]',
 'Figure 6. Time-only example for an eligible January 2026 delivery. [A10]',
 'Figure 7. Sample deal terms and sequence from appraisal to settlement. [A12]',
 'Figure 8. Consolidated issue tree for acquisition, service and replacement. [A13]']
for i,(h,b,c) in enumerate(zip(head,sections[1:],caps),1):
 title(h,'claim'+str(i),lvl=2,new=i in (3,5,7,8),template=source[24+i*2])
 body(b.strip(),source[25+i*2])
 picture('f'+str(i),c)
 body(depth[i-1].strip(),source[25+i*2])
 if i==7:
  table(['The owner has','The decision still open','What resolves it'],[
   ['A market price range','Is there a buyer at that price?','An inspected buy offer with conditions and expiry.'],
   ['An inspected offer','How much can I put toward the replacement?','Official payoff, applicable fees and the dated amount due.'],
   ['An acceptable deal','Will the exact car be there when the offer is settled?','A reserved unit, aligned dates and an adviser who tracks both handovers.'],
  ],[4.05,5.85,7.1])
  p('The adviser needs three confirmations from different parties: the used-car buyer confirms the offer, the lender confirms payoff, and sales confirms the replacement unit. When one changes, the owner needs the revised terms before accepting or paying a deposit.')
 if i==8:
  body('One customer-visible record can carry the decision across Digiroom, WhatsApp and the branch. Count the first xEV delivered to a new Auto2000 customer, the completed eligible paid work order, and the repeat xEV delivery separately. Each can then be matched to a transaction Auto2000 can recognize.',source[41])
anchor=source[70]
def ref(author,year,work,url=None,extra=''):
 a=p();a.alignment=Align.LEFT;a.paragraph_format.left_indent=Cm(.65);a.paragraph_format.first_line_indent=Cm(-.65)
 a.add_run(f'{author}. ({year}). ');a.add_run(work).italic=True;a.add_run('.'+(' '+extra if extra else ''))
 if url:a.add_run(' ');hlink(a,url,url=url)
ref('Auto2000','n.d.','All New Kijang Innova Zenix Hybrid 2026 harga terbaru, spesifikasi dan promo','https://auto2000.co.id/mobil-baru-toyota/p/innovahybrid')
ref('Gabungan Industri Kendaraan Bermotor Indonesia','2026, January 19','Innova Zenix pimpin penjualan mobil hybrid nasional tahun 2025','https://www.gaikindo.or.id/innova-zenix-pimpin-penjualan-mobil-hybrid-nasional-tahun-2025/')
ref('International Business Solution Competition','2026','Semifinal round casebook: Auto2000 Digiroom',extra='[Competition casebook]')
ref('OtoXpert','n.d.','OtoXpert nearest workshop point of service','https://www.otoxpert.co.id/workshop')
ref('Toyota Astra Motor','n.d.','T-Care','https://aftersales.toyota.astra.co.id/t-care')
anchor=None
mark(source[70],'appendix_index')
names=[
 'Aftersales earns nearly half of case gross profit',
 'Digiroom already takes requests and the branch still has to confirm them',
 'Each source reveals a different part of the customer journey',
 'Paid work can stall at reception, scope or approval',
 'Households need to answer different questions on the drive',
 'Financing insurance trades upfront cash for higher instalments',
 'Existing outlets close 19 of 39 modeled oil-service gaps',
 'Bandung holds most of the gaps that remain',
 'A branch can matter for general repair even where oil alternatives exist',
 'Seven included visits can push paid scheduled work beyond 2028',
 'An appraisal can exist while the deposit or reservation remains unresolved',
 'The inspected offer becomes Rp71.5m of usable equity in this example',
 'Each customer decision has a different commercial endpoint',
 'Play Store ratings can look favorable without showing a completed task',
 'X accounts show why an owner might repair, buy or choose a specialist',
 'Three YouTube videos surface distinct BEV concerns',
 'Branch reviews identify specific points where jobs stall',
 'Zenix accounts for about four in five Toyota hybrids in the published breakdown',
 'Registered cars and mapped chargers answer different questions',
 'Sentiment and telemetry datasets have narrow roles in this case']
backs=['intro','claim1','analysis','claim2','claim3','claim4','claim5','claim5','claim5','claim6','claim7','claim7','claim8','claim1','claim3','claim3','claim2','intro','claim3','analysis']
index_titles=['Casebook metrics','Existing Digiroom journeys','Research coverage','Workshop cases','Household fit and test drives','Zenix credit comparison','Routing method and results','Four-market access atlas','Branch-level decisions','Entitlement timing','Appraisal and settlement cases','Worked upgrade terms','Issue tree crosswalk','Play Store and App Store reviews','X ownership accounts','YouTube BEV discussions','Google Maps review cohorts','Toyota model mix','Registered cars and charging sites','Auxiliary method checks']
for i in range(0,len(names),2):
 a=p()
 a.paragraph_format.space_after=Pt(3)
 for j in range(i,min(i+2,len(names))):
  if j>i:a.add_run('   |   ')
  hlink(a,f'A{j+1}  '+index_titles[j],'A'+str(j+1))
def appendix(n,new=False):
 title(f'A{n}  {names[n-1]}',f'A{n}',2,new)
 a=p();hlink(a,'Return to related analysis',backs[n-1]);a.add_run('   |   ');hlink(a,'Appendix index','appendix_index')
 a.paragraph_format.keep_with_next=True
def geo_rows(file):
 with (Path('repo/analysis/geography/tables')/file).open() as f:return list(csv.DictReader(f))

appendix(1,True)
p('The casebook supplies a common baseline for the market, Digiroom and the company economics. Each figure retains its original denominator.')
table(['Indicator','Value','Denominator or interpretation'],[
 ['xEV share, 2024 → 2025','11.9% → 21.8%','Indonesian new-car wholesales, including HEV, PHEV and BEV'],
 ['2025 xEV mix','103,931 BEV; 65,943 HEV; 5,270 PHEV','175,144 xEV wholesales'],
 ['Toyota hybrid share','51%','2025 hybrid sales in the casebook'],
 ['Vehicle sales and aftersales GP','Rp3,600bn; Rp3,150bn','Case Exhibit 3; all powertrains'],
 ['Aftersales share of revenue and GP','13.0%; 46.7%','Rp9,000bn revenue and Rp3,150bn GP across service, parts and body and paint'],
 ['Digiroom audience','500,000+ downloads; ~21,000 MAU','Cumulative downloads versus active users in a month'],
 ['Primary Digiroom activity','46% booking; 22% catalogue; 14% promotions; 10% tracking; 8% test drive or trade-in','Share of active users by main activity'],
 ['Service booking channels','16% Digiroom; 38% WhatsApp; 46% phone or walk-in','All service bookings in the case mix'],
 ],[4.4,5.1,7.5])
p('Source: IBSC (2026), pp. 3, 8, 10–11. xEV refers to HEV, PHEV and BEV.')

appendix(2,True)
table(['Existing customer entry','Evidence in the case or reviewed journey','What is still open for the customer'],[
 ['Vehicle catalogue and test drive','Digiroom supports model browsing and test-drive requests. Selected branch-model links preserved the requested vehicle and branch.','Is the demonstrator available, who confirms it, and what can the family check on the drive?'],
 ['Credit simulation','A hybrid and a BEV example displayed finance estimates before contact entry in the team’s desktop review.','Which terms does the buyer accept, and has the lender decided?'],
 ['Service booking and assisted channels','Both interviewees reporting routine service successfully used WhatsApp. The casebook lists booking and tracking in Digiroom.','Has the shop acknowledged the car and confirmed the work, finish time and payer decision?'],
 ['Trade-in and appraisal','The casebook identifies the existing trade-in route via OLXmobbi. Selected public reviews describe appraisal features.','Who makes a written buy offer and coordinates payoff, a specific replacement unit, and settlement?'],
 ],[3.65,6.35,7])
p('The casebook dates the Digiroom relaunch to December 2025 and describes Single ID as an existing CRM capability whose use by sales can be improved. Case records need to carry a decision across channels and make its owner visible. Source: IBSC (2026), pp. 2, 4, 7, 11; team review of public Digiroom journeys and anonymized interviews.')

appendix(3,True)
picture('corpus','Figure A3.1. Exported and deduplicated counts by platform. The scales describe records within each source.')
table(['Evidence family','Records reviewed or screened','What the evidence can establish'],[
 ['X posts','14,892 export rows; 14,291 unique platform IDs','Specific accounts of purchase, workshop or ownership decisions. Broad searches also captured replies, listings and news.'],
 ['Google Maps reviews','8,385 export rows; 8,119 unique IDs; 5,504 with text; 37 places','Named branch handoffs and counterexamples. Latest and low-rating selections overlap and serve different purposes.'],
 ['YouTube comments','74 unique comments across 3 videos','Specific perceptions and reported actions around BEV use, support and resale.'],
 ['Interviews','2 filled interviewer guides and 1 set of BYD Atto answer notes','Individual actions and household roles. The Atto notes are paraphrased.'],
 ['Workshop routing model','284 paired origins; 4 market windows; 29 corrected general-service endpoints','Relative modeled access for defined jobs and destinations.'],
 ],[3.65,5.27,8.08])
p('Platform records were deduplicated within platform. The team retained source-run membership and reviewed specific episodes in context. Reviews and posts are selected accounts rather than a representative sample of owners or completed jobs. Secondary evidence cutoff: 14 November 2026. Interviews were integrated on 16 November 2026.')

appendix(4,True)
table(['Case and context','Reported episode','Decision it informs'],[
 ['Setiabudi · Aug 2026','Veloz owner described arriving for paid service, waiting without reception and rejecting the branch.','Assign an adviser to acknowledge arrivals, including walk-ins.'],
 ['Pancing · 2026','Walk-in registration plate reportedly failed to enter the queue.','Carry the case into physical reception.'],
 ['Kertajaya · Feb 2026','Avanza owner described an assembly replacement estimate and a cheaper outside repair. Technical equivalence is unknown.','Explain diagnosis, scope and installed cost before authorization.'],
 ['Plaju · Oct 2026','Reviewer objected to communication and approval of work.','Record the exact scope the payer accepted.'],
 ['Soekarno-Hatta · Jul 2024 and Oct 2025','Two separate accounts described repeated visits or recorded complaints missed in service.','Carry the symptom through the work order and check resolution at handover.'],
 ['Cilandak · Mar 2026','Reviewer described prior consultation about additional work, clear charges and follow-up.','Use accepted scope and follow-up as a positive process comparison.'],
 ['Yaris Cross Hybrid interview','Driver booked and completed routine covered service. A family member controlled extra spend.','Keep driver, payer and programme entitlement distinct.'],
 ],[3.8,7.1,6.1])
p('Sources: selected Google Maps reviews of the named branches and anonymized team interview. Review dates are publication dates. Reports help locate breakdowns and counterexamples. They do not establish branch performance rates or verify invoices.')

appendix(5,True)
table(['Source','Routine or decision observed','What a confirmed drive needs to answer'],[
 ['Wuling Air EV interview','Apartment charging fit routine trips. The driver reported dealer booking via WhatsApp and used a separate tire shop.','Whether a particular household already has usable charging and room to wait.'],
 ['BYD Atto notes','The driver reported switching transport on one low-charge trip and searching for a charger on another. Parents handled acquisition.','Whether regular routes still work under pressure, and what backup the household can use.'],
 ['Yaris Cross Hybrid interview','The family chose a hybrid after a Raize and valued reported fuel efficiency. The father led the purchase.','How fuel use, carrying capacity and routine travel fit the buyer’s decision.'],
 ['Auto2000 prospect on X','Reported being unable to find a test-drive vehicle. The account does not identify a model or outlet.','Whether the branch can confirm the requested car, date and adviser.'],
 ['Setiabudi hybrid purchase reviews','Reported examples of an adviser coordinating household scheduling, financing, handover or paperwork.','Which parts of the decision a named adviser can already coordinate.'],
 ],[4.15,6.55,6.3])
p('The evidence supports designing around a household’s own questions. A 48-hour drive and a 3D fit check are design decisions. The accounts do not establish demand for a particular duration or estimate sales uplift.')

appendix(6)
p('Auto2000’s online credit calculator was observed on 11 November 2026 with New Innova Zenix 2.0 G HV CVT, Gray Metallic, Jakarta Pusat, a displayed price of Rp475,400,000, a 20% base down payment, and a 60-month term. Both calculations include instalment 1 upfront.')
table(['Displayed amount','Insurance paid upfront','Insurance financed','Financed minus upfront'],[
 ['Total cash due upfront','154,847,741','109,533,402','−45,314,339'],
 ['Monthly instalment','9,271,161','10,403,402','+1,132,241'],
 ['Remaining instalments','59','59','0'],
 ],[5,4,3.75,4.25],(1,2,3))
p('Values are in rupiah except the instalment count. The observation illustrates cash timing using the same model, price, base down payment, location and initial instalment convention. It is a dated calculator estimate. The source vehicle page is listed in References (Auto2000, n.d.).')

appendix(7,True)
p('For each retained origin, compare modeled driving time to the corrected general-service dealer network and the collected oil-job comparator. Repeat after including eligible Auto2000-operated OtoXpert destinations. A gap is the network time minus the comparator time. Count origins with a strict gap above five minutes using the same paired sample in both scenarios.')
mm={r['market']:r for r in geo_rows('raw_recomputed_markets.csv')}
rr=[]
for k in ('Bandung','Surabaya','Medan','Palembang'):
 r=mm[k];rr.append([k,r['paired_origins_n'],r['oil_tail_before_n'],r['oil_tail_after_n'],f"{float(r['median_oil_gap_min']):.2f} → {float(r['median_owned_gap_min']):.2f}"])
table(['Market','Paired origins','Dealer only >5 min','With OtoXpert >5 min','Median gap before → after, min'],rr+[['Total','284','39','20','—']],[3.1,2.2,3.45,3.6,4.65],(1,2,3,4))
p('Interpretation. 19 of 39 origin gaps clear the threshold in the expanded network. Bandung retains 14 of 20 and Surabaya retains six. The five-minute line is an analytical threshold. Grid points are not demand weights and modeled times do not represent live traffic, workshop capacity or booking outcomes.')
p('OtoXpert locations carry their operator designation. The official directory identifies both Auto2000-operated and separately operated outlets. Only locations eligible for the job and attributed to the relevant operator enter the expanded scenario (OtoXpert, n.d.).')

appendix(8,True)
p('Each panel uses the same retained origins within its market. The plots use origin coordinates in a schematic east–west and north–south frame, with axes scaled to each market window. They show where the gap persists. Street networks, captured routes and real-time traffic are outside the map.')
for i,(k,a,b,n) in enumerate([('Bandung',17,14,78),('Surabaya',10,6,59),('Medan',3,0,78),('Palembang',9,0,69)]):
 if i==2:
  title('A8  Four-market modeled access atlas continued',lvl=2,new=True)
  ret=p();hlink(ret,'Return to related analysis','claim5');ret.add_run('   |   ');hlink(ret,'Appendix index','appendix_index')
 picture('atlas_'+k,f'Figure A8.{i+1}. {k}. {a} to {b} origins above five minutes, from {n} paired origins.')
p('Source for all four panels: team’s corrected workshop routing model, using paired origin centres and scenario-specific gaps. The geographic frame preserves relative positions within each market.')

appendix(9,True)
table(['Branch or market','Oil-service finding','Implication for general repair and fulfilment'],[
 ['Bandung Soekarno-Hatta','8 remaining oil-gap origins are assigned there.','Prepare eligible work and address the reported risk of missed items or repeat visits.'],
 ['Bandung Suci','3 remaining oil-gap origins are assigned there after the endpoint correction.','Use the corrected destination in comparisons. Keep job eligibility separate from travel time.'],
 ['Bandung Cibiru, Pasteur and Setiabudi','1 remaining oil-gap origin each.','Address outlet and job-specific pockets.'],
 ['Surabaya','6 remaining oil-gap origins in the corrected comparison.','Use job-specific alternatives and keep the remaining pockets visible.'],
 ['Medan Pancing','0 remaining oil-gap origins; 8 origins lose 15-minute general-workshop access when it is removed in the model.','Preserve its general-workshop role.'],
 ['Palembang Tanjung Api-Api','0 remaining oil-gap origins; 7 lose 15-minute general-workshop access in the removal comparison.','Keep general service accessible even where eligible oil routes have alternatives.'],
 ],[4.05,5.8,7.15])
p('Oil-service substitution and general-workshop protection use separate destination sets. The branch-removal exercise compares modeled access and does not recommend closing or expanding any site.')

branch_data=geo_rows('branch_portfolio.csv')
assert len(branch_data)==29
title('A9.1  Corrected workshop destinations',lvl=2,new=True)
a=p();hlink(a,'Return to related analysis','claim5');a.add_run('   |   ');hlink(a,'Appendix index','appendix_index')
p('Assigned origins use the modeled nearest general-service dealer. The final column counts origins that lose a dealer within 15 model minutes when the assigned branch is removed. A zero indicates a result under that comparison.')
for i,batch in enumerate([branch_data[:15],branch_data[15:]]):
 if i:
  title('A9.1  Corrected workshop destinations continued',lvl=2,new=True)
  a=p();hlink(a,'Return to related analysis','claim5');a.add_run('   |   ');hlink(a,'Appendix index','appendix_index')
 table(['Market and outlet','Assigned origins','Oil tails before','Oil tails after','Lose access'],[
   [r['market']+' · '+r['branch_name'].split(' - ')[0].replace('AUTO2000','Auto2000'),r['assigned_grid_origins_n'],r['oil_gap_gt5_before_owned_network_n'],r['oil_gap_gt5_after_owned_network_n'],r['origins_losing_15min_general_branch_access_if_removed_n']] for r in batch
 ],[7.4,2.5,2.4,2.3,2.4],(1,2,3,4))
p('Source: corrected four-market workshop-routing study. Timing is scenario-based. The oil columns use the >5-minute screen.')
appendix(10,True)
table(['Item','Timing or coverage','Paid-service implication'],[
 ['Eligible Toyota T-Care','Up to seven services within three years or 60,000 km, whichever comes first.','Check programme, vehicle and job coverage.'],
 ['Illustrative time-only calendar','Jan 2026 delivery; Feb 2026 visit 1; Jul 2026 visit 2; every six months thereafter.','Visit 7 falls Jan 2029 and visit 8 falls Jul 2029.'],
 ['High-mileage owner','Mileage trigger can precede the calendar.','Use the vehicle’s actual odometer and due work.'],
 ['Mixed job or policy exception','A visit can include covered scheduled work and an uncovered addition.','Assign eligibility, payer and any reimbursement by work item.'],
 ],[4.2,6.0,6.8])
p('Source for programme terms: Toyota Astra Motor (n.d.). The dates are an illustrative entitlement calculation. A vehicle’s actual schedule and eligibility determine what it pays.')
title('Paid work by powertrain and payer',lvl=2)
table(['Cohort','Relevant opportunity','How to count it'],[
 ['HEV or PHEV with covered scheduled work','Programme labor and parts eligible under vehicle terms.','Record any reimbursement separately from customer-paid extras.'],
 ['HEV or PHEV with uncovered work','Due or uncovered tasks confirmed for the vehicle and programme.','Count paid work once at completion.'],
 ['BEV owners','Vehicle-specific inspection, diagnostics or eligible wear work.','Use actual job eligibility, payer and outlet capability.'],
 ['Petrol Toyota owners','Customer-paid oil or general repair where the job fits the outlet.','Identify the owner’s prior comparable workshop for the win-back count.'],
 ],[4.0,6.8,6.2])

appendix(11,True)
table(['Evidence','What happened or was reported','What the evidence supports'],[
 ['Yaris Cross Hybrid interview','Driver consulted marketplace and dealer prices and reached a range. The account contains no closed appraisal or trade.','Distinguish market indication, inspection and an offer a buyer has issued.'],
 ['Kertajaya reviews · Oct 2026','Two reviews describe TRIVA estimates or appraisal inputs, including an OLX comparison.','Appraisal interfaces are already familiar to some customers.'],
 ['Gatot Subroto trade-in account','Reviewer reported stalled approval and difficulty recovering a deposit.','Put the expiry, commitments and refund route in the terms.'],
 ['OLXmobbi Tamini account','Reviewer reported the booked unit went to another buyer despite payment and reported credit approval.','Confirm the specific replacement unit and reconcile the hold with the offer and credit timeline.'],
 ['BYD Atto answer notes','The respondent expressed interest in knowing a minimum future value and reported no resale action.','A stated preference for certainty is distinct from taking an actual offer.'],
 ],[4.1,6.4,6.5])
p('Sources: anonymized team interviews and selected public Google Maps accounts. The deposit and allocation reports identify plausible handoff failures. Neither report identifies an xEV.')

appendix(12)
table(['Item','Sample terms or state','Who confirms it'],[
 ['Inspected buy offer','Rp248.0m','Used-car purchaser or appraiser, subject to written offer terms'],
 ['Existing loan payoff','Rp174.0m','Existing lender'],
 ['Trade-in fees','Rp2.5m','Appraiser or adviser with a fee breakdown'],
 ['Usable equity','Rp71.5m = Rp248.0m − Rp174.0m − Rp2.5m','Upgrade adviser reconciles the agreed inputs'],
 ['Replacement, credit and settlement','Exact unit reserved; dated terms accepted; old lender paid and both handovers reconciled','Sales, lender and upgrade adviser each confirm the state they control'],
 ],[4.15,6.5,6.35])
p('Source: sample transaction in the Digiroom KEY demonstration. Figures illustrate the arithmetic. The sample does not establish market value, lender approval or a completed sale.')

appendix(13,True)
table(['Customer decision','Evidence carried from Chapter 2','Commercial outcome'],[
 ['Can this xEV fit the household and its budget?','Different household driving and charging routines; reported demonstrator availability; dated cash timing contrast.','A new-to-Auto2000 customer takes xEV delivery.'],
 ['Can this outlet complete the agreed job?','Job-specific access comparison; reported reception, scope and payer handoffs; scheduled-service entitlement timing.','Auto2000 completes eligible customer-paid work, with outside-workshop recovery identified separately.'],
 ['Can I fund and close the upgrade?','Resale range, payoff and fees; reported deposit and allocation dependencies.','An existing Auto2000 customer takes delivery of the next xEV.'],
 ],[4.75,6.65,5.6])
p('Digiroom’s common role is to preserve the case, show who can act next, and give the customer a reason to return when the decision moves. Each outcome can be counted once across digital and assisted channels.')
exec((W/'extra.py').read_text())
# Refresh the display cache of the original Word TOC field while keeping its styles.
toc_rows=list(toc.iter(qn('w:p')))
old_toc=[deepcopy(toc_rows[i]) for i in range(len(toc_rows))]
for i,pn in enumerate(toc_rows):
 if i in (6,7,8,9,10,13):pn.getparent().remove(pn)
def toc_item(row,text,key,page):
 link=row.find(qn('w:hyperlink'));link.set(qn('w:anchor'),key)
 tt=list(link.iter(qn('w:t')))
 tt[0].text=text
 tt[-1].text=str(page)
 return row
positions=[2,2,3,3,4,4,5,5]
for i,h in enumerate(head,1):
 toc_rows[11].addprevious(toc_item(deepcopy(old_toc[6]),f'{i}. {h}',f'claim{i}',positions[i-1]))
for i,label,key,page in [(2,'CHAPTER I: INTRODUCTION','intro',1),(5,'CHAPTER II: ANALYSIS','analysis',2),(15,'REFERENCES','references',6),(16,'APPENDICES','appendix_index',6)]:
 toc_item(toc_rows[i],label,key,page)
for i,num in [(1,1),(3,1),(4,2),(11,6),(12,6),(14,6)]:
 link=toc_rows[i].find(qn('w:hyperlink'))
 list(link.iter(qn('w:t')))[-1].text=str(num)

for row in toc.iter(qn('w:p')):
 pr=row.find(qn('w:pPr'))
 if pr is not None:
  for tab in pr.iter(qn('w:tab')):
   if tab.get(qn('w:val'))=='right':tab.set(qn('w:pos'),str(Cm(16.9).twips))
d.save(W/'output'/'Digiroom_KEY_Chapters_1_and_2.docx')
