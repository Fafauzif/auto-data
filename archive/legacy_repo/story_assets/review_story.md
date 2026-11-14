# Four visual pages: reviews and the evidence footprint

These briefs use the frozen source records. Chart numbers reconcile with the existing tables. The supplied visual reference contributes no research facts.

## A good rating may be about something else

Sixteen of the 20 displayed Digiroom reviews in the Indonesian Google Play view had four or five stars. Seven describe a specific app interaction. Five do not give enough detail to tell. Four describe another experience or come before a service was used. Even a specific app interaction can be a failed attempt. These records show why favorable stars alone cannot tell us whether someone booked successfully, completed a service or bought a vehicle. They describe this selected view, rather than all users.

**Implication:** Measure the task and its outcome before treating a rating as evidence of success.

**Visual:** One row of 16 equal tiles, grouped 7 / 5 / 4, with three large count labels. Use count labels as well as color.

**Exact chart labels:** Specific app interaction; Not enough detail; Other experience / not used yet.

**Chart note:** Specific app interaction includes failures. No completed transaction was independently verified.

**Evidence:** /workspace/scratch/70444ed5f561/auto2000_run/workstreams/reviews/reviews_derived.csv, /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_reviews/ER_T01_rating_experience_crosstab.csv, /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_reviews/ER_T02_classification_sensitivity.csv

**Limits:** Selected displayed records, not a representative user sample. Specific interaction includes failed attempts and does not establish completed service. AI source coding; no human validation or independently verified customer outcomes.

## Two listing views tell very different stories

The same BYD app has 19 favorable ratings among the 20 records displayed in its Indonesian-language view, but three among the 20 in its English-language view. Both views used the same store country setting and the same four-or-five-star rule. The two sets share no review IDs. Their dates also differ. This contrast shows how the selected view can change the apparent story. It does not identify reviewer nationality or establish a language effect on satisfaction, and it cannot support a brand league table.

**Implication:** Keep source selection consistent before comparing results.

**Visual:** Two rows of 20 equal tiles on the same scale. Fill favorable tiles blue and other tiles gray. Print 19 of 20 and 3 of 20 beside the rows; show 0 shared review IDs as a small annotation.

**Exact chart labels:** 4–5 stars; 1–3 stars.

**Chart note:** Selected listing records. Requested language does not establish reviewer location.

**Evidence:** /workspace/scratch/70444ed5f561/auto2000_run/workstreams/reviews/reviews_derived.csv, /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_reviews/ER_T03_original_locale_pair_sensitivity.csv

**Limits:** Both selected cohorts contain 20 records; the favorable threshold is aligned at rating >= 4. Zero overlap concerns source IDs, not verified unique people. Language and storefront do not verify geography or nationality. Displayed selection and date mix can change; this is not a causal language test.

## Most captured Digiroom reviews predate the relaunch

The first-wave Digiroom collection contains 50 reviews across Google Play and Apple. Thirty-seven carry dates before the 6 December 2025 relaunch; 13 are dated on or after it. Six of those 13 describe a specific app interaction. The rest do not establish one. Older accounts can reveal useful tasks and earlier friction, but they cannot describe the relaunched experience by themselves. A review date is also different from the date of the experience or proof of the installed app build. No before-and-after effect is identified.

**Implication:** Check the current journey directly before using old complaints to set priorities.

**Visual:** A 50-unit bar split into 37 before and 13 on/after the relaunch. Place a separate callout next to the 13-unit segment: 6 describe a specific app interaction. Do not draw a conversion funnel.

**Exact chart labels:** Before relaunch; On or after relaunch.

**Chart note:** Source review dates; no installed-build exposure or before/after effect is established.

**Evidence:** /workspace/scratch/70444ed5f561/auto2000_run/workstreams/reviews/reviews_derived.csv, /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_reviews/ER_T04_digiroom_relaunch_date_context.csv

**Limits:** The date is source-reported review date, not verified experience date or installed-build exposure. The 50 records are a selected historical/current mix, not a panel. Specific interaction includes failures; completion remains unverified.

## Different evidence answers different questions

The direct review collection contains 358 unique platform review IDs: 210 from the first wave and 148 added later. Separately, the narrative work contains 95 annotated units drawn from 38 public URLs. A unit can be a personal account, advice or a research finding. These quantities describe different objects and should not be added into one customer count. Several passages can come from the same document, and source IDs do not verify unique people. The package supports diagnosis and further questions rather than verified customer outcomes.

**Implication:** Match each source to the question, then seek customer and branch outcome data.

**Visual:** Two separate evidence cards, without a shared numerical axis or grand total. Card 1 shows 358 review IDs with a small 210 + 148 split. Card 2 shows 95 annotated units from 38 source URLs, keeping the nested relationship explicit.

**Exact chart labels:** Review records; Annotated passages / findings; Source documents.

**Chart note:** Counts describe records, annotations and documents. They are not counts of verified customers.

**Evidence:** /workspace/scratch/70444ed5f561/auto2000_run/workstreams/reviews/reviews_derived.csv, /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_reviews/new_reviews_derived.csv, /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_reviews/validation.json, /workspace/scratch/70444ed5f561/auto2000_run/workstreams/narratives/combined_metrics.json, /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_reviews/SECOND_AI_CHECK_RECEIPT.json

**Limits:** 358 review IDs, 95 annotation units and 38 URLs are distinct units, not additive customer counts. Several annotations may share one document or originate from related sources. Large auxiliary datasets remain separate from direct automotive consumer evidence. The new 16 targeted nonblind AI checks are separate from the first-wave 30 checks; neither is human validation or independent outcome verification.
