from pathlib import Path
import json,csv
out=Path(__file__).resolve().parent;rows=json.loads((out/'claim_matrix.json').read_text())
findings=[
'Zurich publicly offers EV-specific syariah motor protection.',
'The product object specifies four-wheel battery-electric vehicles.',
'Total package: charging battery and vehicle each Rp100 million/year; charger Rp20 million/year.',
'Flood is included in Total Protection and optional in Custom packages.',
'Authorized-brand workshop benefit is optional in comprehensive packages.',
'Battery-fire deductible is 5%; flood is 10%, minimum Rp500,000.',
'Exclusions mention wear, intrinsic material defects and misuse.',
'Autocillin Mobile Claim already handles reporting, validation and repair authorization.',
'Contribution includes acquisition costs; no Auto2000 fee share is specified.',
'Fund use and insurer fees follow the stated insurance contract.',
'Astra describes syariah motor/Garda Oto products with distinct policy wording.',
'Garda distinguishes partial/total loss and lists reduced-price/financial-loss exclusions under stated standard terms.',
'Garda already provides claims, survey, repair authorization and workshop channels.',
'Astra announces hydraulic flatbed EV evacuation and AstraWorld collaboration.',
'Jasindo describes comprehensive/TLO, optional flood and nature-of-object exclusions.',
'Jasindo specifies notice, documents and insurer investigation before repair.',
'The 70% trade-in programme applies in months 25–36 to named Stargazer/Creta variants.',
'Original ownership, 60,000 km maximum, authorized servicing, condition and document rules apply.',
'VinFast campaign advertises an up-to-80% resale guarantee subject to terms.',
'RVI Group describes future-value coverage for properly maintained assets.',
'RVI Group describes custom policies for banks, finance companies, lessors and fleets.',
'The published rule requires insurable risk and appropriate contribution.',
'Marketing channels, written agreements and accurate remote information are regulated.',
'Sharia products require a relevant fatwa/basis and DPS opinion on actual product, risk and contract.',
'SEOJK 14/2024 addresses product approval/reporting and DPS-opinion procedures.',
'The DSN directory lists insurance wakalah and tabarru fatwas.',
'Fatwa 52 addresses participant authority granted to the insurer with ujrah.',
'IFRS 17 excludes certain manufacturer/dealer residual guarantees from its scope.',
'OJK lists a 2025 syariah asset/liability rule covering related fund management.'
]
implications=[
'An existing product category; dealer value and customer demand remain unknown.',
'Do not assume automatic HEV or PHEV eligibility.',
'Actual selected policy governs; insured amounts are not dealer income.',
'Compare the selected package rather than a generic brand headline.',
'Auto2000 routing needs insurer/workshop eligibility; it is not automatic.',
'Customer out-of-pocket exposure remains.',
'Accidental battery protection is not proof of normal-capacity-decline cover.',
'A new claim app would duplicate an existing function unless specific extra value is established.',
'Insurer ujrah or acquisition cost is not a verified dealer commission.',
'An akad label does not create residual-value cover.',
'No matching EV endorsement or signed Digiroom distribution agreement was verified.',
'Ordinary motor cover is not confirmed market-depreciation insurance.',
'Test the incremental value of coordination against the existing insurer workflow.',
'Evacuation capability does not establish battery or charging policy cover.',
'No explicit residual-price-loss benefit was identified on this page.',
'Scheduling and claim approval remain distinct decisions.',
'This is not a verified Hyundai BEV floor or proof of insurer backing.',
'Eligibility controls redemption; no named insurer does not prove absence of insurer funding.',
'Tenor, settlement basis and insurance backing were not verified here.',
'This does not verify Indonesian availability or local authorization.',
'No Indonesian syariah quote or automatic dealer eligibility was established.',
'Acceptance of pure-market-depreciation risk in a proposed contract remains unresolved.',
'Actual arrangements require insurer/regulatory assessment; this is not a legality opinion.',
'General fatwas are not product-specific approval of a new RVI design.',
'The route applicable to a specific new product remains unresolved.',
'Directory presence alone establishes no product approval.',
'It does not establish a specific dealer commission agreement.',
'Accounting classification establishes neither local authorization nor sharia certification.',
'This workstream does not certify an exhaustive current legal or compliance position.'
]
for i,r in enumerate(rows):r['scoped_finding']=findings[i];r['research_implication']=implications[i]
rows[13]['retrieval_ref']='turn602562615search0';rows[13]['document_locator']='official release section on EV-friendly emergency service; search-retrieved full section'
(out/'claim_matrix.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (out/'claim_matrix.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
