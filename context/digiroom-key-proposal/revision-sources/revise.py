from pathlib import Path
from copy import deepcopy
import re,json,textwrap
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'drafts/Digiroom_KEY_Chapters_1_and_2_Revised.docx'; ASSET=ROOT/'revision-sources/charts';ASSET.mkdir(exist_ok=True)
d=Document(ROOT/'drafts/Digiroom_KEY_Chapters_1_and_2.docx'); orig=list(d.paragraphs); tables=list(d.tables)
serial=6000
RED='#8F2030';BLUE='#315E73';GRAY='#52616B'
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
def link(p,label,target):
 h=OxmlElement('w:hyperlink');h.set(qn('w:anchor'),target);r=OxmlElement('w:r');pr=OxmlElement('w:rPr')
 for tag,val in [('color','8F2030'),('u','single')]:
  e=OxmlElement('w:'+tag);e.set(qn('w:val'),val);pr.append(e)
 r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);h.append(r);p._p.append(h)
def bookmark(p,name):
 global serial
 serial+=1;a=OxmlElement('w:bookmarkStart');a.set(qn('w:id'),str(serial));a.set(qn('w:name'),name);b=OxmlElement('w:bookmarkEnd');b.set(qn('w:id'),str(serial));p._p.extend([a,b])
def settext(p,text):
 # Keep original paragraph properties, numbering, and bookmarks.
 for el in list(p._p):
  if el.tag not in [qn('w:pPr'),qn('w:bookmarkStart'),qn('w:bookmarkEnd')]:p._p.remove(el)
 for part in re.split(r'(\[A\d+(?:\.\d+)?\])',text):
  if re.fullmatch(r'\[A\d+(?:\.\d+)?\]',part):link(p,'Appendix '+part[1:-1],part[1:-1].replace('.','_'))
  else:p.add_run(part)
def after(el,text='',style='normal'):
 p=d.add_paragraph(style=style);settext(p,text);el.addnext(p._p);return p
