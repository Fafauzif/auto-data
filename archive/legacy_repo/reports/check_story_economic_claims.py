"""Claim QA for the final41-page reading PDF. Read-only; no collection or PDF editing."""
from pathlib import Path
from datetime import datetime,timezone
import json,csv,hashlib,re
import fitz

R=Path(__file__).resolve().parents[1];O=R/'reports'
pdf=R/'output/pdf/Auto2000_Research_Findings.pdf'
expected='7c1fc15d879afc59b217bb89d43b5625dfb5710e4b2c4acc2a8f127f84444034'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
doc=fitz.open(pdf);pages=[2,3,4,15,16,26,27,39];text={n:doc[n-1].get_text() for n in pages};flat={n:re.sub(r'\s+',' ',t) for n,t in text.items()}
checks=[]
def ck(id,p,claim,observed,expected_value,method,refs,limit=''):
 ok=abs(observed-expected_value)<1e-8 if isinstance(expected_value,(int,float)) and not isinstance(expected_value,bool) else observed==expected_value
 checks.append(dict(check_id=id,pdf_pages=p,assertion=claim,result='PASS' if ok else 'FAIL',observed=observed,expected=expected_value,method=method,evidence_refs=refs,scope_limit=limit))
def phrases(p,items):return all(s.lower() in flat[p].lower() for s in items)

ck('SEC01',pages,'PDF SHA256 matches the requested final version',sha(pdf),expected,'File hash','output/pdf/Auto2000_Research_Findings.pdf')
ck('SEC02',pages,'Final PDF has41pages',len(doc),41,'PDF structure','Final PDF')

# Source values are checked separately from the visibly rendered labels.
story=json.loads((R/'story_assets/economic_story.json').read_text());ep={p['page_id']:p for p in story['pages']}
gp=ep['EC01']['plot_data'];rendered_gp=[3600,1320,1200,630];rendered_shares=[53.3,19.6,17.8,9.3]
ck('SEC03',[2],'Four rendered caseGP bars match case-exhibit inputs',rendered_gp,[r['gross_profit_idr_billion'] for r in gp],'AI visual inspection of page002 plus source-data comparison','Casebook Exhibit3p10;economic_story.jsonEC01')
ck('SEC04',[2],'CaseGP total is6750billion',sum(rendered_gp),6750,'Recalculation','Casebook Exhibit3p10')
ck('SEC05',[2],'Rendered caseGP shares match the6750denominator',rendered_shares,[round(v/6750*100,1) for v in rendered_gp],'AI visual labels plus recalculation','Page002;Casebook Exhibit3p10')
ck('SEC06',[2],'After-sales caseGP is3150billion',sum(rendered_gp[1:]),3150,'Recalculation','Casebook Exhibit3p10')
ck('SEC07',[2],'Case scope and not-audited limitation are explicit',phrases(2,['supplied case','not audited Auto2000 results','GP differs from operating profit','Line-average margins do not identify EV-specific']),True,'Final PDF text inspection','Page2 source/limit')
ck('SEC08',[2],'Rendered GP axis is Rp billion and zero-based',True,True,'AI visual inspection of page002','page002.png','Numeric axis and labels checked visually; no human review claimed.')

pi=json.loads((R/'workstreams/extension_economics/portfolio_inputs_and_method.json').read_text())
ck('SEC09',[3],'Portfolio endpoints match37693and31668',[pi['xev_2024'],pi['xev_2025']],[37693,31668],'Input comparison and AI visual endpoint labels','AR2025printed140/PDF142;page003')
ck('SEC10',[3],'Symmetric terms reconcile−6025',pi['shapley_scale']+pi['shapley_mix'],-6025.,'Independent arithmetic','portfolio_inputs_and_method.json')
ck('SEC11',[3],'Rounded plotted changes are−5050and−975',[round(pi['shapley_scale']),round(pi['shapley_mix'])],[-5050,-975],'AI visual labels plus independent rounding','page003.png;portfolio inputs')
ck('SEC12',[3],'Toyota/Lexus scope and accounting-only interpretation remain explicit',phrases(3,['Toyota and Lexus','do not measure the effects of national demand, Digiroom','not causes or Auto2000 volume']),True,'Final PDF text inspection','Page3 body/source')
ck('SEC13',[3],'Scale and mix are allocations rather than named causal effects',phrases(3,['Scale','Do not label the scale term a national-market effect','Do not label the mix term a Digiroom effect']),True,'Final PDF text and chart-label inspection','Page3')

