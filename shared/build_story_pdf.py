"""Finding-led visual reading edition. Full research remains in source reports.
Fixed pages have measured text bounds; every finding keeps its source and limit.
"""
from pathlib import Path
import json,html,re,hashlib,datetime,shutil
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
PDF=OUT/'Auto2000_Research_Findings.pdf';FIG=ROOT/'figures/story'
FONT=Path('/usr/share/fonts/truetype/open-sans')
for name,file in [('Body','OpenSans-Regular.ttf'),('Bold','OpenSans-Bold.ttf'),('Italic','OpenSans-Italic.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
W,H=A4;M=45;CW=W-2*M
BLUE=colors.HexColor('#245A78');ORANGE=colors.HexColor('#B97032');INK=colors.HexColor('#183A50');MUTED=colors.HexColor('#576D7B');LIGHT=colors.HexColor('#EEF4F7');PALE=colors.HexColor('#FBF1E7');GRAY=colors.HexColor('#A6B4BE')
ST={
 'title':ParagraphStyle('title',fontName='Bold',fontSize=23,leading=28,textColor=INK),
 'body':ParagraphStyle('body',fontName='Body',fontSize=11.7,leading=16.8,textColor=colors.HexColor('#253642')),
 'small':ParagraphStyle('small',fontName='Body',fontSize=9.4,leading=12.8,textColor=MUTED),
 'label':ParagraphStyle('label',fontName='Bold',fontSize=11,leading=15,textColor=INK),
 'card':ParagraphStyle('card',fontName='Body',fontSize=10.6,leading=14.4,textColor=colors.HexColor('#253642')),
 'metric':ParagraphStyle('metric',fontName='Bold',fontSize=29,leading=34,textColor=BLUE),
 'cover':ParagraphStyle('cover',fontName='Bold',fontSize=31,leading=38,textColor=INK)}
pages=[];bounds=[];source_assets=[]
def clean(s):
 s=str(s).replace('\u2014',', ').replace('\u2013','-').replace('\u2011','-').replace('\u2212','-').replace('\u2192',' to ').replace('\u2194',' versus ').replace('\u00a0',' ')
 s=re.sub(r'\b(of|for|including|from|than|within|above|below|over|under|returned|HTTP|PDF)(?=\d)',r'\1 ',s)
 s=re.sub(r'\ball(?=\d)','all ',s)
 s=re.sub(r'(?<=\d)(of|versus|through|to)(?=\d)',r' \1 ',s)
 s=re.sub(r'(\d)(?=customer|fleet|matrix|source|first-wave|additional|independent|aligned|distinct|duplicate|public|scoped|analytical|finer|assertions|pass|qualified|records|years|months|million|billion|rows|parts)',r'\1 ',s)
 s=re.sub(r'(\d)(?=November|December|January|October|Nov\b|Dec\b|Jan\b|Oct\b|Indonesia|Google|Digiroom|km\b)',r'\1 ',s)
 s=re.sub(r'\b(November|December|January|October|Nov|Dec|Jan|Oct)(?=20\d{2})',r'\1 ',s)
 s=re.sub(r'\bDP(?=\d)','DP ',s)
 s=re.sub(r'\b(organizes|The|the|not|Across|across|and|both|as|observed|Deloitte|Rakuten)(?=\d)',r'\1 ',s)
 s=re.sub(r'(\d)(?=concepts|grouped|prices|cross-source|targeted|units)',r'\1 ',s)
 s=re.sub(r'(?<=[A-Za-z]),(?=\d)',', ',s)
 s=re.sub(r'(?<=:)(?=\d)',' ',s)
 s=re.sub(r'(?<=\d)and(?=T\d)',' and ',s)
 s=re.sub(r'\bcodes(?=T\d)','codes ',s)
 s=re.sub(r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?=20\d{2})',r'\1 ',s)
 s=s.replace('PwC\'s71%','PwC\'s 71%').replace('PwC’s71%','PwC’s 71%').replace('%versus','% versus ').replace('The61/62%','The 61/62%')
 s=s.replace('checks.18','checks. 18').replace('URLs;21','URLs; 21').replace('records,May','records, May')
 s=s.replace('on255,414','on 255,414').replace('with617,703','with 617,703').replace('71%maintenance','71% maintenance').replace('28%awareness','28% awareness')
 return s
def markup(s):return re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',html.escape(clean(s))).replace('\n','<br/>')
def asset(name):
 fs=list(ROOT.rglob(name));assert len(fs)==1,(name,fs);source_assets.append(str(fs[0].relative_to(ROOT)));return json.loads(fs[0].read_text())
EC=asset('economic_story.json')['pages'];DS=asset('data_story.json')['pages'];RV=asset('review_story.json')['pages'];JY=asset('journey_story.json')['pages'];MC=asset('mechanism_story.json')['pages'];SOL=asset('solution_cards.json')
def para(c,text,x,y,width,style='body',min_y=118):
 p=Paragraph(markup(text),ST[style]);_,h=p.wrap(width,1000)
 assert y-h>=min_y,f'Page {c.getPageNumber()}: text below reserved region ({y-h:.1f}) {str(text)[:80]}'
 p.drawOn(c,x,y-h);bounds.append({'page':c.getPageNumber(),'kind':'text','top':y,'bottom':y-h,'x':x,'width':width});return y-h
def add(headline,body,visual,takeaway,limit,source,kind='OBSERVED / DERIVED',chapter=''):
 pages.append({'headline':headline,'body':body,'visual':visual,'takeaway':takeaway,'limit':limit,'source':source,'kind':kind,'chapter':chapter})
def from_econ(i,headline,takeaway):
 p=EC[i];vis={'type':'image','name':f'economic_{i+1:02d}.png'} if i!=2 else {'type':'entitlements','data':p['plot_data']}
 add(headline,p['body'],vis,takeaway,' '.join(p['limits'][:2]),p['source_note'],kind='ILLUSTRATION ONLY' if i>=4 else 'SUPPLIED CASE EXHIBIT' if i==0 else 'PUBLISHED / DERIVED')
def from_data(i,headline=None):
 p=DS[i];vis={'type':'unit_cards','data':p['chart']['cards']} if i==3 else {'type':'image','name':f'data_{i+1:02d}.png'}
 attribution='Allam et al.(2023), Mendeley V2, doi:10.17632/7vdkzpnjgj.2, CC BY-NC3.0.' if i>=4 else p['attribution']
 add(headline or p['title'],p['body'],vis,p['takeaway'],p['evidence_limit'],p['chart_note']+' Source: '+attribution,kind='AUXILIARY MEASUREMENT TEST' if i>=4 else 'DERIVED SENSITIVITY')
def from_review(i,visual):
 p=RV[i];add(p['headline'],p['body'],visual,p['implication'],p['limits'][0]+' '+p['limits'][-1],p['one_line_chart_note']+' Evidence: extension_reviews and frozen reviews tables.',kind='SELECTED PUBLIC RECORDS')

# The story is a reading layer, not a replacement for the full research archive.
pages.append({'type':'cover','headline':'The real question is which customer job Digiroom can help finish.'})
from_econ(0,'Aftersales matters more than its revenue share suggests.','A useful ownership job can matter commercially even when it produces few app sessions.')
from_econ(1,'Most of the xEV decline matches a smaller total portfolio.','Separate broad sales scale, vehicle mix and dealer conversion before blaming an app.')
add(MC[0]['headline'],MC[0]['paragraph']+' Low monthly activity alone does not tell us whether a job was due, completed elsewhere or lost.',{'type':'accounting'},'Follow completed jobs across channels, then compare with a credible counterfactual.',MC[0]['uncertainty_line'],'Evidence: MECH-01; extension_hypotheses/MECE_HYPOTHESIS_COVERAGE.csv and accounting review.',kind='MECE ACCOUNTING FRAMEWORK')
add(JY[0]['headline'],JY[0]['body'],{'type':'capabilities','data':JY[0]['visual']['rows']},'The new idea needs a specific improvement beyond the existing route.',JY[0]['boundary'],JY[0]['source_caption'])
add(JY[1]['headline'],JY[1]['body'],{'type':'image','name':'finance_timing.png'},'Explain cash at delivery and later obligations without inventing an approved rate.',JY[1]['boundary'],'UX03-UX04. Innova Zenix G HV CVT; Jakarta Pusat; Rp475.4m; DP20%; ADDM; 60-month illustration,59 remaining payments.')
add(JY[2]['headline'],JY[2]['body'],{'type':'observed_labels'},'Investigate this exact information issue; do not generalize it into a site-wide failure.',JY[2]['boundary'],'XT05/XTS02; auto2000.co.id/mobil-baru-toyota/p/bz4x/spesifikasi;11 November2026.')
add(MC[1]['headline'],MC[1]['paragraph'],{'type':'study_cards','data':MC[1]['visual']['cards']},'Better understanding is plausible. A delivery uplift still needs evidence.',MC[1]['uncertainty_line'],'Petrov et al.(2025),doi:10.1016/j.trd.2025.104921; Bernardic et al.(2024); NIST DCI008. Exact locators in extension_hypotheses.')
from_review(0,{'type':'review_tiles'})
from_review(1,{'type':'image','name':'review_language.png'})
from_review(2,{'type':'image','name':'review_dates.png'})
add('Service confidence extends beyond a booking slot.','In Deloitte\'s Indonesia service-provider choice question, quality, trust and warranty coverage lead the published reasons. Convenience still matters, but this question does not put it first. These are stated reasons in a national study, not measurements of Auto2000 customers or evidence that one proposed feature changes a sale.',{'type':'image','name':'service_choice.png'},'A scheduling idea should explain how it helps the underlying service decision.','Different survey questions have different bases. A rounded zero in another question does not mean customers never want online booking.','Deloitte2026 SEA Automotive Consumer Study,p33,Q17,Indonesia n=618. Published rounded shares; fieldworkOct-Nov2025.',kind='PUBLISHED SURVEY')
add(JY[3]['headline'],JY[3]['body'],{'type':'request_states'},'A tentative window and a confirmed unit are different promises.',JY[3]['boundary'],JY[3]['source_caption'])
add('Branch and vehicle context survived two tested links.','Two actual branch links carried their selections into the test-drive route. Juanda opened with bZ4X; Cempaka Putih opened with Hiace and changed the preceding branch selection. These are useful counterexamples to a blanket claim that handoffs always lose context. They do not establish technician competence, current unit stock, a confirmed slot or successful fulfilment.',{'type':'handoffs'},'Keep the functioning baseline and look for the narrower unresolved handoff.','Two logged-out desktop routes; no request or personal data submitted. Mobile and native-app behavior remain untested.','XT08, XTS10/XTS12. Branch codesT151andT155. Detailed URLs and observations in extension_journeys.')
from_econ(2,'Longer coverage does not always mean more covered visits.','Keep programme eligibility, covered work and event count separate from headline years.')
from_econ(3,'Later service bills vary within one model.','A dated retail estimate can inform a conversation; it cannot reveal dealer gross profit.')
from_data(0,'Nearby on a map does not establish usable access.')
from_data(1,'One published location differs by 55 kilometres.')
from_data(2,'Boundary matching changes the provincial ranking.')
from_data(3)
add('Toyota retention and Auto2000 capture can differ.','Toyota already offers fleet telematics and an economical parts/repair ecosystem. These are baselines for new reminder or older-vehicle ideas. A customer who stays with Toyota through another authorised or economical channel may support the ecosystem without producing the same Auto2000 branch ticket. The customer, decision owner, payer and business perimeter need to stay visible.',{'type':'perimeters'},'Define whose outcome improves before calculating an incremental benefit.','Public programme descriptions do not establish local adoption, referral fees or dealer profit. Europe-only warranty terms must not be transferred to Indonesia.','Extension stakeholder audit: G-Fleet, T-OPT/OtoXpert, partner roles and geographic warranty checks.18targeted URLs;21 scoped observations.')
add(MC[2]['headline'],MC[2]['paragraph'],{'type':'certificate'},'A retrieval route is a baseline. Accepted evidence and a changed transaction are later links.',MC[2]['uncertainty_line'],'JX02; NIST TN2328 and DCI008; extension_hypotheses and extension_battery. No certificate downloaded or appraisal observed.',kind='OBSERVED BASELINE / UNTESTED MECHANISM')
from_data(4,'The large telemetry subset still lacks a public health reference.')
from_data(5,'Bridging recording gaps inflated one result by 47.5%.')
from_data(6,'Four partial-charge slopes are not four health scores.')
from_econ(4,'A capped top-up does not create a full price floor.','State the customer promise and retained exposure before discussing who might fund it.')
from_econ(5,'The same offers can produce a larger peak loss.','A limit on insurer payment does not cap a separate full-floor promise.')
add('MECE reveals lifecycle gaps as well as more features.','The lifecycle audit organizes25customer or fleet outcomes plus one institutional funding layer across ten grouped decision-owner roles. It also highlights recall completion, delivery closure, reasoned redress and terminal ownership or account exit. These are coverage questions, not proof that Auto2000 lacks the relevant functions. Safety-campaign completion should not be treated as discretionary paid upsell.',{'type':'lifecycle'},'Use the matrix to find an unobserved job and its decision owner, then test the gap.','The260matrix cells are not260independent needs. Recall is one separate research candidate; no solution is selected.','Extension stakeholder audit:26analytical job units,10grouped roles,18finer stakeholder lenses. EXT-OPT01 builds on existing VIN lookup and booking.',kind='MECE COVERAGE AUDIT')

for family in SOL['family_order']:
 cards=[s for s in SOL['cards'] if s['family']==family]
 chunks=[cards[:3],cards[3:]] if len(cards)>4 else [cards]
 for part,chunk in enumerate(chunks):
  pages.append({'type':'options','headline':family.split('. ',1)[1]+(' (continued)' if part else ''),'family':family,'cards':chunk})
from_review(3,{'type':'evidence_footprint'})
add('Two automated label views disagreed on 41.35% of rows.','The largest review appendix covers Indonesian public-service apps, not Digiroom. Its rating-derived and VADER labels disagree on255,414of617,722aligned rows. Neither is human ground truth. The two label files describe the same base records, with617,703distinct composite keys and19duplicate excess rows per view. They are useful for testing shortcuts, not for expanding the Auto2000 customer sample.',{'type':'igar'},'Keep a star rating, sentiment label, specific task and completed outcome as different fields.','Historical auxiliary records,May2012-Mar2023. Agreement is not accuracy; duplicate label views are not extra people.','IGAR V2,doi:10.17632/7zryc6k76z.2,CC BY4.0. Paired raw files and row-level nontext comparison are included in the primary ZIP.',kind='AUXILIARY METHOD TEST')
add('Some supplied numbers need narrower denominators.','Several friend-source claims become more useful after checking who answered each question. The older Deloitte charging result uses a small EV-intender subgroup, not all1,004Indonesia respondents. PwC\'s71%maintenance answer is conditional on owners considering a return to ICE. The supplied Rakuten57%versus28%awareness values could not be independently verified from the underlying chart.',{'type':'survey_scope'},'Keep the population, year, vehicle definition and question beside every percentage.','Unverified values remain supplied claims. Conflicting secondary Populix geography and undisclosed subgroup bases remain unresolved.','Friend survey audit:43claims; Deloitte2025 SEA Q42/Q43; PwC2024/2025 methods; Rakuten chart metadata versus hidden numeric values.',kind='SOURCE-SCOPE AUDIT')
add('The strongest open questions are operational and commercial.','The research found existing functions, specific presentation issues and several plausible opportunities. It did not measure actual branch capacity, fulfilled jobs, current owner entitlement, realized margins or incremental response. A clearer request, record or certificate may help. Which change produces additional value is still a hypothesis.',{'type':'known_unknown'},'Use the solution menu to choose a question worth resolving, rather than treating page counts as proof of impact.','No human interviews, branch visits, private account records, submitted bookings or causal Auto2000 experiment were conducted.','First-wave numerical QA:157assertions,140pass/17qualified/0fail. Extension:69assertions,66pass/3qualified/0fail. AI checks; no human validation.',kind='EVIDENCE BOUNDARY')
pages.append({'type':'file_guide','headline':'Use this story to navigate the full research.'})

def basic(c,n,total,kicker):
 c.setFillColor(MUTED);c.setFont('Body',8.5);c.drawString(M,H-25,'AUTO2000 DIGIROOM  |  RESEARCH FINDINGS')
 c.setStrokeColor(colors.HexColor('#D7E1E7'));c.line(M,40,W-M,40);c.setFont('Body',8.5);c.drawString(M,25,'11 November 2026 | Public-source research');c.drawRightString(W-M,25,f'{n} / {total}')
 if kicker:
  if not kicker.startswith('(guessing)'):
   kicker=('(certain, conditional) ' if 'ILLUSTRATION' in kicker or 'FRAMEWORK' in kicker else '(certain) ')+kicker
  c.setFillColor(ORANGE if 'ILLUSTRATION' in kicker else BLUE);c.setFont('Bold',8.8);c.drawString(M,H-55,clean(kicker))
def card(c,x,y,w,h,title,body,value=None,fill=LIGHT):
 c.setFillColor(fill);c.roundRect(x,y-h,w,h,8,stroke=0,fill=1);yy=y-12
 if value:yy=para(c,value,x+12,yy,w-24,'metric',min_y=y-h+7)-6
 yy=para(c,title,x+12,yy,w-24,'label',min_y=y-h+7)-5
 if body:para(c,body,x+12,yy,w-24,'card',min_y=y-h+7)
def image(c,name,x,y,w,h):
 p=FIG/name;im=Image.open(p);iw,ih=im.size;s=min(w/iw,h/ih);ww,hh=iw*s,ih*s;c.drawImage(str(p),x+(w-ww)/2,y-hh,width=ww,height=hh,mask='auto');return y-hh
def visual(c,v,y):
 t=v['type'];x=M;w=CW;h=270
 if t=='image':return image(c,v['name'],x,y,w,h)
 if t=='unit_cards':
  for j,d in enumerate(v['data']):card(c,x+(j%2)*(w/2+5),y-(j//2)*118,w/2-5,108,d['label'],d['meaning'],d['display'])
  return y-236
 if t=='review_tiles':
  colorset=[BLUE]*7+[GRAY]*5+[ORANGE]*4;tw=(w-15*5)/16
  for j,col in enumerate(colorset):c.setFillColor(col);c.roundRect(x+j*(tw+5),y-38,tw,30,3,stroke=0,fill=1)
  for j,(val,title,body) in enumerate([('7','Specific app interaction','May include a failed attempt'),('5','Not enough detail','Task or outcome remains unclear'),('4','Other / not used yet','Car, branch or prospective view')]):card(c,x+j*(w/3+4),y-62,w/3-8,137,title,body,val,fill=LIGHT if j<2 else PALE)
  return y-207
 if t=='accounting':
  rows=[('Jobs due','Eligible vehicle cohort and work'),('Completed here','Across all Auto2000 channels'),('Gross profit per job','Revenue less recognized direct cost')]
  for j,(a,b) in enumerate(rows):card(c,x+j*(w/3+3),y,w/3-6,116,a,b,str(j+1))
  para(c,'Compare the with-change result with the counterfactual. Keep operating costs below GP separate; count each item once.',x,y-140,w,'label',min_y=120)
  return y-205
 if t=='capabilities':
  yy=y
  for d in v['data']:
   para(c,d['task'],x+8,yy-6,w*.43,'label');para(c,d['observed_endpoint'],x+w*.46,yy-6,w*.52,'body');c.setStrokeColor(colors.HexColor('#D7E1E7'));c.line(x,yy-41,x+w,yy-41);yy-=48
  return yy-4
 if t=='observed_labels':
  card(c,x,y,w,100,'Observed translated label','Displayed value unchanged','Fuel system: BEV')
  card(c,x,y-116,w,110,'Tank capacity (litres)','Literal page value; engineering meaning unverified','7311',fill=PALE)
  para(c,'Research redraw of two observed fields, not a product screenshot.',x,y-242,w,'small');return y-260
 if t=='study_cards':
  for j,d in enumerate(v['data']):card(c,x+(j%2)*(w/2+5),y-(j//2)*125,w/2-5,115,d['source'],d['endpoint']+'. '+d['result'])
  return y-258
 if t=='request_states':
  rows=[('Preview branch, date and time','Observed on desktop',BLUE),('Submit request','Not performed',GRAY),('Staff confirms unit and schedule','Stated in FAQ; not observed',GRAY),('Attend and complete the job','Not observed',GRAY)]
  for j,(a,b,col) in enumerate(rows):
   yy=y-j*57;c.setFillColor(col);c.circle(x+9,yy-15,7,stroke=0,fill=1)
   if j<3:c.setStrokeColor(GRAY);c.line(x+9,yy-24,x+9,yy-50)
   para(c,a,x+30,yy-2,w-35,'label');para(c,b,x+30,yy-21,w-35,'small')
  return y-239
 if t=='handoffs':
  for j,(a,b) in enumerate([('Juanda / bZ4X','Juanda / bZ4X'),('Cempaka Putih / Hiace','Cempaka Putih / Hiace')]):
   yy=y-j*111;card(c,x,yy,w*.46,85,'Actual branch link',a);card(c,x+w*.54,yy,w*.46,85,'Loaded selection',b)
   c.setStrokeColor(BLUE);c.line(x+w*.47,yy-40,x+w*.53,yy-40);c.line(x+w*.53-5,yy-36,x+w*.53,yy-40);c.line(x+w*.53-5,yy-44,x+w*.53,yy-40)
  return y-230
 if t=='entitlements':
  for j,d in enumerate(v['data']):
   yy=y-j*83;para(c,d['program'],x,yy,w*.25,'label');para(c,f"{d['maximum_years']}years / {d['maximum_km']:,}km maximum",x,yy-23,w*.25,'small')
   for k in range(7):
    if k>=d['covered_scheduled_event_count']:continue
    xx=x+148+k*42;c.setFillColor(BLUE if k<d['covered_scheduled_event_count'] else LIGHT);c.circle(xx,yy-17,13,stroke=0,fill=1);c.setFillColor(colors.white if k<d['covered_scheduled_event_count'] else MUTED);c.setFont('Bold',10);c.drawCentredString(xx,yy-20,str(k+1))
   para(c,'Labor + specified parts' if d['covered_specified_parts'] else 'Labor only; base programme',x+136,yy-41,w-140,'small')
  return y-255
 if t=='perimeters':
  card(c,x,y,w,80,'Customer outcome','A suitable, affordable job is completed for the person or fleet.')
  card(c,x,y-96,w/2-6,125,'Toyota ecosystem','May retain the owner through different brands, partners and economical repair channels.')
  card(c,x+w/2+6,y-96,w/2-6,125,'Auto2000 business','Needs attributable completed work and contribution at its own stated perimeter.')
  return y-229
 if t=='certificate':
  labels=[('Measure','Technically valid result'),('Understand','Scope, age and limits'),('Trust','Credible issuer'),('Accept','Appraiser uses it'),('Change outcome','A transaction changes')]
  for j,(a,b) in enumerate(labels):
   yy=y-j*47;c.setFillColor(LIGHT);c.roundRect(x,yy-39,w,39,5,stroke=0,fill=1);para(c,a,x+11,yy-9,110,'label');para(c,b,x+135,yy-9,w-145,'body')
  return y-247
 if t=='lifecycle':
  labs=[('Choose and acquire','Delivery closure is a separate job'),('Maintain and repair','Model, programme and payer matter'),('Protect and resolve','Recall completion and reasoned redress'),('Replace or exit','Appraisal, custody and account exit')]
  for j,(a,b) in enumerate(labs):card(c,x+(j%2)*(w/2+5),y-(j//2)*121,w/2-5,110,a,b)
  return y-249
 if t=='evidence_footprint':
  card(c,x,y,w/2-6,140,'Unique app-review IDs','210first-wave +148additional; selected records, not verified people.','358')
  card(c,x+w/2+6,y,w/2-6,140,'Narrative annotations','Across38source URLs; not95independent customers.','95')
  para(c,'Keep these evidence types separate. There is no meaningful grand total.',x,y-163,w,'label');return y-214
 if t=='igar':
  agree=617722-255414;total=617722;c.setFillColor(BLUE);c.roundRect(x,y-64,w*agree/total,48,0,stroke=0,fill=1);c.setFillColor(ORANGE);c.rect(x+w*agree/total,y-64,w*255414/total,48,stroke=0,fill=1)
  card(c,x,y-94,w/2-6,110,'Same label','362,308aligned rows','58.65%');card(c,x+w/2+6,y-94,w/2-6,110,'Different labels','255,414aligned rows','41.35%',fill=PALE);return y-223
 if t=='survey_scope':
  for j,(title,body) in enumerate([('Deloitte 2025 charging preference','The 62% home-charging result uses Q43\'s 178 BEV/PHEV intenders, not all 1,004 Indonesia respondents.'),('PwC maintenance concern','71% refers to owners considering a return to ICE, not all owners in the study.'),('Rakuten brand awareness','The supplied 57% versus 28% chart values remain unverified; metadata does not verify the numbers.')]):card(c,x,y-j*87,w,76,title,body,fill=LIGHT if j<2 else PALE)
  return y-269
 if t=='known_unknown':
  card(c,x,y,w/2-6,215,'What is supported','Existing public functions\n\nSpecific rendered states\n\nReproduced calculations\n\nSource and scope corrections')
  card(c,x+w/2+6,y,w/2-6,215,'What remains open','Eligible demand and capacity\n\nFulfilled work and margins\n\nAppraisal acceptance\n\nIncremental customer response',fill=PALE);return y-225
 raise ValueError(t)
def regular(c,p):
 y=H-76;y=para(c,p['headline'],M,y,CW,'title')-16;y=para(c,p['body'],M,y,CW)-17;y=visual(c,p['visual'],y)-16
 # The implication is close to the evidence rather than hidden in a later essay.
 q=Paragraph(markup(p['takeaway']),ST['body']);_,hh=q.wrap(CW-24,500);bh=hh+24
 assert y-bh>=145,(c.getPageNumber(),p['headline'],'takeaway overflow',y-bh)
 c.setFillColor(PALE if 'ILLUSTRATION' in p['kind'] else LIGHT);c.roundRect(M,y-bh,CW,bh,6,stroke=0,fill=1);para(c,p['takeaway'],M+12,y-12,CW-24,min_y=145);y-=bh+12
 para(c,'Limit: '+p['limit'],M,y,CW,'small',min_y=112)
 para(c,p['source'],M,91,CW,'small',min_y=46)
def cover(c,total):
 para(c,'The real question is which customer job Digiroom can help finish.',M,H-85,CW,'cover')
 para(c,'A visual research story for the Auto2000 case',M,H-235,CW,'body')
 para(c,'Existing tools already do useful work. The open opportunity is more specific: a decision, record or handoff that the customer cannot yet use with confidence.',M,H-280,CW)
 for j,(a,b) in enumerate([('Start with value','Completed jobs and contribution'),('Test the evidence','States, samples and source limits'),('Keep choices open','27concepts; no selected winner')]):card(c,M,H-390-j*102,CW,88,a,b)
 para(c,'(certain) marks captured states or reproduced calculations. (guessing) marks an untested mechanism. Charts preserve those distinctions. Full technical work and raw data remain in the ZIP.',M,122,CW,'small',min_y=46)
def options(c,p):
 y=H-76;y=para(c,p['headline'],M,y,CW,'title')-12;y=para(c,'Possible directions for your choice. Existing baseline, possible addition and a reason it might fail are kept together.',M,y,CW,'body')-15
 for d in p['cards']:
  label=d['solution_id']+' | '+d['title'];q=Paragraph(markup(label),ST['label']);_,th=q.wrap(CW-20,600)
  text='**Already:** '+d['existing_baseline']+'<SEP>**Possible:** '+d['possible_addition']+'<SEP>**Could fail if:** '+d['what_could_kill_it']
  text=text.replace('<SEP>','\n');a=Paragraph(markup(text),ST['card']);_,bh=a.wrap(CW-20,600);height=th+bh+24
  assert y-height>=112,(c.getPageNumber(),d['solution_id'],'option card overflow',y-height)
  c.setStrokeColor(colors.HexColor('#D5E1E8'));c.line(M,y+3,M+CW,y+3);yy=para(c,label,M+10,y-5,CW-20,'label')-6;para(c,text,M+10,yy,CW-20,'card',min_y=112);y-=height+10
 para(c,'All benefits remain hypotheses. Full evidence, dependencies and alternative explanations: reports/SOLUTION_MENU.json and workstreams/extension_stakeholders/all_27_option_audit.json.',M,85,CW,'small',min_y=46)
def guide(c):
 y=H-76;y=para(c,'Use this story to navigate the full research.',M,y,CW,'title')-19
 items=[('Read the complete analysis','Workstream reports and16cross-source insight cards retain details that are intentionally short here.'),('Continue in another AI session','context/Auto2000_Master_AI_Context_Updated.md contains the extensive updated case context, evidence capsules, corrections and open questions.'),('Inspect the underlying data','raw_licensed_data/ contains the original permitted source files. The primary download includes both617,722-row IGAR label views and the five exact telemetry MAT bundles.'),('Reproduce the supported calculations','Code, source hashes, datasets, numerical checks and scope notes are included. Some historical live-web recipes still need omitted source caches; this is not a one-click replay of the internet.'),('Use the correct archive variant','The public backup omits original IGAR review text for privacy. For smaller hosts, the core plus five whole-MAT ZIP volumes extract into the same directory. The main ZIP retains the original licensed files.'),('Keep the earlier work','Both previous ZIP releases are included unchanged. Their plans and ceilings are historical; the final reports explain what was actually completed.')]
 for title,body in items:
  y=para(c,title,M,y,CW,'label')-5;y=para(c,body,M,y,CW,'body')-17
 para(c,'Style inspiration: the supplied four-page audit PDF, used only for layout. No unrelated case facts or artwork were imported. This is a research reading edition, not a competition submission or implementation plan.',M,93,CW,'small',min_y=46)

if PDF.exists():
 drafts=ROOT/'private_cache/pdf_drafts';drafts.mkdir(parents=True,exist_ok=True);shutil.copy2(PDF,drafts/'technical_compendium_draft.pdf')
c=canvas.Canvas(str(PDF),pagesize=A4,pageCompression=1);c.setTitle('Auto2000 Digiroom: a visual research story');c.setAuthor('Research synthesis')
for n,p in enumerate(pages,1):
 kind='(guessing) POSSIBLE DIRECTIONS' if p.get('type')=='options' else p.get('kind','RESEARCH STORY')
 basic(c,n,len(pages),kind);key='page-'+str(n);c.bookmarkPage(key);c.addOutlineEntry(clean(p['headline']),key,0)
 if p.get('type')=='cover':cover(c,len(pages))
 elif p.get('type')=='options':options(c,p)
 elif p.get('type')=='file_guide':guide(c)
 else:regular(c,p)
 c.showPage()
c.save()
from pypdf import PdfReader
r=PdfReader(str(PDF));text='\n'.join(p.extract_text() or '' for p in r.pages);assert len(r.pages)==len(pages)
receipt={'file':str(PDF.relative_to(ROOT)),'edition':'readable_visual_story','pages':len(r.pages),'words_extracted':len(text.split()),'bytes':PDF.stat().st_size,'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'actual_chart_files':len(list(FIG.glob('*.png'))),'source_assets':source_assets,'research_scope_reduced':False,'full_research_reports_and_raw_in_zip':True,'visual_qa_pending':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(ROOT/'reports/STORY_PDF_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2));(ROOT/'reports/STORY_PAGE_PLAN.json').write_text(json.dumps(pages,indent=2));(ROOT/'reports/STORY_LAYOUT_BOUNDS.json').write_text(json.dumps(bounds,indent=2))
md=['# Auto2000 visual research story','']
for n,p in enumerate(pages,1):
 md += [f"## {n}. {p['headline']}",'',p.get('body',''),'',p.get('takeaway',''),'',p.get('limit',''),'',p.get('source',''),'']
(ROOT/'reports/STORY_READING_TEXT.md').write_text('\n'.join(md))
print(json.dumps(receipt))
