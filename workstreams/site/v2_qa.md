# Independent cached-source QA of extraction version2

Snapshot: 11 November2026,03:09:30UTC. A separate AI researcher checked the same fixed24 successful source responses used in the earlier v1 review, covering15 template families. No network request, browser rendering, human reviewer or participant test occurred. The production SQLite database was opened read-only within a snapshot transaction; no source rows, collector code or production exports were modified by this check.

## Outcome

The v2 numerical fields reproduced correctly for all24 selected responses, and the earlier nav-link, promotion-amount and WhatsApp-path corrections were visible. However, **two semantic boundary failures remain**: the generic article fallback selected an empty video-embed element instead of a populated inner main container. The two stored zero-word results are extraction artifacts, not evidence of empty page content, absent product information or duplicate content. Correct the fallback and reparse affected cached pages before using their topic, amount, link or similarity outputs.

## Fixed-source checks

| Check | Result within this fixed sample | Scope |
|---|---:|---|
| Pages recorded as extraction2.0 |24/24|Time-specific snapshot; crawl continued.|
| Selected selector matches current v2 code |24/24|Reproducibility, not semantic adequacy.|
| Word counts and content hashes match recomputation |24/24|Same parser family and extraction specification.|
| Main-link target sets match cleaned-container rule |24/24|Navigation/header/footer links excluded; not task completion.|
| Title20-word cap, exact-rel canonical, globalH1 and form counts match |24/24|Structural initialHTML values only.|
| Numeric-Rp flag matches selected text |24/24|A mention flag, not a verified offer or worked cost example.|
| Capture timestamp matches original transport request |24/24|Cached reparse did not falsely refresh capture time.|
| WhatsApp phone-number paths in stored link export |0/24pages|Sanitization test on these24sources; not whole-release PII certification.|
| Editorial pages with outer-main numericRp but none in article prose |4|Correctly excluded from selected-article numeric flag; old promotion contamination resolved for these sources.|
| Empty media-article chosen over populated inner main |2/24|Blocking semantic fallback issue detailed below.|

All denominators are reviewed-source counts. They do not estimate site-wide defect prevalence, customer outcomes, search-engine indexing or revenue effects.

## Remaining selector issue

| Source | V2 stored selection | Independent source-structure observation | Consequence |
|---|---|---|---|
| QA-01, adviser profile reached by promotionURL redirect |`article`,0words|The first article is `<article class="yt-lite" data-title="video">` with only a play button. Inner main contains725words, the adviser heading, offers and other substantive modules.|Source body is not empty. Generic mediaarticle must not override a populated main.|
| QA-13, Toyota bZ4X product video page |`article`,0words|The first article is a `yt-lite` video wrapper. Inner main contains347words, the product heading, descriptive information, price representation and CTAs.|Do not equate a video wrapper's zero text with zero page substance or feature absence.|

Recommended selector rule: use identified editorial prose first; otherwise use the populated inner main, with any article fallback restricted to a substantive article body and excluding media wrappers such as `yt-lite`. If a genuinely media-only page has no textual substance, record that as a modality/measurement boundary; do not group all empty hashes as duplicate editorial content.

The source content was inspected directly from the existing body captures; no video was downloaded or watched. Source URLs, requestIDs and hashes are in `v2_qa.csv` and `v2_semantic_checks.csv`. Those tables preserve the actual pre-correction snapshot. The main word-count reference is a structural counterexample, not an assertion that every inner-main word is unique editorial information.

## Remaining interpretation constraints

Product subnavigation and page CTAs remain in selected inner-main text by design. That can be appropriate for a job/capability inventory, but word counts and similarity remain selected-container measures, not pure article substance. Raw canonical absence is not an indexing failure. GlobalH1, forms and image-alt flags may include template or hidden elements and cannot certify accessibility.

The earlier decimal-currency normalization concern remains a code-level limitation: removing punctuation can misread a decimal-formatted amount. No such decimal match was observed in these24sources; this check does not validate prices, reconcile variants, location or current terms, or establish an economic cost example. Selected amounts must remain unverified mentions unless separately reconciled.

This QA found no new source-date or canonical mismatch in its fixed sample. Repeated extraction passes and corrected records are not new independent source observations. The root agent received the fallback finding while collection was active. Version2 is not release-approved; its stored values must be superseded by the planned v3 cached reparse. A later correction requires its own versioned cached-source recheck; this document does not claim it has already passed.