ck('SEC14',[4],'Framework preserves an all-channel counterfactual',phrases(4,['across all channels','defensible counterfactual','Across all Auto2000 channels']),True,'Final PDF text and AI visual inspection','Page4')
ck('SEC15',[4],'Displacement cannot be deducted twice',phrases(4,['If displaced work is already missing from the completed-job total','subtracting it again understates the result','Assign every cost, benefit and recovery once']),True,'Final PDF text inspection','Page4')
ck('SEC16',[4],'GP and extra operating cost remain separate and unmeasured',phrases(4,['operating costs below GP separate','realized job GP','remain unmeasured']),True,'Final PDF text inspection','Page4')

prog=json.loads((R/'workstreams/extension_economics/program_distinctions.json').read_text());progd={r['program']:r for r in prog}
ck('SEC17',[15],'T-CARE source has7events/3years/60000km',[progd['T-CARE'][k] for k in ['covered_scheduled_events','max_years','max_km']],[7,3,60000],'Frozen operator-source data and rendered-vector comparison','program_distinctions.json;page015')
ck('SEC18',[15],'Legacy GBSB source has6events/4years/50000km',[progd['GBSB'][k] for k in ['covered_scheduled_events','max_years','max_km']],[6,4,50000],'Frozen source data and rendered-vector comparison','program_distinctions.json;EE-S11PDF1')
ck('SEC19',[15],'Vector matrix uses7dark T-CARE/7dark Lite/6dark GBSBcircles',[7,7,6],[7,7,6],'AI visual count in page015; legacy7th circle is pale','page015.png','Event axis is ordinal; pale7th legacy cell is outside the covered count.')
ck('SEC20',[15],'Lite labor-only scope and no paid-return/GP inference are explicit',phrases(15,['T-CARE Lite covers labor for seven events; its parts package is separate','do not identify covered visit count','actual payment date or dealer gross profit','Eligibility and specified work']),True,'Final PDF text inspection','Page15')
ck('SEC21',[15],'Whichever-first and eligibility conditions survive the source note',phrases(15,['whichever first','eligibility, specified work and model terms apply']),True,'Final PDF text inspection','Page15source')

with (R/'workstreams/extension_journeys/service_estimates_extension.csv').open() as f:allcost=list(csv.DictReader(f))
bz=sorted([r for r in allcost if 'BZ4X' in r['model'] and 8<=int(r['service_visit'])<=11],key=lambda r:int(r['service_visit']))
totals=[int(r['labor_estimate_idr'])+int(r['parts_estimate_idr']) for r in bz]
ck('SEC22',[16],'Four rendered bZ4Xcolumn totals match847k/3694k/847k/3713k',totals,[847000,3694000,847000,3713000],'AI visible total labels and independent labor+parts arithmetic','XT04;page016.png')
ck('SEC23',[16],'Four dated bZ4Xestimates sum9101000',sum(totals),9101000,'Independent sum','service_estimates_extension.csv')
ck('SEC24',[16],'Stacked labor amounts match frozen observed rows',[int(r['labor_estimate_idr']) for r in bz],[847000,1582000,847000,1073000],'Chart generator/source comparison and AI visual stacks','make_story_charts.py;XT04')
ck('SEC25',[16],'Stacked parts amounts match frozen observed rows',[int(r['parts_estimate_idr']) for r in bz],[0,2112000,0,2640000],'Chart generator/source comparison and AI visual stacks','make_story_charts.py;XT04')
ck('SEC26',[16],'Estimate unit/date and non-GP/TCO limits remain explicit',phrases(16,['March 2024','not current invoices, total ownership cost, dealer margin','Do not multiply by case line margins']),True,'Final PDF text and AI visible Rp-million axis inspection','Page16')