# New text is authored as complete paragraphs, with claim-specific evidence links.
rewrite={
4:"Auto2000’s relationship with a customer extends well beyond the showroom. Through vehicle sales, servicing, spare parts, and body and paint, the business can support a Toyota from its first purchase through years of use and eventual replacement. Digiroom brings those activities into a digital channel, alongside the branch relationships customers already maintain through WhatsApp, phone calls, and workshop visits.",
5:"That relationship is becoming more important as Indonesia’s vehicle market shifts towards electrification. xEVs accounted for 21.8% of new-car wholesales in 2025, up from 11.9% a year earlier. Toyota held 51% of hybrid sales, giving Auto2000 a substantial position in a market where hybrids and battery electric vehicles meet different ownership needs. Meanwhile, aftersales generated 46.7% of gross profit across powertrains. Sustaining that contribution requires Auto2000 to remain useful between purchases, even as servicing needs change. [A1]",
7:"The challenge is to turn Digiroom into a useful part of owning an xEV: helping a household choose an xEV through Auto2000, helping an owner complete the right service work, and helping an existing customer move into the next vehicle. Regular use matters when it supports these decisions and gives Auto2000 another opportunity to earn the customer’s business.",
9:"Most service bookings already happen elsewhere, so Digiroom needs a role beyond taking the request.",
10:"WhatsApp accounts for 38% of Auto2000’s service bookings, while phone calls and walk-ins account for another 46%. Digiroom handles the remaining 16%, despite service booking being the main activity for 46% of its monthly active users. These are different measures, but together they reveal the central challenge: booking is important inside the app, while the business still receives most bookings outside it. [A1] The Yaris Cross Hybrid driver described booking through WhatsApp as practical and consistently successful; the Wuling driver reported the same convenience with a different dealer. [A21] [A22]",
13:"For these owners, another booking form offers little reason to change an established habit. The opportunity comes as the service progresses: the branch confirms the work, an estimate changes, or a family member needs to approve the cost. Digiroom already offers booking and tracking, so its value depends on how well those functions help customers act at these moments. [A2] With about 21,000 monthly active users and 1.6 sessions per active user, the task is to create useful reasons to return after the initial request, while following whether the service itself goes ahead. [A1]",
14:"Choosing Auto2000 does not guarantee that the workshop wins the job.",
15:"A customer can arrive intending to pay and still leave before any work begins. One Setiabudi reviewer described exactly that: arriving for service, waiting without being received, and leaving dissatisfied. A Pancing account points to a different breakdown, where a walk-in registration reportedly never entered the queue. [A4] Elsewhere, the decision changed at the estimate. A Kertajaya Avanza owner rejected a larger brake replacement proposal and chose a cheaper repair outside Auto2000; the account does not establish whether the repairs were technically equivalent. [A4]",
18:"These accounts locate the problem at different stages of a visit, from reception to agreement on the work. Cilandak provides a useful contrast: a reviewer described being consulted before extra work, with clear charges and follow-up. Soekarno-Hatta accounts instead describe missed or unresolved work and further visits. [A4] The Yaris interview adds another practical detail: the driver arranges the visit, but the father decides on additional spending. [A22] An adviser therefore needs to keep the workshop’s explanation and the payer’s decision together as the job changes.",
19:"The household needs to try the xEV against its own routine.",
20:"Charging was a settled part of daily life for the interviewed Wuling driver. The car was charged at the apartment when its battery reached around 30%, leaving the driver free to rest or continue other activities. [A21] The Atto driver described a less forgiving situation: on one low-charge trip, urgency led to taking Gojek; on another, the driver searched for charging near Rungkut. [A23] The difference is what access allows each household to do when time is tight. A charger count alone cannot explain it. [A19]",
23:"For a hybrid household, the unanswered questions may concern fuel use, passengers, or performance on familiar roads. The Yaris driver, for example, described a long trip with friends and a different acceleration response under load. [A22] A household checklist gives those questions a place in the test drive, but the requested model must also be available: a separate X account described a prospect unable to find a demonstrator. [A15] Garage and cabin checks, a confirmed drive, and a 48-hour option for suitable households are design choices that follow from these needs; the interviews do not establish a preferred test duration. [A5]",
24:"A lower upfront payment can make the monthly commitment harder to carry.",
25:"The Zenix Hybrid calculator comparison shows why affordability needs more than one number. Financing insurance reduced the displayed cash due upfront from Rp154.85 million to Rp109.53 million, a difference of Rp45.31 million. Each of the remaining 59 instalments, however, rose from Rp9.27 million to Rp10.40 million. [A6] For a buyer working within an upfront budget, that change can make the offer easier to enter while increasing the commitment that follows.",
28:"Both calculations used the same model, location, vehicle price, base down payment, and tenor. Because the first instalment was included upfront, the comparison applies the monthly difference to the 59 payments still due. The result is a change in payment timing, not a whole-transaction saving. [A6] A household weighing the offer needs the cash due today, the continuing instalment, and its expected running costs presented together, especially when the driver and the person financing the car are different people. [A22]",
29:"Existing OtoXpert outlets close many oil-service access gaps, but Bandung retains most of the remainder.",
30:"The four-city model identifies 39 origins where an oil-service alternative is more than five minutes faster than the dealer network. Including eligible Auto2000-operated OtoXpert outlets reduces that count to 20 across the same 284 origins. [A7] The improvement is uneven. Medan and Palembang have no remaining origins above the threshold, while Bandung retains 14 and Surabaya six. [A8] Eight of Bandung’s remaining origins are assigned to Soekarno-Hatta, concentrating the case for better visit preparation and suitable Home Service around a specific branch area. [A9]",
33:"Oil-service access is only one part of the network decision. Pancing and Tanjung Api-Api have no remaining oil gaps above five minutes, yet removing them from the general-workshop model leaves eight and seven origins respectively without a dealer within 15 minutes. [A9] Their repair and diagnostic role remains important even where an operated outlet can take an oil job. Routing should therefore follow the work and the vehicle’s eligibility. The model compares locations and travel times; it does not measure customer demand, workshop capacity, or live traffic. [A7]",
34:"The near-term paid-service opportunity lies in cars already on the road.",
35:"New-car growth does not immediately translate into customer-paid scheduled servicing. Toyota’s T-Care programme includes up to seven scheduled services within three years or 60,000 km, whichever comes first, for eligible vehicles (Toyota Astra Motor, n.d.). In a time-only illustration, a January 2026 delivery reaches its seventh visit in January 2029 and its eighth in July 2029, beyond the 2026–2028 investment window. [A10] The Yaris driver’s routine work was still covered, illustrating why a completed hybrid service visit cannot automatically be counted as customer-paid revenue. [A22]",
38:"Paid opportunities can arise earlier through mileage or uncovered work, and older vehicles may already have passed their included-service period. The commercial starting point is therefore the installed base and the work actually due, with coverage checked for each vehicle and item. [A10] A visit can combine included maintenance with an extra repair that requires the owner’s approval. Digiroom can help the family understand that distinction, while Auto2000 separates customer payments from covered work and programme reimbursement. Petrol work supports the wider service opportunity; xEV contribution still needs to be identified separately.",
39:"A trade-in price only becomes useful when the owner can close the next purchase.",
40:"The Yaris driver had already checked marketplaces and dealers to establish a resale range. [A22] That gives an owner a starting point, but it does not say how much money is available for the next car. An inspected buy offer still needs to be reconciled with the lender’s payoff and any fees. In the worked example, a Rp248 million offer becomes Rp71.5 million of usable equity after a Rp174 million payoff and Rp2.5 million in fees. [A12] The family can then compare the replacement against the amount it actually has.",
43:"Timing can still prevent the deal from closing. Selected accounts describe difficulty recovering a deposit and a reserved vehicle reportedly being allocated elsewhere, showing why appraisal, finance, and stock cannot be treated as unrelated steps. [A11] The adviser needs to align the offer’s expiry with the replacement unit and settlement dates, and explain what happens to a deposit if the purchase falls through. These accounts do not identify xEVs, but they reveal transaction dependencies that the upgrade journey must address.",
44:"An existing appraisal interface already addresses part of this journey. The stronger proposition is to carry an accepted offer through to payoff and a secured replacement, with revised terms returned to the owner whenever one of those commitments changes. [A2] [A12]",
45:"The analysis converges on three decisions that Digiroom must help customers finish.",
46:"For acquisition, the household must settle whether the xEV fits its routine and budget. For service, the owner must choose a capable outlet and agree to work the workshop can complete. For replacement, the family must know its usable equity and be able to secure the next car. The issue tree consolidates these causes into buying, service, and upgrade, linking each to the evidence developed above. [A13]",
49:"Together, these findings give Digiroom a role throughout ownership. The app becomes useful when a real decision moves: a demonstrator is confirmed, extra work needs approval, or an upgrade offer is ready. Sales and workshop teams carry the same decision through their existing assisted channels, so the customer does not have to restart the explanation at each handoff.",
50:"Commercial performance follows three separate outcomes: an xEV delivered to a customer new to Auto2000, a completed customer-paid service order, and a repeat xEV delivery. Tracking those outcomes across channels distinguishes additional business from bookings that simply moved into Digiroom. [A13]",
12:"Figure 1. Service booking channels and the main activities of Digiroom’s monthly active users.",
17:"Figure 2. Where reported service journeys succeed or break down. Sources: Google Maps reviews; owner interviews.",
22:"Figure 3. Household routines create different questions for an xEV test drive. Sources: owner interviews; selected X account.",
27:"Figure 4. Cash due upfront and continuing instalments in the dated Zenix Hybrid comparison.",
32:"Figure 5. Origins above the five-minute oil-access gap, before and after eligible OtoXpert routing.",
37:"Figure 6. Included-service calendar for an eligible January 2026 delivery; time-only illustration.",
42:"Figure 7. From appraisal to usable equity and a settled replacement. Sample transaction terms.",
48:"Figure 8. Consolidated issue tree linking buying, service, and upgrade to commercial outcomes."
}
for i,t in rewrite.items():settext(orig[i],t)
# Remove the redundant main-body trade-in table; prose now develops the point.
tables[0]._tbl.getparent().remove(tables[0]._tbl)
# Remove casebook attribution everywhere, retaining the supplied baseline facts.
orig[57]._p.getparent().remove(orig[57]._p)
for p in list(d.paragraphs):
 if p is orig[57]:continue
 if 'IBSC (' in p.text or 'The casebook' in p.text or 'casebook' in p.text or 'Casebook' in p.text:
  t=p.text
  t=re.sub(r'\s*\(IBSC, 2026[^)]*\)','',t)
  t=t.replace('Casebook metrics','Business and market baseline').replace('The casebook supplies a common baseline for the market, Digiroom and the company economics. Each figure retains its original denominator.','The baseline separates market wholesales, app activity, booking channels, and gross profit. Each measure retains its own denominator.')
  t=t.replace('2025 hybrid sales in the casebook','2025 hybrid sales').replace('The casebook dates the Digiroom relaunch to December 2025','Digiroom relaunched in December 2025')
  t=re.sub(r'Source: IBSC \(2026\)[^.]*\.[^;]*;\s*','Source: ',t)
  t=t.replace('Source: IBSC (2026), pp. 3, 8, 10–11. ','').replace(' and the relaunch date in IBSC (2026, p. 4)','')
  t=t.replace('in the casebook','in the market baseline').replace('from the casebook','from the supplied baseline')
  settext(p,t)
