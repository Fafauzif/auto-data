from pathlib import Path
import json,csv,re
out=Path(__file__).resolve().parent
rows=json.loads((out/'sources.json').read_text())
methods={
'MS01':'IEA compiled market data; electric-car definitions exclude conventional HEVs.',
'MS02':'Survey analysis; question-specific bases must be checked in the underlying SEA report.',
'MS03':'Driving-age online panel via email; Indonesia total n=1,004, service bases n=629 or 618; not a dealer census.',
'MS04':'General technical guidance; model-specific manufacturer schedules control.',
'MS05':'Published eligibility and certificate terms; no adoption or outcome measurement.',
'MS06':'Published program design; no dealer cost or reimbursement data.',
'MS07':'Advertised PLN Mobile and installation routes; no live uptime test.',
'MS08':'Qualtrics survey n=1,490: 490 BEV owners and 1,000 potential buyers; new/preowned question groups 752/738.',
'MS09':'Separate Java 2W/4W surveys of 680 respondents each; 5,440 repeated choices per survey; stakeholder FGDs and interviews.',
'MS10':'181 of 580 responses retained: EV affordability, urban residence, ICE ownership and EV interest; cross-sectional PLS-SEM.',
'MS11':'Purposive automotive-community recruitment, n=230; millennial birth-year screen; self-reported PLS-SEM.',
'MS12':'Purposive n=140 ICE-vehicle owners; online survey and PLS; Java-majority sample.',
'MS13':'Retrospective survey of 2,300 recent US purchasers; nonbuyers excluded; vendor incentives relevant.',
'MS14':'Feature announcement; no controlled conversion estimate.',
'MS15':'Published Recurrent and Treehouse mechanisms; no measured commercial uplift.',
'MS16':'UK warranty terms and record mechanism; not Indonesian entitlement.',
'MS17':'Operator-described inspection, history and warranty bundle; no comparative effect established.',
'MS18':'51,228 verified registered owners/lessees of one- to three-year-old vehicles; repair data included; not an experiment.',
'MS19':'Published channel/satisfaction comparison; self-selection and context confounding remain.',
'MS20':'3,175 owners; service events August 2016–September 2017; historical mechanism evidence only.',
'MS21':'5,741 model-year 2025/2026 BEV/PHEV owners; first-year experience and consideration, not realized repurchase.',
'MS22':'Public subscription terms; current contract, model and availability control.',
'MS23':'Published estimate-to-inspection process; no appraisal submitted.',
'MS24':'Advertised simulation, verification and partner process; no approval or quote observed.'}
for r in rows:
 r['method_and_sample']=methods[r['source_id']]
 for k in ['evidence_period']:
  r[k]=re.sub(r'([A-Za-z])([0-9])',r'\1 \2',r[k])
  r[k]=re.sub(r'([0-9])([A-Za-z])',r'\1 \2',r[k])
(out/'sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
fields=list(dict.fromkeys(k for r in rows for k in r))
with (out/'sources.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
assert len({r['source_id'] for r in rows})==len(rows)
print('Source metadata refined',len(rows))