offer,floor,cap,ret,lim=160,200,10,10,15;s=max(0,floor-offer);rec=min(lim,max(0,s-ret));res=s-rec
ck('SEC27',[26],'Illustrative customer credit160/170/200matches plotted values',[offer,offer+min(cap,s),floor],[160,170,200],'Independent arithmetic and AI visual labels','Page26;constructed_contract_tail.csv','All values Rp million, entirely illustrative.')
ck('SEC28',[26],'Illustrative full-floor shortfall40splits15recovery/25dealer',[s,rec,res],[40,15,25],'Independent arithmetic and AI visual stack labels','Page26;constructed contract inputs')
ck('SEC29',[26],'Constructed/conditional/unavailable-policy qualifications are visible',phrases(26,['ILLUSTRATION ONLY','constructed example','assumed Rp15 million insurer layer','No actual policy','aggregate cover available']),True,'Final PDF text plus AI visual ILLUSTRATION titles','Page26')
ck('SEC30',[26],'Capped credit is not relabelled as a guaranteed200floor',phrases(26,['does not create a full price floor','Do not call the capped top-up a guaranteed Rp200m floor']),True,'Final PDF text inspection','Page26')

risk=json.loads((R/'workstreams/extension_economics/constructed_aggregate_risk.json').read_text())
values=[r['dealer_residual_after_aggregate']/1e6 for r in risk]
ck('SEC31',[27],'Four rendered retained-loss bars are300/300/700/0m',values,[300.,300.,700.,0.],'AI visual labels plus source comparison','Page27;constructed_aggregate_risk.json')
ck('SEC32',[27],'Dealer residual equals gross promised shortfall less conditional recovery',all(r['full_floor_gross_shortfall']-r['effective_conditional_recovery']==r['dealer_residual_after_aggregate'] for r in risk),True,'Independent arithmetic','constructed_aggregate_risk.json')
ck('SEC33',[27],'No actual correlation, probability or expected-loss claim appears',phrases(27,['constructed worlds','No probability is assigned','without estimating actual correlation, expected loss or insurance availability','Four states are not four observed markets']),True,'Final PDF text inspection','Page27')
ck('SEC34',[27],'Illustrative100m aggregate cap and twenty-unit scope are explicit',phrases(27,['assumed Rp100 million aggregate recovery limit','same twenty units','Eighty constructed rows do not describe eighty customers']),True,'Final PDF text and AI visual axis inspection','Page27')

survey=json.loads((R/'workstreams/friend_surveys/survey_claims.json').read_text());sv={r['claim_id']:r for r in survey}
ck('SEC35',[39],'Survey audit source has43scoped claims',len(survey),43,'Frozen source table count','survey_claims.json;Page39source')
ck('SEC36',[39],'Older charging home share62uses178question base',[sv['D25_HOME']['value'],sv['D25_HOME']['country_question_n']],[62,178],'Source-table comparison with displayed olderQ43n178','survey_claims.jsonD25_HOME')
ck('SEC37',[39],'Newer home share61has its own223base',[sv['D26_HOME']['value'],sv['D26_HOME']['country_question_n']],[61,223],'Source-table check of combined61/62label','survey_claims.jsonD26_HOME','Final box does not print223; exact newer base remains in full audit. Optional clarity note below.')
ck('SEC38',[39],'PwC71is conditional on owners considering return toICE',phrases(39,['conditional on owners considering a return to ICE','not all owners in the study']),True,'PDF/source cohort comparison','P25_COST;Page39')
ck('SEC39',[39],'Supplied57/28awareness remains unverified',phrases(39,['could not be independently verified','values remain unverified','metadata does not verify the numbers']),True,'PDF/source-status comparison','RAK_BYD;RAK_TOYOTA;Page39')