for table in d.tables:
 for row in table.rows:
  for cell in row.cells:
   for p in cell.paragraphs:
    if 'casebook' in p.text.lower() or 'Case Exhibit' in p.text:
     settext(p,p.text.replace('The casebook lists','Digiroom includes').replace('The casebook identifies','Digiroom includes').replace('in the casebook','in the market baseline').replace('Case Exhibit 3;','Business-line baseline;'))
# Helper charts: exact quantitative comparisons or evidence sequences, never prevalence from selected accounts.
def savefig(fig,name):
 path=ASSET/(name+'.png');fig.savefig(path,dpi=220,bbox_inches='tight',facecolor='white');plt.close(fig);return path

def sequence(table,name):
 rows=[[c.text for c in r.cells] for r in table.rows][1:]
 fig,ax=plt.subplots(figsize=(9, max(2.6,len(rows)*.90)));ax.axis('off')
 for i,row in enumerate(rows):
  y=1-(i+.5)/len(rows)
  ax.text(.01,y,textwrap.fill(row[0],17),va='center',color=RED,weight='bold',fontsize=10)
  content=row[1]+('  Implication: '+row[2] if len(row)>2 else '')
  ax.text(.245,y,textwrap.fill(content,78),va='center',fontsize=10.5,linespacing=1.35)
  if i<len(rows)-1:ax.axhline(1-(i+1)/len(rows),color='#D9D9D9',lw=.6)
 return savefig(fig,name)
