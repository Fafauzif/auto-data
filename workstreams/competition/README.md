# Competition and stakeholder evidence workstream

45 structured observations, 26 used source URLs across 11 core ecosystems plus provisional MG; 27 sources in catalog including one additionally inspected source. The source URL count and observation count differ because multiple observations can share a source. No observation is a customer count, representative prevalence estimate or measured effect.

Start with `analysis.md`; inspect `evidence_matrix.csv` or `.json` for every claim and limitation. `sources.json` has exact source URLs and retrieval method, including search-index-only evidence. `direct_verification.json` contains22successful HTTP source responses after robots checks, but two Nasmoco responses have no extracted words. Other stopped domains and web-tool failures are documented. Raw bodies are in the shared private cache, not this public folder.

`source_term_checks.json` contains53targeted raw-text substring checks:52found; the remaining SEVA partner label appears in an image alt attribute, separately checked. These are content checks, not rendered/browser or customer tests. A transport200 does not establish live function.

`normalized_programmes.csv/json` contains12derived programme rows with model, type, year/km, owner/use restrictions, paid retail extension and date scope. These reuse existing source evidence and must not be counted as new independent observations. Historical or index-only benefits are labeled.

`option_cards.json/csv/md` contains25candidate directions for user assessment. Each resolves actual evidence IDs and gives a benefit hypothesis, rival, existing analogue, transfer limit, stakeholder tension, economic dependency and kill condition. The Auto2000 gap is explicitly unestablished by this competitor workstream. No winner, roadmap or implementation is supplied. Link these cards to root Auto2000 and customer evidence before any final recommendation exercise.

Reproduction: `build_evidence.py` recreates the curated source/observation table from reviewed evidence; it is not a scraper. `verify_sources.py` uses the shared public transport and source catalog, then `enrich_verification.py` attaches direct-request provenance. `normalize_programmes.py` and `build_option_cards.py` recreate the derived comparison and analytical cards. Term QA reads shared private cached bodies and does not fetch more pages. Raw source extraction and scholarly rights limits prevent publishing entire page bodies; locators, hashes and concise original paraphrases are retained.

English; research date11November2026. No direct Auto2000 crawl from this agent. No forms, OTP requests, messages, login, account session or purchase.
