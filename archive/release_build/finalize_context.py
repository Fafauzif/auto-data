from pathlib import Path
import json,re,shutil,csv
R=Path(__file__).resolve().parent/'release_repo'
def put(p,t):
 f=R/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(t.strip()+'\n',encoding='utf-8')
refs=[]
for i,paths,typ in [
('C1',['sources/case/Semifinal_Casebook_IBSC_2026.pdf','analysis/research/original_casebook.txt','analysis/research/original_case_kpis.csv'],'original_case'),
('G1',['analysis/geography/tables/raw_independent_audit.json','analysis/geography/tables/raw_recomputed_markets.csv'],'recomputed_model'),
('G2',['analysis/geography/tables/branch_portfolio.csv','analysis/geography/tables/market_portfolio.csv','analysis/geography/tables/raw_branch_checks.csv'],'recomputed_model'),
('G3',['analysis/geography/geography_source_map.json','manifests/source_inventory.jsonl'],'original_source_map'),
('S1',['analysis/social/corpus_metrics.json','analysis/social/source_runs.csv','analysis/social/record_run_membership.csv'],'cleaning_metadata'),
('S2',['analysis/social/curated_social_evidence.jsonl','analysis/social/cleaned/x.jsonl'],'selected_accounts'),
('S3',['analysis/social/youtube_video_summary.csv','analysis/social/youtube_analyst_annotations.jsonl'],'selected_video_comments')]:
 refs.append({'evidence_ref':i,'type':typ,'paths':paths})
for r in json.loads((R/'analysis/research/master_report_reference_crosswalk.json').read_text(encoding='utf-8')):
 refs.append({'evidence_ref':r['report_reference_id'],'type':'namespaced_prior_evidence','paths':['analysis/research/master_report_reference_crosswalk.json','analysis/research/legacy_evidence_union.jsonl'],'crosswalk_key':r['report_reference_id']})
for r in json.loads((R/'analysis/social/maps_deep/curated_maps_evidence.json').read_text(encoding='utf-8')):
 refs.append({'evidence_ref':r['evidence_id'],'type':'selected_maps_account','paths':['analysis/social/maps_deep/curated_maps_evidence.json'],'record_id':r['review_id'],'place_id':r['place_id']})
for l in (R/'analysis/social/curated_social_evidence.jsonl').read_text(encoding='utf-8').splitlines():
 r=json.loads(l);refs.append({'evidence_ref':r['evidence_id'],'type':'selected_'+r['platform']+'_account','paths':['analysis/social/curated_social_evidence.jsonl'],'record_id':r['record_id']})
# Source map filenames can differ only in capitalization; resolve actual generated artifact.
for r in refs:
 if r['evidence_ref']=='G3':r['paths']=['analysis/geography/GEOGRAPHY_INTEGRATION_REPORT.md','manifests/source_inventory.jsonl']