def replace_table(ix,path,caption):
 tbl=tables[ix]; el=tbl._tbl;p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(path),width=Cm(16.8));el.addprevious(p._p)
 cap=d.add_paragraph(caption,style='KEY Figure Caption');el.addprevious(cap._p);el.getparent().remove(el)
 return p
# Baseline: market progression and revenue/profit contrast.
fig,axs=plt.subplots(1,2,figsize=(9,2.5))
axs[0].bar(['2024','2025'],[11.9,21.8],color=[GRAY,RED]);axs[0].set_title('xEV share of new-car wholesales');axs[0].set_ylabel('%');axs[0].set_ylim(0,28)
for i,v in enumerate([11.9,21.8]):axs[0].text(i,v+.5,f'{v}%',ha='center')
axs[1].barh(['Revenue','Gross profit'],[13,46.7],color=[GRAY,RED]);axs[1].set_xlim(0,60);axs[1].set_title('Aftersales share across powertrains');axs[1].set_xlabel('%')
for i,v in enumerate([13,46.7]):axs[1].text(v+1,i,f'{v}%',va='center')
fig.tight_layout();bp=savefig(fig,'baseline')
# Retain exact baseline table; add graphical overview before it.
p=d.add_paragraph();p.add_run().add_picture(str(bp),width=Cm(16.8));tables[1]._tbl.addprevious(p._p)
for ix,name in [(2,'existing_journeys'),(4,'workshop_cases'),(5,'household_comparison'),(8,'branch_choices'),(13,'appraisal_cases'),(17,'x_accounts'),(18,'youtube_accounts')]:
 replace_table(ix,sequence(tables[ix],name),'Evidence comparison. Sources: '+({'existing_journeys':'Auto2000 public journeys and owner interviews.','workshop_cases':'selected Google Maps reviews and Yaris Cross Hybrid interview.','household_comparison':'owner interviews, selected X account, and Google Maps reviews.','branch_choices':'authors’ corrected workshop-routing calculations.','appraisal_cases':'owner interviews and selected Google Maps reviews.','x_accounts':'selected X ownership accounts, paraphrased.','youtube_accounts':'selected YouTube comments, paraphrased.'}[name]))
# Corpus summary and denominator mapping belong in prose, not repeated tables.
for ix,text in [(3,'The comparison draws on three owner interviews and a routing model with 284 paired origins across four markets. X, Google Maps, and YouTube provide separate sets of public accounts, with counts shown above. These sources describe different units and cannot be combined into a customer sample.'),(11,'Included scheduled service follows the vehicle’s programme, mileage, and time limits. A January 2026 delivery reaches visit seven in January 2029 in the time-only example above; earlier paid work depends on mileage or uncovered items.'),(15,'Buying leads to a first xEV delivery for a customer new to Auto2000; service leads to a completed customer-paid work order; upgrade leads to a repeat xEV delivery. The issue tree connects each outcome with its own customer decision.'),(20,'National xEV wholesales establish market context. Toyota’s model breakdown describes brand-level distribution, while a commercial service forecast needs Auto2000’s actual vehicle and job eligibility. Wholesale shares cannot supply that installed-base denominator.')]:
 el=tables[ix]._tbl;p=d.add_paragraph(text);el.addprevious(p._p);el.getparent().remove(el)
