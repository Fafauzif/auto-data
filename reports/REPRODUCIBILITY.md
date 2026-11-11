# Reproducibility and implementation boundaries

This is an evidence project with preserved source versions, derived tables, AI-written annotations, analysis scripts and acquisition recipes. It is **not a tested one-command installer that recreates the entire live-web research run on any computer**. Separate three activities: reproducing calculations from included source data; regenerating views of already curated evidence; and reacquiring changing public sources. The first two are substantially supported. The third depends on current access, markup, source rules and capture retention.

All source inspection, annotation and crosschecking in this run was performed by AI research agents. No human validation, participant usability experiment, representative survey, or verified customer transaction was conducted by this project. Upstream published datasets/studies retain their own methods and limits.


## Final extraction checkpoint

The recorded production comparison now passes: `workstreams/site/v3_qa_reference_summary.json` has production_v3_verified=true, with all24fixed cached sources matching version3.0, selector, words, contenthash, mainlinktargets, selected numericflag, canonical, globalH1/forms, cappedtitle, originalcapturetime and requestID. The separate final read-only database check finds281successful error-free source responses and all281carry version3.0; the complete saved queue has345requestedURL records. The24reference cases are a deliberate subset of those sources, not24new observations or a claim that every page was individually inspected. No new network or human validation was involved.

The public release remains reproducible at different levels: included licensed raw CSVs support exact source-byte checking and deterministic recalculations; preserved factual tables and AI annotations support rebuilding their summaries; historical live-source HTML/review text that is not redistributed cannot be reconstructed from hashes alone. No full one-click or complete public-archive-only replay claim is made.

## Runtime and installation

The run used Python3.12 in the provided Linux runtime. The observed package versions are recorded in `requirements-analysis.txt`, `requirements-collection.txt` and optional `requirements-documents.txt`, next to this document. They are minimal observed direct dependencies, not a complete OS/container/transitive lock or a clean-install guarantee.

| Layer | Direct requirements | Role |
|---|---|---|
| Numeric analysis |numpy2.3.5, pandas2.2.3|Dataset reconciliation, descriptive tables and geographic scenarios.|
| Original figures |matplotlib3.10.8|Headless Agg rendering; exact pixels can vary with fonts/platform.|
| Auxiliary NLP baseline |scikit-learn1.8.0|IndoNLU CASA calibration, not current Digiroom ground truth.|
| HTML parsing |beautifulsoup4 4.15.0, lxml6.1.1|Initial-HTML extraction and cached-source QA.|
| Play public-page parsing |google-play-scraper1.2.7|Parsing the allowed public listing HTML only; not the prohibited pagination endpoint.|
| Optional document builders/checks |python-docx1.2.0, PyMuPDF1.26.6|DOCX creation and private-PDF arithmetic checks; original supplied casebook is not publicly redistributed.|
| Host commands |curl; optionally pdftotext from Poppler|Verified-TLS HTTP acquisition; extraction of permitted public PDF evidence into private cache.|
| Standard library |sqlite3, csv, json, hashlib, urllib, zipfile, pathlib and others|No extra pip packages for those modules.|

No paid SDK, browser-session import, proxy service, API key, new account, Node build, hosted database or GPU is required for the supported offline analyses. Missing data or blocked endpoints must remain missing; installing a scraper does not grant platform access.

