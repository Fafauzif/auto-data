AUTO2000 PILOT ANALYSIS AND REVISED FOLLOW-UP
Prepared 14 November 2026. Repository commit 34498fe033ae4dcd1a52c8d2e039f870b00d08fe.

START HERE
The pilot is useful for decision discovery, but it is not a clean customer-only corpus. Do not launch the earlier broad bulk inputs unchanged. Use these narrower staged inputs instead. No paid run has been executed by this analysis.

1. Read FINDINGS.txt. Its source is the 434-post uploaded export plus the existing repository, with both kept separate.
2. Run 01_preflight/01_digiroom_external.json first; its exact JSON is ready to paste into xquik/x-tweet-scraper. The other five single-query preflights test different topics. Run 07_batch_control last to compare batching with the single-query path. The six singles are capped at 50 each; batch control is capped at 100. Maximum 400 delivered rows / $0.06 result fees at the assumed rate.
3. In Console set a small charge ceiling for each preflight (e.g. $0.02) and a short timeout (e.g. 180 seconds); these are RUN options, not Actor input JSON keys. Check the displayed result rate for your account and actual cost after each run. A row cap is not an all-in dollar guarantee.
4. Review every returned preflight row. Use verify_followup.py to flag missing literal anchors, date violations and excluded-author matches. It checks query compliance, not whether the post reports a genuine customer experience. Manually inspect up to 50 posts per preflight for buying/service relevance and source role. Proposed gate: investigate any obvious keyword leakage or excluded-author returns; revise a topical query if fewer than about half the inspected compliant posts address its intended decision. This is an operating threshold, not a validated statistical rule. Empty output is not evidence of zero real-world demand.
5. Recover context with 02_context/01_missing_roots_and_parents.json. It contains real missing IDs selected from the pilot. Read the returned roots before running 02_selected_conversation_replies.json. Drop unrelated roots; do not assume every comment under an automotive root is a customer account. Replies mode collects direct replies; missing nested replies are not guaranteed recovered. Use tweetIds or a documented conversation search only for necessary missing context, within remaining spend.
6. 02_context/03_smartdrive_programme_claims.json deliberately includes corporate posts. It is for identifying a published programme and its terms, not measuring customer uptake. Verify an actual written contract/manual on an official source before making any current programme claim.
7. Only after preflight passes, run either FOUR files in 03_bulk_after_checks OR the selected single-query jobs in 04_atomic_searches. NEVER run both versions of the same search. Atomic files give exact requested-query provenance and are the fallback if multi-query batching misbehaves. They also let you skip already-exhausted themes. Do not run all 176 atomic jobs merely because they are supplied.
8. All main searches use simple mandatory quoted terms, no OR expansion, four nonoverlapping 2026 date windows, and explicit exclusions for the two dominant Toyota/Auto2000-branded accounts. Exclusions apply to authors, not customers mentioning those brands. We do not blanket-exclude links, promotions or all seller accounts. Sell-side evidence and genuine user accounts with unrelated business promotion must still be separated after collection. No language filter is used: the pilot labels every record in but includes visibly non-Indonesian content. This change probes language omission and does not establish Indonesian residence. Screen language/market after export.
9. Date-only bounds use UTC. Since is inclusive and until exclusive. The final bound is 14 November 2026 00:00 UTC / 07:00 WIB. Window lengths differ; per-window caps cannot measure posting rates. Exact terms can miss spelling variants and synonyms. Add variants only after a useful theme is demonstrated, and record a new input revision.
10. At the listed $0.00015 rate, main ceilings are P1 9,600 / $1.44; P2 14,400 / $2.16; P3 8,000 / $1.20; shared 800 / $0.12. Suggested Console event-charge ceilings match those amounts. Actual remaining balance must be checked because pilot usage and previous runs are unknown.
11. Optional Top discovery is capped at 2,000 / $0.30. It overlaps Latest intentionally and is a distinct ranked discovery supplement. Do not use it to estimate prevalence. All new stages together cap at 36,815 delivered rows / $5.5222 result fees at the assumed rate. Including the 434-row pilot would imply $5.5873 result fees before platform usage. This is not your actual invoice or confirmed remaining balance. Stop if actual cumulative costs would exceed the $10 total.
12. Export JSON, submitted input, run ID, run status, actual usage and any diagnostics/run-report together. The pilot export alone did not include those run-level records, so query attribution, underdelivery cause and cost are unknown. Preserve result IDs as strings.

FILES
FINDINGS.txt: interpreted findings and decision implications.
pilot_metrics.json: exact mechanical counts and limitations.
PRIVATE_all_434_screening.csv: full export screened for source/context flags, with pseudonymous author keys; not a validated qualitative classification of every record.
PRIVATE_curated_evidence.csv/.json: 27 purposively selected analytical examples, including exclusions and counterexamples; not 27 independently verified customers or an exhaustive relevance count.
repository_integration.json: repository version, files read and evidence crosswalk.
repository_overlap_audit.json: exact X-status URL scan; not a person-level overlap test.
search_job_manifest.csv: one row per requested atomic search; the request log is not a count of returned matches.
verify_followup.py: local export audit, with no network calls or paid actor execution.
reproduction/: original-workspace analysis/build scripts; paths need adjustment for another environment.
followup_budget.json: conditional event-fee ceilings.

PRIVACY AND INTERPRETATION
PRIVATE files retain source URLs for your internal checks; do not publish the row-level files. Contact emails and common Indonesian phone-number patterns are removed from text copies, and author biographies/media are omitted. This pattern screen is not an anonymity guarantee. Raw export remains unchanged outside this pack. Anonymize public examples and minimize identifying detail.
All qualitative interpretations were produced by one AI analyst, with local arithmetic checks. No human coding reliability, recruitment, dealer fieldwork or offline transaction verification is claimed. Existing repo AI coding is not independent validation of this pilot. Keep unknowns explicit.
The latest 14 November strategy guides the three prongs. The repository is the 11 November evidence baseline. No repository files were changed or pushed.