# Equity waterfall.
fig,ax=plt.subplots(figsize=(9,2.8));vals=[248,-174,-2.5,71.5];starts=[0,74,71.5,0];labels=['Inspected offer','Loan payoff','Fees','Usable equity']
for i,(v,s) in enumerate(zip(vals,starts)):
 ax.bar(i,abs(v),bottom=s,color=RED if i==3 else (BLUE if i==0 else '#9AA5AD'));ax.text(i,s+abs(v)+4,f'Rp{abs(v):g}m',ha='center')
ax.set_xticks(range(4),labels);ax.set_ylabel('Rp million');ax.set_ylim(0,285);ax.set_title('What the old car contributes to the replacement')
replace_table(14,savefig(fig,'equity'),'Sample terms: Rp248m offer − Rp174m lender payoff − Rp2.5m fees = Rp71.5m usable equity. Replacement stock, credit and settlement are confirmed separately.')
# App reviews coding chart; denominator is the 16 favorable reviews only.
fig,ax=plt.subplots(figsize=(9,2.5));ax.barh(['Specific app interaction','Unclear experience','Other / no experienced task'],[7,5,4],color=[BLUE,'#9AA5AD',RED]);ax.set_xlim(0,9);ax.set_xlabel('Reviews among 16 favorable records');ax.set_title('A favorable rating does not identify what the reviewer completed')
for i,v in enumerate([7,5,4]):ax.text(v+.12,i,str(v),va='center')
replace_table(16,savefig(fig,'app_tasks'),'Source: authors’ coding of selected Google Play reviews. In the original 20-record Indonesian-language view, 16 had four or five stars. Specific interactions can include failed attempts. Counting all five unclear records as interactions yields a coding range of 7/16–12/16. The original date comparison uses 50 Digiroom records; nine matched app-language selections showed zero overlap in displayed review IDs.')
# Add granular bookmark destinations to the first exhibit/table in each appendix.
body=list(d.element.body);current=None
for el in body:
 txt=''.join(el.xpath('.//*[local-name()="t"]/text()'))
 m=re.match(r'^A(\d+)\s{2}',txt)
 if m:current=m.group(1)
 if current and ('A'+current+'_1') not in {x.get(qn('w:name')) for x in d.element.xpath('.//w:bookmarkStart')} and (el.tag==qn('w:tbl') or el.xpath('.//*[local-name()="drawing"]')):
  from docx.text.paragraph import Paragraph
  if el.tag==qn('w:tbl'):
   new=d.add_paragraph();el.addprevious(new._p);bookmark(new,'A'+current+'_1')
  else:bookmark(Paragraph(el,d._body),'A'+current+'_1')
  current=None
# Repoint key quantitative links to the exact supporting exhibit.
for i in [25,28,30,33,40]:
 for h in orig[i]._p.xpath('.//w:hyperlink'):
  a=h.get(qn('w:anchor'))
  if a in ['A6','A7','A9','A12']:
   h.set(qn('w:anchor'),a+'_1')
   for t in h.xpath('.//w:t'):t.text=t.text+'.1'