put('data/evidence_catalogue.json',json.dumps(refs,ensure_ascii=False,indent=2))
faq=[
('What is the current mandate?','Integrated private research, recommendations and complete continuation context across all available evidence families. Historical diagnosis-only instructions are superseded.',['PROJECT_CONTEXT.md','context/SESSION_DECISIONS.json']),
('Which three prongs must be answered?','New-to-Auto2000 xEV acquisition, eligible customer-paid aftersales recovery, repeat xEV replacement/trade-in.',['PROJECT_CONTEXT.md']),
('What does the original case require?','Digital innovation as the core driver, meaningful regular Digiroom use, xEV sales/aftersales GP, privacy, realistic assumptions and a roadmap within IDR150bn for2026–2028.',['analysis/research/original_case_kpis.csv','sources/case/Semifinal_Casebook_IBSC_2026.pdf']),
('Does the case EV definition include hybrids?','Yes. HEV, PHEV and BEV are included.',['analysis/research/original_casebook.txt']),
('How much X evidence exists?','14,892 rows and14,291 unique post IDs across10exports. This includes noise and promotional material.',['analysis/social/corpus_metrics.json','analysis/social/source_runs.csv']),
('What thread context is missing?','6,186Xreplies, of which5,704lackthe immediate parent in the supplied corpus.',['analysis/social/corpus_metrics.json']),
('What YouTube evidence actually returned?','74comments/replies on3videos:26M6owner-experience,3SetirKananM6 and45Netaresale. No Toyota video is returned.',['analysis/social/youtube_video_summary.csv']),
('How should Maps sampling be interpreted?','8,385rows become8,119IDs across37places. Lowest-ranking and newest selected cohorts overlap266IDs and must retain cohort membership.',['analysis/social/corpus_metrics.json','analysis/social/maps_branch_cohort_summary.csv']),
('Are these counts customers?','No. PlatformIDs, reviews, authors, modelorigins and telemetry values have different units and do not authenticate transactions.',['DATA_GUIDE.md']),
('Which geography version is current?','The corrected14Novemberlatest source package and independent audit; older Suci/Sidoarjo coordinates/headlines are historical.',['analysis/geography/GEOGRAPHY_INTEGRATION_REPORT.md','context/SUPERSESSION.md']),
('What is the main new geographic prioritization?','Owned eligible routing reduces oil tails39to20. Bandung has14of20remaining origins andSoekarno-Hatta8. These are model origins, not demand weights.',['analysis/geography/tables/market_portfolio.csv','analysis/geography/tables/branch_portfolio.csv']),
('Why preserve Pancing or TAA service despite oil alternatives?','Pancing0residualoil tails/8originslosing15minute generalbranch access underremoval;TAA0/7. General-workshop geometry differs from oil-job substitution.',['analysis/geography/tables/branch_portfolio.csv']),
('What happens to Sidoarjo zero baseline assignment?','Keep its separate correction/southern extension:6of6targeted added origins choose it. Zero baseline count is not zero demand.',['analysis/geography/GEOGRAPHY_INTEGRATION_REPORT.md']),
('Are app booking, HHC and trade-in new features?','Existing capability evidence is preserved. Differentiation must address usable acceptance, fulfillment and executable offers.',['analysis/research/master_report_reference_crosswalk.json']),
('Can all new2026sales be routine paid aftersales inside2028?','No. Entitlement, mileage, model/cohort and uncovered work determine payment. The month42illustration is conditional, not a BEV maintenance forecast.',['analysis/research/COMMERCIAL_MODEL_SPEC.md','reports/INTEGRATED_REPORT.md']),
('What does the case46.7%aftersalesGP mean?','It is the aggregate all-powertrain GP share, paired with13.0%revenue share. It is not an xEV margin.',['analysis/research/case_business_line_inputs.csv']),
('What is the primary digital proposition?','A customer-visible ownership case linking vehicle, job, entitlement, suitable destination, accepted scope and completed outcome across channels, with xEV demo and net-upgrade paths.',['reports/INTEGRATED_REPORT.md']),
('How is channel migration handled?','A programme-linked transaction is not necessarily incremental. Model counterfactual completed work, recognized GP, costs and displacement; set displacement deduction tozeroifalreadyin the counterfactual.',['analysis/research/COMMERCIAL_MODEL_SPEC.md','reports/INTEGRATED_REPORT.md']),
('Where are all original sources and scraping inputs?','The source inventory resolves logical paths and byte-identical aliases across original repo, session uploads/workproducts and geography archive members.',['manifests/source_inventory.jsonl','sources/ARCHIVE_GUIDE.md']),
('Can large files be restored exactly?','Yes. Original byte parts carry length/hash metadata and source_archive.py reconstructs to ignored.restored. Do not commit oversized restored originals.',['scripts/source_archive.py','MIGRATION.md']),
('Does Replace All remove obsolete files?','No. Use the migration dryrun/applyworkflow to move unmodified obsolete sources to a siblingbackup while protecting changed/unknownfiles and.git.',['MIGRATION.md','scripts/migrate_legacy.py']),
('What is the source-container vault for?','Optional exact original ZIP bytes. The primary repo already retains source-member content.',['sources/ARCHIVE_GUIDE.md']),
('Was anything spent or published?','No paid actor, lead, booking, message or GitHub push was performed in this integratedanalysis.',['context/SESSION_DECISIONS.json','context/ACQUISITION_HISTORY.md']),
('Can the chat now be closed?','The repo preserves current mandate, decisions, sourcecontext, status, findings and nextresearchdecisions. It is a faithful reconstructedhandoff with originals, not an unavailable completeverbatim chat export.',['PROJECT_CONTEXT.md','context/SESSION_TIMELINE.csv'])]
put('context/CONTINUATION_FAQ.json',json.dumps([{'question':q,'answer':a,'paths':p} for q,a,p in faq],ensure_ascii=False,indent=2))
put('context/USER_AUTHORIZATION.md','''# Current user authorization

The user explicitly corrected scope to include everything, particularly X and YouTube as well as Google Maps, and required enough context in the repo to close the originating chat.

The user answered the planning questions as follows, preserving the original wording:

> 1. yes, will be private. i agree
> 2. english, tkes sumber ttp bahasa asli
> 3. can rapihkan
>
> Ok take your time, analyze everything, make unique insights, bla bla bla. take your time. go all out

The immediately preceding approved plan covered source inventory, cleaning, all three prongs, integrated geography, commercial scenarios, English reports, AI-readable context, immutable source preservation, a private source-container companion and a one-time migration. Individual tracked files have a90,000,000byte build ceiling to remain below the user's100MBlimit.

This authorization permits research execution and packaging. It does not authorize paid actor runs, external messaging, live customer submissions or a GitHub push. Earlier requests to prepare scraping JSONs are retained in the source archive as collection history.
''')
# Friendly UTF8 English spacing in newly authored root prose, preserving links/identifiers/code.
for path in [R/'README.md',R/'READ_FIRST.md',R/'DATA_GUIDE.md',R/'REPOSITORY_MAP.md',R/'PROJECT_CONTEXT.md',*(R/'context').glob('*.md'),R/'reports/EXECUTIVE_FINDINGS.md']:
 t=path.read_text(encoding='utf-8');t=re.sub(r'\b(is|of|to|in|at|by|as)(?=\d)',r'\1 ',t)
 t=re.sub(r'(?<=[A-Za-z%]),(?=\d)',', ',t);t=re.sub(r':(?=\d)',': ',t)
 path.write_text(t,encoding='utf-8')
# Preserve reproducibility output and current mandate independently of ignored temporary reruns.
receipt=R/'.restored/rerun/RERUN_RECEIPT.json'
if receipt.exists():shutil.copy2(receipt,R/'qa/OFFLINE_REPRODUCTION.json')
status={'release_date':'2026-11-14','state':'analysis_complete_release_QA_in_progress','analysis_cutoff':'2026-11-14','private':True,'sources_preserved':2656,'social_source_rows':23351,'social_platform_ids':22484,'source_count_is_not_independent_evidence':True,'three_prongs_included':True,'digital_core_case_requirements_included':True,'paid_collection_run':False,'github_pushed':False,'next_read':['reports/EXECUTIVE_FINDINGS.md','reports/INTEGRATED_REPORT.md','context/NEXT_RESEARCH_DECISIONS.md'],'context_type':'reconstructed_decision_handoff_with_available_original_sources'}
put('context/CURRENT_STATUS.json',json.dumps(status,indent=2))
print('continuation context and evidence catalogue created',len(refs),'refs',len(faq),'FAQs')
