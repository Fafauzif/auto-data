# App-store evidence workstream

Research run: 11 November 2026. Public pages only. This workstream contains 210 deduplicated original review records as derived, anonymized data, drawn from six automotive apps and 12 app/platform/locale cohorts. They are a convenience sample selected by the stores' public-page interfaces, not a review census or representative sample. No account, key, payment, private session, blocked endpoint, review submission or customer interaction was used.

## Files

- `reviews_derived.csv`: 210 records, stable REV evidence IDs, review IDs, dates, versions where present, ratings, pseudonyms, source URLs, lexical mention flags and AI experience classifications. No raw review text, author handles, phone numbers, images, contact information or developer reply text is included.
- `manual_audit.csv`: all 210 records source-inspected and coded by an AI researcher, with short English paraphrase codes. One AI researcher coded210 records; a second AI checked30 targeted records. No human validation or human inter-rater reliability.
- `listing_metadata.json`: extracted app-level metadata for six available Google Play listings. SEVA failed live retrieval. Store ratings/counts are contextual snapshots; do not rank apps from these aggregates.
- `review_summary.json`: sample distributions by app/platform; this is not population prevalence.
- `manual_audit_summary.json`: within-sample experience types, not verified customer outcomes.
- `collection_log.json`: fetched public page URLs, HTTP statuses and shared transport request IDs. Shared cached-response provenance is retained in the root transport SQLite log.
- `play.google.com_robots.txt`, `itunes.apple.com_robots.txt`, `apps.apple.com_robots.txt`: actual retrieved robots evidence.
- `mention_rules.json`: deterministic lexical mention rules. Mentions are neither validated complaints nor sentiment.
- `collect_public_listings.py`, `analyze_reviews.py`, `manual_audit.py`: collection and derivation scripts, with frozen AI coding keyed to stable review IDs. Raw HTML, full source text, parsing objects, installation dependencies and pseudonymization salt remain in root `private_cache/reviews`, outside the public deliverable.
- `FINDINGS.md`: bounded findings, rival explanations and candidate implications.

## Method and access

The Google Play robots file disallows `/_` and `/store/getreviews`. The inspected google-play-scraper 1.2.7 review pager calls `/_/PlayStoreUi/data/batchexecute`; that route was never requested. The installed library was used only to parse allowed public details HTML. Its comment-array location had drifted from ds:8 to ds:10 in the retrieved pages, so initial empty parser output was corrected locally, never treated as zero reviews. Current details HTML contained20 embedded review objects per available app/language page.

Apple's itunes.apple.com robots disallows country RSS paths, so RSS feeds were not requested. Allowed apps.apple.com public `?see-all=reviews` pages yielded ten embedded records for each of Digiroom, mToyota and BYD AUTO. Public source state supplied no continuation marker in this collection; no hidden pagination or authenticated endpoint was forced. Indonesia storefront/language is not proof of reviewer residence.

App identities were verified against public Google Play and Apple listings. SEVA `id.seva` / Apple 1589727482 appeared in search indexes but both requested live public listings returned404. This means unavailable on this retrieval surface; delisting, geography, temporary failures and URL changes remain possible. The failed requests are retained. No SEVA app experience was fabricated.

## Interpretation rules

`self_reported_app_job` means a reviewer reports a specific interaction, not investigator-observed usability or independently verified completion. `branch_experience` concerns a human/dealer episode. `product_review` concerns the car. `prospective_no_job` explicitly precedes relevant ownership or service use. `unknown` is generic praise, a request, promotional contact, ambiguous evidence or insufficient detail. A primary label simplifies overlap; use `paraphrase_code` and source before interpreting. All rows set independently_verified=false.

`pre_digiroom_relaunch` compares Digiroom review date with 6 December2025; it does not establish the installed build at posting. Android version fields may refer to review-created version; updates/edits and platform details remain uncertain. Apple page JSON did not expose review build. Review timestamps parsed from Google are UTC epoch conversions; source text may display localized dates. Dates and extraction time are distinct.

Rating counts/histograms, text-review counts and installation ranges have different definitions. Histograms may not sum exactly to displayed aggregate ratings; parser drift, source update timing and presentation precision are unresolved. Zero extraction failures are not zero complaints. Old featured reviews are not evidence of a current defect. No sentiment classifier, population inference, causal test, forecast or ROI estimate was run.

## Language-selection expansion

Three additional allowed public Google Play pages (Digiroom, mToyota and BYD AUTO) changed hl from id to en while retaining gl=ID. They each supplied20 additional reviewIDs, all distinct from the original150; final corpus210. Public summary stratifies locale as well as app/platform. This is not a geography comparison or another independent population sample. The different requested language coincided with different displayed review sets and date distributions. Unknown nationality/residence remains false for verified-residence fields. `locale_probe_log.json` records the source requests. No blocked pagination was used.

Independent checking here means a second AI checked30 targeted records (20original,10expanded). It was nonblind and not random; no human reviewer or inter-rater reliability estimate exists. `self_reported_app_job` never establishes job completion. Derived flags distinguish app-task-eligible records from product, branch, prospective, unknown and promotional records.

The two uncached BYD language rechecks returned identical within-language reviewID sets; no new customer records were added. This tests short-window extraction repeatability, not the platform selection mechanism or business impact. See `locale_recheck.json`.