questions=[
'Q01. When did you start using the car, and what part did you play in choosing it?',
'Q02. What did you handle in the most recent car-related task or payment?',
'Q03. Describe a recent journey and the decisions you made.',
'Q04. How did you manage charging or stops during the journey?',
'Q05. What was the latest maintenance or assistance task you handled?',
'Q06. What had to be decided before work could proceed, and how did it end?',
'Q07. Which alternatives were actually considered when the car was chosen?',
'Q08. Which costs were discussed or changed the purchase decision?',
'Q09. What were you trying to finish the last time you used a car-related app or conversation?',
'Q10. Have you taken any steps to value, sell, or replace a car?',
'Q11. Which part of the experience most needs improvement?',
'Q12. Was anything in the interviewer’s summary incorrect or incomplete?']
wuling=[
'The respondent has used a Wuling Air EV since 2023. Their father chose the model and dealer, arranged the transaction, and funded it. The respondent had not personally purchased or serviced a car at Auto2000; the family’s Toyota dealings were unknown to them.',
'The respondent arranges service through WhatsApp, takes the car to Wuling Soekarno-Hatta in Bandung, approves the work, and pays by transfer. Their father reimburses the expenditure.',
'Bandung–Jatinangor and ordinary university or activity trips had gone smoothly. The respondent reported no cancelled or diverted trips, or car substitution, during the previous two to four weeks.',
'The car is charged at the apartment when the battery reaches around 30%. The respondent rests or continues activities at home while it charges and reported no disruption to the routine.',
'The respondent handled a tyre replacement at Nawilis in Jakarta because it was a familiar workshop. They also described routine servicing roughly every three months at Wuling Soekarno-Hatta, booked through WhatsApp.',
'Service quality was the main consideration. The respondent paid first and was reimbursed by their father. They reported satisfactory completion without repeat visits, cancelled work, or transferring an unfinished job elsewhere.',
'The respondent did not know which other cars or dealers their father had considered. Their family has a Toyota, but they did not know whether Auto2000 had been consulted.',
'The respondent did not know the original price, down payment, instalments, or purchase-cost calculations because their father handled those decisions.',
'The latest conversation concerned a routine service booking through the Wuling workshop’s WhatsApp contact. The respondent did not use Digiroom, mTOYOTA, or a dedicated vehicle app for the task.',
'The family had sold or replaced vehicles, but their father handled those transactions. The respondent could not describe offers or settlement details.',
'The respondent identified no problem requiring improvement in the car, service arrangements, or ownership experience.',
'The respondent added no correction. Their role as driver and service organiser remained distinct from their father’s purchase and funding role.'
]
yaris=[
'The family bought a new 2024-model Yaris Cross Hybrid from Auto2000 and began using it in January 2025. The respondent contributed colour and model-year preferences. Their father chose the model and dealer, funded the purchase, and used an established sales relationship.',
'The respondent contacts the workshop, books the visit, drops off the car, and collects it. Routine service was still covered by the purchase package. Their father retains the final decision on extra work or spending.',
'The respondent described an approximately eight-hour return journey between Jatinangor and Tasikmalaya with friends. They chose the route and departure time. Under passenger load on hills, acceleration required more time and effort than when driving alone.',
'Stops were planned around tiredness, motion sickness, toilet needs, and stretches where stopping would be difficult. The respondent said fuel use and the trip broadly met expectations.',
'The respondent described routine servicing at mileage intervals or roughly every six months. They selected the nearby Auto2000 branch associated with the purchase, booked through WhatsApp, brought the service booklet, and collected the car after notification.',
'The work matched the initial agreement and was described as covered routine maintenance. Their father decides on extra work after the adviser explains the technical need. No work had been cancelled or transferred to another workshop.',
'The family moved from a Raize Turbo to the Yaris Cross Hybrid for reported fuel efficiency. The respondent did not identify another model seriously considered at that purchase. Their father chose Auto2000 through a long-standing contact.',
'The purchase discussion included vehicle price and fuel use compared with the Raize. Reported fuel savings met expectations, although fuel-price increases did not. Instalments were arranged around the selected 2024-model unit; amounts were not supplied.',
'The respondent last used the Auto2000 WhatsApp admin contact to arrange service timing. They described the task as consistently completed and preferred to keep using that channel.',
'The respondent had checked marketplaces and official dealers for resale information. They stopped once they had found a plausible average range for the car’s condition; no completed appraisal or sale was reported.',
'The respondent identified no current ownership or routine-service problem requiring improvement.',
'The respondent reported no correction to the interviewer’s summary and was willing to provide a later clarification.'
]
conceptq=[
'C1. Which part of the proposed service, purchase, or trade-in support could change your action?',
'C2. If price and technical results were the same, why choose or reject the proposed route?',
'C3. If an adviser or WhatsApp supplied the same information, what would still justify opening an app?',
'C4. What would you fill in, remove, or return to next?']
conceptw=[
'The respondent saw no urgency for the proposed service support because their existing arrangements worked.',
'They preferred the current method when the price and technical outcome were unchanged.',
'They identified no additional app task; WhatsApp was sufficient for workshop communication.',
'They did not see a reason to use the app for their own service task. Purchase and replacement decisions belonged to their father.'
]
concepty=[
'The respondent favoured trade-in support as a way to move beyond manually checking market prices.',
'They saw little personal relevance in purchase-planning support because their father already handled buying through a dealer contact.',
'They identified service details, cost estimates, and approval status as reasons to view a service record.',
'They would fill in trade-in information, remove purchase-planning content from their own flow, and revisit service status or approval. These were reactions to a described concept.'
]
attoq=[
'N1. Topic prompt: How do commuting and charging fit your routine?',
'N2. Topic prompt: What attracted you to the Atto, and who handled buying?',
'N3. Topic prompt: Were any offers rejected or negotiated?',
'N4. Topic prompt: Has a fault made the car unusable?',
'N5. Topic prompt: Have you researched resale or a replacement?',
'N6. Topic prompt: Would knowing a minimum trade-in value at purchase affect confidence?']
attoa=[
'The Sidoarjo–Surabaya university commute was described as fairly long. The respondent prefers locations with several chargers, such as PLN sites. On one urgent occasion with around 12% battery, they took Gojek. On a separate occasion near Rungkut, low charge led them to search for a nearby charger.',
'They had considered Wuling, then became interested in the newly released Atto because of its perceived price and the wish to try an EV. Their parents arranged the purchase.',
'The respondent did not know the negotiations because their parents handled them. They personally perceived the Atto as cheaper while offering comparable quality; no matched prices were provided.',
'They reported no fault that had immobilised the car or forced a substitute university trip because of breakdown. This is separate from the low-charge transport substitution described in N1.',
'They had not checked resale prices or sought a replacement because they were not planning to sell. They viewed lower running costs during ownership as an offset to possible future depreciation.',
'They preferred knowing a minimum future trade-in value from the outset and said it would increase purchase confidence. This was a stated preference, without a quoted floor, accepted terms, or purchase commitment.'
]
def interview(n,name,qs,answers,note):
 h=d.add_paragraph(f'A{n}  {name}',style='Heading 2');bookmark(h,'A'+str(n))
 p=d.add_paragraph();link(p,'Return to household analysis','claim3');p.add_run('  |  ');link(p,'Return to service analysis','claim2');p.add_run('  |  ');link(p,'Appendix index','appendix_index')
 d.add_paragraph(note)
 t=d.add_table(rows=1,cols=2);t.autofit=False;t.columns[0].width=Cm(6);t.columns[1].width=Cm(11)
 t.rows[0].cells[0].text='Question or topic';t.rows[0].cells[1].text='Interpreted answer'
 t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 for q,a in zip(qs,answers):
  c=t.add_row().cells;c[0].text=q;c[1].text=a
 d.add_paragraph('Source: anonymised '+name.lower()+'. Answers are English interpretations of the supplied Indonesian notes, not verbatim quotations. Reported experiences and concept reactions are distinguished above.')