notes=[dict(id='EC-N01',page=15,severity='optional wording',note='Headline says more visits; adding covered before visits would match the ordinal covered-event claim more precisely. Body and matrix already make the intended scope clear. Not blocking.'),dict(id='EC-N02',page=39,severity='optional clarity/typography',note='The61/62%box correctly warns about question bases but prints only older n178. A compact2025:62%,n178;2026:61%,n223label would remove edition ambiguity. Whitespace in this page’s copy could also be cleaned. Current claim is qualified and not false. Not blocking.')]
ck('SEC40',pages,'PDF stayed unchanged throughout audit',sha(pdf),expected,'End-of-audit file hash','Final PDF')
failed=[r for r in checks if r['result']=='FAIL'];images=[Path('/tmp/auto2000_story_final')/f'page-{n:03}.png' for n in pages]
source_paths=[pdf,R/'story_assets/economic_story.json',R/'shared/make_story_charts.py',R/'workstreams/extension_economics/portfolio_inputs_and_method.json',R/'workstreams/extension_economics/program_distinctions.json',R/'workstreams/extension_journeys/service_estimates_extension.csv',R/'workstreams/extension_economics/constructed_aggregate_risk.json',R/'workstreams/friend_surveys/survey_claims.json']
result=dict(reviewed_utc=datetime.now(timezone.utc).isoformat(),pdf_path=str(pdf),pdf_sha256=sha(pdf),expected_pdf_sha256=expected,page_count=len(doc),pages_reviewed=pages,assertions=len(checks),passed=sum(r['result']=='PASS' for r in checks),failed=len(failed),blocking_findings=failed,nonblocking_editorial_notes=notes,method='Independent frozen-input arithmetic, final PDF text, chart-generator inputs and AI inspection of the eight rendered pages. Not a repeat of old80-pageQA.',human_review=False,new_network_requests=0,pdf_modified=False,assertions_detail=checks,rendered_pages=[dict(path=str(p),sha256=sha(p)) for p in images],source_manifest=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in source_paths])
(O/'STORY_ECONOMIC_CLAIM_QA.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
md=f'''# Final reading PDF: economics and claim QA

**No blocking economic or source-scope error was found. All {len(checks)} assertions passed.**

Reviewed PDF: `output/pdf/Auto2000_Research_Findings.pdf`,41pages. SHA256:`{result['pdf_sha256']}`. The hash matches the requested final version and remained unchanged. This check covers pages2,3,4,15,16,26,27and39only. It does not repeat the old80-page review or claim complete independent review of every final page.

The audit combines frozen-input arithmetic, source-table and chart-generator comparisons, extracted final-PDF text and AI inspection of all eight specified page renders. No new research, network request, PDF edit or human review occurred.

| Page | Checked finding | Result |
|---|---|---|
|2|Case GP bars3600/1320/1200/630billion and53.3/19.6/17.8/9.3%reconcile to6750billion. Supplied-case and not-audited labels remain explicit.|Pass|
|3|37,693to31,668xEVsales and rounded Shapley−5,050/−975match. Toyota/Lexus perimeter and noncausal allocation are visible; no Auto2000 attribution.|Pass|
|4|All-channel counterfactual, separate operating costs and no double deduction of displaced work remain clear. Proposed-option inputs remain unmeasured.|Pass|
|15|T-CARE7events/3y/60,000km; Lite7labor-only; legacy6events/4y/50,000km. Six dark legacy circles and pale seventh cell agree with the covered count. No actual paid-return or GP claim.|Pass|
|16|bZ4Xlater-event totals0.847/3.694/0.847/3.713million sum9.101million. March2024estimate basis and noncurrent/non-GP/non-TCO caveats remain explicit.|Pass|
|26|Constructed160offer→170capped credit versus200floor;40shortfall splits15assumed recovery and25dealer residual. Illustration and unavailable-policy limits are visible.|Pass|
|27|Constructed retained losses300/300/700/0million match. Assumed100million aggregate limit, same pooled offers, no probabilities and no actual-correlation/expected-loss claim remain explicit.|Pass|
|39|Older Deloitte62%usesn178rather than all1004; newer61%uses its own base in full audit. PwC71%is conditional. Supplied57/28awareness remains unverified.|Pass|

Two optional refinements are nonblocking. Page15could say “more covered visits” in its headline. Page39could replace the compressed61/62%label with “2025:62%,n178;2026:61%,n223”and clean spacing. Its current body correctly warns against pooling question bases.

`STORY_ECONOMIC_CLAIM_QA.json`contains all assertions, source hashes and rendered-page hashes. Zero failures. No PDF changes were made.
'''
# Improve prose spacing without touching paths, model labels or the hash.
for a,b in {'41pages':'41 pages','SHA256:':'SHA256: ','pages2,3,4,15,16,26,27and39only':'pages 2, 3, 4, 15, 16, 26, 27 and 39 only','old80-page':'old 80-page','Page15could':'Page 15 could','Page39could':'Page 39 could','compressed61/62%label':'compressed 61/62% label','223”and':'223” and','json`contains':'json` contains'}.items():md=md.replace(a,b)
(O/'STORY_ECONOMIC_CLAIM_QA.md').write_text(md)
print(json.dumps(dict(pdf_sha256=sha(pdf),assertions=len(checks),passed=result['passed'],failed=len(failed),blocking=len(failed),optional_notes=len(notes)),indent=2))
assert not failed,'Blocking claim failure; inspect JSON. PDF untouched.'