Example Linux/macOS setup from the extracted project root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r reports/requirements-analysis.txt
python -m pip install -r reports/requirements-collection.txt
```

Use an isolated environment. On Windows, activate its corresponding virtual environment and install curl/Poppler equivalents when using acquisition recipes. The source run did not validate a fresh Windows installation. A no-network offline environment can inspect the CSV/JSON reports without installing acquisition dependencies.

## Supported calculation and reporting map

Run commands from the extracted project root. These commands write generated outputs, so preserve an immutable original release copy if comparing hashes. None of the offline commands below should launch a web collector.

| Purpose | Command | Required inputs and boundary |
|---|---|---|
| Check included raw source files |`python workstreams/release_methods/check_raw_manifest.py`|Uses `raw_licensed_data/DATASET_SOURCE_MANIFEST.json`; checks bytes, hashes and CSV widths, not factual truth or privacy completeness.|
| Stage licensed raw analysis inputs |`python workstreams/release_methods/stage_licensed_inputs.py`|Copies/reuses four already included source CSVs into private_cache/datasets after hash verification. No download. `--dry-run` reports intended staging.|
| Recompute IGAR label comparison |`python workstreams/datasets/igar_analyze.py`|Requires staged Rating_labeled.csv and VADER_labeled.csv; exact source version/count asserted. Performs a six-field-key join with duplicate ordinals. Two views of the same records are not additional reviews.|
| Recompute SPKLU descriptive/geographic context |`python workstreams/datasets/spklu_analyze.py`|Requires staged station/charger files and included `workstreams/datasets/bps_vehicle_stock_long.csv`. Its all-pairs distances are derived comparisons, not new stations or driving times.|
| Recompute branch-coordinate sensitivity |`python workstreams/datasets/geo_sensitivity.py`|Requires preceding charging outputs plus included `site_branch_identity_probe.json`. Uses preserved official-direction candidates; it is a sensitivity scenario, not field verification.|
| Rebuild dataset figures |`python workstreams/datasets/dataset_figures.py`|Uses the derived IGAR/province CSVs; no new source retrieval.|
| Rebuild three synthesis figures |`python shared/make_figures.py`|Uses the included source-transcribed service-survey cells, observed finance scenarios and five-branch crosscheck. It does not rerun a survey or simulator.|
| Rebuild site summary views |`python shared/site_analyze.py`|Requires packaged `data/site_evidence.sqlite`. Use only after final v3 cached reparse/version checks. This exports structure/flags, not search rankings, task success or reconciled prices.|
| Rebuild option review table |`python reports/build_option_review.py`|Requires included competition/market option and evidenceJSON. Reproduces the saved AI-written concept-disposition mapping; it does not independently rediscover or validate the strategy.|

Pandas joins over the large IGAR files and all-pairs geographic computation can use substantial RAM. The included derived tables allow inspection without rerunning those calculations. This review did not establish a universal minimum memory/runtime requirement.

## Acquisition recipes and conditional re-execution

The source registry/provenance logs should be consulted before any new network run. Recheck source rules, use the shared request budget, preserve errors and stop on confirmed restrictions. `shared/public_http.py` centralizes cache, domain concurrency, timing and request logs; it does **not itself decide every source's robots or reuse policy**. Adapters must apply the documented source-specific checks. A successful HTTP response is not proof of access rights, current usability or commercial outcome.

The v3 site collector is the supported extraction specification. Versions1 and2 remain as historical code explaining corrections; their numbers must not be presented as final v3 results. The source inventory came from the earlier release, so it is inherited discovery rather than another8436new observations. The root corrected the supported v3 collector to use the packaged `data/sitemap_urls.csv`. Historical v1/v2 collectors retain the old outside-workspace reference and should not be used as the supported pipeline. No hidden sibling sitemap cache should be assumed present on a new computer.

The relevant acquisition command is `python shared/site_collect_v3.py --limit 1200`, conditional on the packaged inventory and current source access. A later `--reparse` operates on successful records but relies on raw private body cache. It is not an offline guarantee if those bodies are absent: `collect()` calls shared fetch, which can make a new request on a cache miss. Therefore **never run --reparse on a fresh public-only archive expecting zero network**. The root also supplied `python shared/reparse_offline.py`, which replaces fetch with a cache-only function and raises on a missing body rather than using the network. This safer command still needs the private source cache; it cannot reconstruct omitted captures from the public archive. The root run retained original request timestamps.

The reviews acquisition sequence is:

```bash
python workstreams/reviews/collect_public_listings.py
python workstreams/reviews/probe_locale_selection.py
```

Those scripts retrieve the allowed public listing pages, not the disallowed Play batchexecute/review pager or Apple RSS paths. The adaptive parser checks review-record shape rather than assuming a callback-number location; nine cached captures yielded the expected180embedded Google objects during its bounded check. New public pages may select different records or expose changed markup. Empty extraction receives an explicit warning rather than proving zero reviews.

`analyze_reviews.py`, `manual_audit.py`, `build_review_source_metadata.py` and cached-source QA need their respective private source objects, salts or transport cache. The public archive deliberately omits full unlicensed app-review text/HTML and reviewer identities. Those scripts are complete recorded derivation recipes, **not fully reproducible from the public derivedCSV alone**. The public210record IDs,12source locators/capturehashes and original timestamps preserve what was analyzed, but do not guarantee that a changing source later returns the same text. The locale-probe script now automatically writes the unique English-locale supplement by comparing platformreviewIDs against the primary Google records; its intermediate `locale_unique_extra.json` remains private. The revised supplement logic reproduced the current60additional IDs from existing cached records without new network requests. The frozen AI labels are keyed to reviewIDs; unknown new records remain unaudited rather than inheriting old positional labels.

The optional `recheck_locale_selection.py` repeats two permitted BYD listing requests with cache disabled. Its two responses added zero independent customer records and support only short-window within-language repeatability.

Mendeley/BPS acquisition scripts are also recorded staged recipes. For example, `igar_collect.py` expects a prior file-list metadata object, `spklu_collect.py` expects prior folder metadata, and `bps_collect.py` expects the privately cached2024page while fetching other years. The included raw Mendeley CSVs and extracted BPS factual table objects avoid assuming these private prerequisites when reproducing downstream calculations. The source download URLs, versions and hashes are recorded; no public rawHTML or private account is supplied.

## TLS and library side effects

Source inspection found that google-play-scraper1.2.7 changes Python's global default SSL context to an unverified context on import. The three supplied Play-parser scripts immediately restore the secure standard context after importing it. Actual HTTP retrieval in those scripts uses shared curl with normal TLS verification; no `-k`/`--insecure` flag or library review-network function is invoked. This observation does not certify upstream package security or make its unmodified network clients appropriate. Keep the parser dependency isolated and do not substitute its unrestricted pagination helper.

## Portability and curated knowledge

The static code snapshot at03:28UTC had72Python scripts with valid syntax; later additions need the same final snapshot check. Several historical market, narrative and friend-context acquisition/assessment recipes contained absolute workspace imports or paths. `workstreams/release_methods/SCRIPT_INVENTORY_QA.json` identifies their file/line locations without reproducing credential values. Those input/import recipes need relative-root adaptation before use outside this workspace; they are not part of a tested portable one-click pipeline. A flagged ROOT.parent archive output path is merely an output destination, not a missing input. The numerical QA also requires the supplied private casebook PDF outside the public archive; its other arithmetic checks and logs remain inspectable, but the complete original run requires that private input. No secret strings were published by this inspection. For a DOCX rebuild, install optional document requirements and run the corresponding builder against included Markdown/JSON; rendering/visual QA additionally needs an available office/PDF rendering environment and was not packaged as a universal installer.

Some builders embed source-grounded AI annotations, transcribed factual cells and concept mappings directly. Rerunning them reproduces those saved interpretations; it does not repeat an independent human review. Fields or comments saying manual/visual transcription refer to AI source inspection in this project unless an upstream study explicitly says otherwise. Keep upstream human-labeled training data separate from this project's AI annotation claims.

## Release content and counting

Exclude private_cache, dependency directories, bytecode/__pycache__, browser profiles, cookies, credentials, user-uploaded private casebooks/PDFs and full unlicensed review bodies from the public backup. At this inspection, no private uploaded PDF/screenshot or installed dependency bundle appeared outside private_cache. The PNGs found outside it were generated analytical figures. Previous archive listings contained the prior generated planDOCX and researchZIPs, with no user private casebook discovered by that path/type check; nested releases are historical copies, not fresh source observations. A path/type check is not a complete content/PII certification.

Raw licensed data has different source terms by folder. IGAR's two original label views, its derived feature table, repeated source captures and annotations must not be summed as new independent customer experiences. SPKLU site/charger rows, dictionary rows, BPS numeric cells, link occurrences, geographic pairs and model features are different units. Keep those denominators explicit in the release count report.

The root release must verify the final archive checksum, actual included paths and final v3 version counts, then report real upload responses and expiry. Temporary backup documentation does not establish a successful backup; see `workstreams/release_methods/BACKUP_METHODS.md` for verified operator limits and untested/access-limited alternatives.


## Final reading edition and extension entry points

The primary readable PDF is generated by shared/make_story_charts.py followed by shared/build_story_pdf.py, using curated story_assets and reports/story_assets inputs. shared/render_story_qa.py renders internal inspection pages outside the archive. The older shared/build_findings_pdf.py is a dense technical-draft recipe and is not the selected reading layout; running it can overwrite the PDF, so preserve an unchanged release first. The complete analysis remains in the workstream reports.

The new battery analysis reads packaged MAT inputs using numpy, scipy, h5py, pandas and matplotlib; see workstreams/extension_battery/analyze.py and verify.py. Its own source manifest and 49-check receipt are separate from the earlier17-file staging receipt. Geometry robustness is supported offline by workstreams/extension_geography/robustness.py. The updated context is rebuilt by shared/build_master_context.py with --final-pdf pointing at the verified final PDF. Source reacquisition and older absolute-path recipes retain their previously stated limitations.