interview(21,'Wuling Air EV owner interview',questions+conceptq,wuling+conceptw,'Interview A. The table translates and condenses the filled interviewer guide. Q01–Q12 follow the core questions; C1–C4 cover the recorded concept discussion. The service provider is Wuling Soekarno-Hatta, a separate business from Auto2000 Soekarno-Hatta. The interview date was not recorded in the supplied materials.')
interview(22,'Toyota Yaris Cross Hybrid owner interview',questions+conceptq,yaris+concepty,'Interview B. The table translates and condenses the filled interviewer guide. Q01–Q12 follow the core questions; C1–C4 cover reactions to the described concepts. The Auto2000 branch is not identified. The interview date was not recorded in the supplied materials.')
interview(23,'BYD Atto driver interview',attoq,attoa,'Interview C. Six numbered answer notes were supplied without the original question wording. Topic prompts below are reconstructed to organise those notes; they are not the original interview questions. Answers are interpreted summaries. The interview date and exact vehicle variant were not recorded.')
# Index additions, immediately before A1.
insert=next(p for p in d.paragraphs if p.text.startswith('A1  Aftersales'))
p=insert.insert_paragraph_before();link(p,'A21  Wuling Air EV interview','A21');p.add_run('  |  ');link(p,'A22  Yaris Cross Hybrid interview','A22')
p=insert.insert_paragraph_before();link(p,'A23  BYD Atto interview','A23')
# Complete borders, restrained headers, and explicit spacing throughout.
for t in d.tables:
 pr=t._tbl.tblPr
 for b in list(pr.findall(qn('w:tblBorders'))):pr.remove(b)
 borders=OxmlElement('w:tblBorders')
 for side in ['top','left','bottom','right','insideH','insideV']:
  e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'5');e.set(qn('w:color'),'AAB1B7');borders.append(e)
 pr.append(borders)
 for ri,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for cell in row.cells:
   cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for b in list(cell._tc.get_or_add_tcPr().findall(qn('w:tcBorders'))):cell._tc.tcPr.remove(b)
   if ri==0:
    sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E9EDF0');cell._tc.tcPr.append(sh)
   for p in cell.paragraphs:
    p.paragraph_format.space_before=Pt(3);p.paragraph_format.space_after=Pt(3);p.paragraph_format.keep_with_next=False
    for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(12);r.bold=ri==0
# Main heading, numbering, indentation and section properties remain from the original file.
for p in d.paragraphs:
 pf=p.paragraph_format
 pf.space_after=Pt(6)
 if p.style.name.startswith('Heading'):
  pf.space_before=Pt(8);pf.space_after=Pt(8);pf.keep_with_next=True
 else:
  pf.keep_with_next=bool(p._p.xpath('.//w:drawing'));pf.widow_control=True
 if p.style.name=='normal' and p.text and not p._p.xpath('.//w:hyperlink'):
  pf.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
