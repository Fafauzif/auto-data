AUTO2000 X SOCIAL LISTENING: $10 INPUT PACK
Prepared 14 November 2026. Actor assumed: xquik/x-tweet-scraper.
This is a proposed collection design. No paid actor run or customer validation has occurred.

PURPOSE
Find decision mechanisms and counterexamples for the three current strategy prongs:
P1: first-time Auto2000 xEV purchases; P2: recover paid workshop jobs and resolve xEV ownership needs; P3: repeat Auto2000 xEV purchases.
Use both Toyota/Auto2000-specific evidence and the wider Indonesian-language market, with separate labels. Evidence from other brands can generate hypotheses, not establish Auto2000 performance.

START
1. Open the exact Actor and check the rate displayed for YOUR account. The current public listing says $0.00015 per delivered result plus platform usage. A historical issue describes a much higher free-tier rate; the current listing says all plans use the same rate. This pack is conditional on the displayed $0.00015 rate, not a promise of account billing.
2. Paste inputs/00_pilot.json into the Actor JSON input tab. For the first pilot set the Console Maximum total charge to $0.20; this is a RUN setting, not a key in actor input JSON. Keep a timeout (for example 180 seconds for this pilot) and inspect the actual total usage afterward. Separate platform consumption may need additional monitoring.
3. Inspect at least 20 posts per returned query where available, including low-engagement posts. Across the pilot inspect about 200 posts. Check irrelevant homonyms, seller spam, media articles, mixed-language omissions, dates, replies missing their parents, and whether a post reports a real decision. Keep complaints and successful outcomes. Label promotions/media separately rather than deleting all links or all positive comments.
4. Proposed practical go/no-go: refine a query if fewer than roughly half the inspected posts are about its intended decision. This is a working screening threshold, not a statistical validity test. Low personal-experience yield may justify narrower action terms even when topic relevance is high.
5. Run core files sequentially in order 02, 01, 03, 04 after the pilot. Aftersales has the largest quota because it covers paid petrol work, hybrid/BEV/PHEV support, and matched competitive support. Each JSON is a separate run. Do not paste budget_plan.json or query_manifest.csv into the Actor.
6. Suggested event-charge caps in Console: 02=$2.70, 01=$1.80, 03=$1.50, 04=$0.60. Pilot actual event fees are at most $0.15 at the assumed price; the $0.20 Console pilot ceiling allows a small discrepancy. Track actual spend, not the sum of nominal caps alone.
7. Stop or reduce a later run if actual total account consumption plus its conservative expected cost would exceed $10. The $2.50 reserve is not a guaranteed platform-price quote. If the displayed result price differs, recompute row ceilings before proceeding: floor(available event budget / displayed price).

BUDGET
Pilot: 1,000 rows / $0.15 event fees.
P1: 12,000 rows / $1.80.
P2: 18,000 rows / $2.70.
P3: 10,000 rows / $1.50.
Shared digital handoff: 4,000 rows / $0.60.
Adaptive follow-up: up to 5,000 rows / $0.75 combined.
Maximum planned total: 50,000 delivered rows / $7.50 event fees.
Reserve: $2.50 for platform usage, overlap, retries or unanticipated consumption. Any retries must fit the same cumulative budget; do not add 50,000 new rows after a pilot or follow-up.
These are delivered-row ceilings, not forecasts. Cross-run overlap will reduce the number of unique posts. Sparse queries can return far less than their quotas. Do not manufacture volume by loosening relevance without recording the design change.

SAMPLING AND COVERAGE
The four core files contain 192 dated searches: 48 P1, 72 P2, 40 P3 and 32 shared. Each theme is split into four nonoverlapping windows, avoiding a single newest-first search that spends the whole quota on recent posts.
Windows: 2025-01-01 to 2025-07-01; 2025-07-01 to 2026-01-01; 2026-01-01 to 2026-07-01; 2026-07-01 to 2026-11-14. Since is inclusive and until exclusive; date-only searches use UTC. The collection stops before 14 November 2026 00:00 UTC, equivalent to 07:00 WIB on 14 November. Report 2025 and 2026 separately when product offers or app versions changed. Window lengths are unequal; quotas cannot be used to compare posting rates.
Latest is used for the main collection. Each search is bounded at 250 rows (125 for shared). A capped search is still a censored slice, not the full population of matches. If a query hits its cap, split that query into smaller nonoverlapping date ranges using an unspent portion of its original quota or the follow-up budget. Date splitting does not establish complete X coverage.
No minimum engagement, follower or verified-account filter. Replies and quote posts remain eligible. Native reposts are excluded to limit repeated amplification. Do not infer nationality from lang:id or profile language. Avoid geo restrictions during initial discovery; code explicitly stated branch/city afterward.
Do not exclude broad words such as promo, diskon, jual, link or kredit at collection: they can also occur in genuine customer narratives. Classify commercial accounts and near-duplicate scripts after export.
The searches intentionally contain some overlapping concepts. Retain multiple analytical tags for one post; never add prong counts as if they were independent people or revenue pools.

ADAPTIVE FOLLOW-UP, TOTAL LIMIT 5,000 ROWS
Templates require replacements and are NOT ready to execute as-is.
05a: select up to 20 genuine decision/service thread roots across all prongs, not only viral complaints. Insert real root post IDs, collect up to 100 direct replies per root, max 2,000. This mode does not guarantee nested conversation recovery. If nested context is essential, use the documented conversationIds/search route within the same budget. Keep all languages in reply collection and screen relevance afterward.
05b: choose up to four validated topical queries, remove lang:id, retain dates and non-repost filter, and retrieve up to 250 each / 1,000 total. This probes Indonesian/English code-switching and language classification omissions; manually screen geography and relevance.
05c: use Top only for selected thin or contrasting themes, up to eight queries x 250 / 2,000 total. Label this a separate discovery supplement. Do not merge it into a denominator as if it had the same selection process as Latest. If not useful, reallocate within the 5,000-row total and document the change.
Missing parents can be looked up with tweetIds, also within the same adaptive allowance. Do not scrape an owner's entire history merely to guess purchase history.

ANALYSIS
Export JSON with nested structure preserved, plus optional CSV for reading. Save each submitted input and run ID, collection time, actual total cost, delivered rows, status, diagnostics and run-report if present. Keep query_manifest.csv as the requested-search record; do not assume every output row includes its exact matching query. Record any available query provenance and retain multiple matches where possible.
Exclude diagnostic/non-post records. Deduplicate globally by post ID, keeping source-run membership. Keep repeated author posts for context, but report unique authors and conversations alongside post counts. Separate near-duplicate dealer templates from individual experiences. Native amplification counts are not counts of independent experiences.
Use coding_codebook.csv. Prior purchase at Auto2000 is explicit_prior_purchase, explicit_no_prior_purchase or unknown. A first-time EV buyer is not necessarily a first-time Auto2000 buyer. A Toyota owner is not necessarily an Auto2000 customer. Most public accounts may remain unknown on retailer history.
Distinguish an actual self-reported choice, hypothetical intent, advice, hearsay, official statements and promotions. For every useful account reconstruct: trigger, options, constraint/enabler, channel handoff, reported action, resolution and remaining uncertainty.
Code model/powertrain/variant, job and payer. Do not compare Chery ICE routine service with Toyota BEV battery diagnosis as if their work were equivalent. A covered service with zero customer cash is not evidence of zero dealer reimbursement, and customer bills do not establish gross profit.
Use AI labels only as a first pass. Check all quotations and decision-critical examples against full text plus thread context; inspect both supporting and conflicting cases. If a human second coder is available, independently review a stratified subset and document disagreements. AI-to-AI agreement is not human reliability evidence.

DECISION OUTPUTS
P1: compare price/credit/stock/demo constraints with fit/comprehension constraints. A showroom feature is useful only if the latter actually explains stalled next steps; collect positive and negative cases.
P2: distinguish owners who prefer independent workshops for price/trust from those who need certainty of scope, authorization, timing, parts or competence. Identify the actual paid job and conditions for switching, plus high-stakes xEV cases that mainly create trust rather than immediate GP.
P3: distinguish low trade-in value or affordability from confusing upgrade economics or missing credible condition evidence. Track self-reported retain/sell/trade/upgrade decisions and unknown prior retailer history.
Shared: identify request versus confirmation versus attendance versus completion, and the actor controlling each handoff. App mentions alone do not establish app-to-branch success or failure.
Produce a mechanism matrix with supporting accounts, counterexamples, evidence strength, testable solution implication and the field evidence still needed. Report frequencies only within a clearly defined retrieved-and-coded corpus. Equal topic quotas and overlapping queries prevent interpreting raw theme counts as market prevalence or brand market share.
Use this as qualitative discovery and fieldwork design. X accounts and posts are selective public expressions, not a representative sample of Indonesian buyers or verified offline transaction records. The 2024 Scientific Reports paper in sources.json discusses Twitter sampling bias in a different substantive domain; it supports this methodological caution, not any Indonesian automotive conclusion.
No causal conversion lift, switching rate, app retention, willingness-to-pay estimate or incremental GP can be established from these posts alone. Validate candidate mechanisms with matched quotes, recruited buyer/owner journeys and a credible branch pilot.

PRIVACY
Keep raw handles, vehicle details and contact information private. Do not contact posters without separate authorization. Pseudonymize excerpts for external reporting, minimize identifying details, and keep private source links only for the review trail.

VALIDATION STATUS
JSON syntax, expected fields/enums, date ranges, target quotas and arithmetic checked locally against the retrieved public schema. No actor execution, live query parsing, result completeness or account-specific charge has been tested.