# Add more separation after each section's concluding paragraph.
for p in d.paragraphs:
 nxt=p._p.getnext()
 if nxt is not None and nxt.tag==qn('w:p') and nxt.xpath('./w:pPr/w:pStyle[contains(@w:val,"Heading")]'):
  p.paragraph_format.space_after=Pt(10)
# Remove residual casebook tokens and stale references, while retaining genuine source labels.
for p in d.paragraphs:
 if 'IBSC (2026)' in p.text or 'casebook' in p.text.lower():
  t=re.sub(r'IBSC \(2026\),?\s*(?:pp?\.\s*[\d,–—\- ]+)?;?\s*','',p.text)
  t=t.replace('Casebook','Business baseline').replace('casebook','baseline')
  settext(p,t)
# Rebuild the contents field so it no longer displays inherited dummy page numbers.
for field in d.element.body.xpath('.//w:instrText'):
 if 'TOC' in (field.text or ''):
  pass
settings=d.settings.element; update=OxmlElement('w:updateFields');update.set(qn('w:val'),'true');settings.append(update)
# Repair final navigation, prose, and front matter after all transformations.
for p in d.paragraphs:
 if p.text.startswith('A1  Business and market baseline'):
  settext(p,'[A1] Business and market baseline  |  [A2] Existing Digiroom journeys')
 if p.text.startswith('Digiroom relaunched in December'):
  settext(p,'Digiroom relaunched in December 2025, with Single ID providing an existing CRM foundation. The public-journey review and owner interviews above distinguish the available entry points from the decisions that follow. Sources for the journey comparison: Auto2000 public pages and owner interviews.')
 if 'rating,.' in p.text:
  settext(p,p.text.replace('rating,.','rating.').replace('rating, .','rating.'))
 if 'calendar' in p.text and 'example above' in p.text:
  settext(p,p.text.replace('example above','example in Figure 6'))
# A9.1 refers to the full corrected destination table.
for e in d.element.xpath('.//w:bookmarkStart'):
 if e.get(qn('w:name'))=='A9_1': e.set(qn('w:name'),'A9_overview')
bookmark(next(p for p in d.paragraphs if p.text.startswith('A9.1  Corrected workshop destinations')),'A9_1')
# Keep appendix introductions with the first evidence row or visual.
for p in d.paragraphs:
 if p.text.startswith(('Interview A.','Interview B.','Interview C.')):p.paragraph_format.keep_with_next=True
# Use a current, linked contents list rather than inherited field-result text.
for el in list(d.element.body):
 if el.tag==qn('w:sdt'):el.getparent().remove(el)
entries=[('EXECUTIVE SUMMARY','summary'),('CHAPTER I: INTRODUCTION','intro'),('CHAPTER II: ANALYSIS','analysis')]+[(f'{i}. '+orig[ix].text,'claim'+str(i)) for i,ix in enumerate([9,14,19,24,29,34,39,45],1)]+[('CHAPTER III: RECOMMENDATIONS','recommendations'),('CHAPTER IV: IMPLEMENTATION AND IMPACTS','implementation'),('CHAPTER V: CONCLUSION','conclusion'),('REFERENCES','references'),('APPENDICES','appendix_index')]
for ix,key in [(1,'summary'),(51,'recommendations'),(52,'implementation'),(53,'conclusion')]:bookmark(orig[ix],key)
cursor=orig[0]._p
for label,target in entries:
 p=after(cursor);link(p,label,target);p.paragraph_format.space_after=Pt(6);p.paragraph_format.keep_with_next=False
 p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.left_indent=Cm(0)
 if target.startswith('claim'):p.paragraph_format.left_indent=Cm(.45)
 cursor=p._p
# Front matter gets its own page; chapters and exhibits still flow continuously.
orig[1].paragraph_format.page_break_before=True
d.core_properties.title='Digiroom KEY Chapters 1 and 2';d.core_properties.comments='';d.save(OUT)
# Evidence and preservation checks.
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
anchors={e.get(qn('w:name')) for e in d.element.xpath('.//w:bookmarkStart')}
links=[e.get(qn('w:anchor')) for e in d.element.xpath('.//w:hyperlink') if e.get(qn('w:anchor'))]
missing=sorted(set(links)-anchors)
report={'output':str(OUT),'tables':len(d.tables),'figures':len(d.inline_shapes),'internal_links':len(links),'missing_link_targets':missing,'interview_answer_rows':[16,16,6],'casebook_tokens':sum('casebook' in p.text.lower() or 'IBSC (2026)' in p.text for p in d.paragraphs),'margins_cm':[{k:round(getattr(s,k).cm,2) for k in ['left_margin','right_margin','top_margin','bottom_margin']} for s in d.sections]}
(ROOT/'revision-sources/structural_qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));assert not missing
