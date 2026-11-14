# App-store findings and hypothesis tests

Prepared 11 November 2026. Dataset: 210 deduplicated public review objects,180 from nine Google Play public details pages and30 from three Apple public review pages. Every record was source-inspected by an AI researcher and coded; a second AI checked30 targeted records. No human reviewer participated. These are store-selected convenience samples; counts describe the released sample only. No completed customer transaction, app usability test, branch fulfillment or causal effect was independently verified.

## Coverage

| App | Google ID-language sample | Google EN-language sample | Apple sample | Google ID-language date range | Apple date range |
|---|---:|---:|---:|---|---|
| Digiroom |20|20|10|2019-03-15 to 2026-11-01|2020-06-19 to 2022-01-21|
| mToyota |20|20|10|2026-04-30 to 2026-11-07|2020-03-24 to 2026-10-30|
| BYD AUTO |20|20|10|2024-11-27 to 2026-10-26|2026-03-16 to 2026-10-28|
| myHyundai Indonesia |20|0|0|2023-05-13 to 2026-05-25|Not collected|
| My Wuling+ |20|0|0|2019-08-09 to 2023-04-09|Not collected|
| My Mitsubishi Motors ID |20|0|0|2018-12-06 to 2026-10-15|Not collected|

Android source locators are https://play.google.com/store/apps/details?id=id.co.astra.ai.dev1&hl=id&gl=ID , https://play.google.com/store/apps/details?id=com.toyota.m&hl=id&gl=ID , https://play.google.com/store/apps/details?id=com.byd.bydautolink&hl=id&gl=ID , https://play.google.com/store/apps/details?id=id.co.hyundaimotor.mmp&hl=id&gl=ID , https://play.google.com/store/apps/details?id=com.yonyou.cip.sgmw&hl=id&gl=ID and https://play.google.com/store/apps/details?id=id.co.mmksi.mitsubishimotors&hl=id&gl=ID . Apple locators are https://apps.apple.com/id/app/id421805050?see-all=reviews , https://apps.apple.com/id/app/id1480809215?see-all=reviews and https://apps.apple.com/id/app/id1492400299?see-all=reviews . Individual review IDs, dates, ratings and version fields reside in reviews_derived.csv under stable REV identifiers. These pages may later select different records.

## Finding 1: a star rating does not establish the customer job completed

Digiroom includes a four-star rating before service experience (REV-0001), a five-star account explicitly without a vehicle (REV-0020), and high ratings alongside a reported multi-car booking limit (REV-0003). Other records praise scheduling (REV-0005, REV-0013, REV-0018). This contradicts the assumption that a favorable rating alone proves completed ownership service. It does not show that favorable ratings are false, incentivized or unhelpful. A prospect can reasonably value discovery.

Across the210 records, primary AI classifications were132 specific reported app interactions,17 branch experiences,10 product reviews,5 explicit prospective/no-job accounts and46 unknown/generic/request accounts. Labels are interpretive, overlap can exist, and all outcomes remain unverified. A positive rating may concern different actors and stages.

Strategic implication: define engagement outcomes by job and stage. Track request acceptance, branch confirmation, attendance and completed invoice separately from ratings, downloads or feature interest. Protect prospect usefulness rather than excluding nonowners from the app.

## Finding 2: request acceptance and operational confirmation deserve separate measurement

Two 2026 mToyota Android accounts allege unconfirmed/cancelled service bookings; one reports keeping an offline alternative (REV-0030, REV-0035). Positive mToyota scheduling and support accounts also exist (REV-0022, REV-0023, REV-0033, REV-0034). This establishes contradictory reported episodes, not failure prevalence. These refer to mToyota, not necessarily Digiroom or an Auto 2000 branch. A 2020 Mitsubishi account likewise alleges central confirmation without a matching dealer record (REV-0116); it is historical context.

Candidate mechanism: the digital request and fulfillment system may expose different states. Rival explanations include invalid requests, customer cancellation, slot rules, stale builds or local exceptions. No backend evidence chooses among them. Candidate option: a confirmation-and-exception workflow with responsibility, expiry and a fallback path. Test it with actual handoff timestamps before claiming uplift.

## Finding 3: digital ownership records are useful infrastructure with a continuity obligation

Historical Mitsubishi accounts describe missing service records/booklets after paperless transition (REV-0108, REV-0110, REV-0113), while a 2026 account values digital manuals and booking (REV-0101). Hyundai samples contain both history/support praise and an older claim of stale records (REV-0064, REV-0068, REV-0069, REV-0071). These do not establish current cross-brand defects.

Candidate implication: continuity and clarity may matter more than adding another history screen. A record could be provisional, delayed or limited in scope for legitimate reasons. Test whether the user can distinguish those states and obtain a correction. For Digiroom, the older history-scope request (REV-0014) remains historical; current widespread incompleteness is unproven.

## Finding 4: frequent connected-car utility does not automatically transfer to dealer economics

BYD samples distinguish car/staff praise from remote-use reports. Battery/status monitoring and remote control appear as specific jobs (REV-0042, REV-0045, REV-0047). Apple accounts request finer charging controls and discuss remote/voice behavior (REV-0141, REV-0145, REV-0150). Remote-feature usefulness is not measured daily frequency, paid demand, or incremental dealer profit. Vehicle, region, hardware and OEM permissions may constrain transfer.

For Auto 2000, an OEM-dependent control feature requires a different business case from a dealer-controlled service confirmation. Benchmark the underlying customer uncertainty and data/control owner before copying the feature. HEVs do not create BEV charging tasks.

## Finding 5: regression and recovery evidence should travel together

All20 Wuling Android examples are dated 2019–2023, so they are unsuitable for a current 2026 app ranking. They contain update-regression claims and counterexamples reporting restored functionality (REV-0081–REV-0085, REV-0090, REV-0098). Five-star ratings can coexist with functional complaints (REV-0089). Digiroom Apple examples are all 2020–2022; one reports images missing and another reports recovery after an update (REV-0122, REV-0130). Their value is methodological: keep version/date and resolution narratives, not just negative snippets.

Candidate option: explicit release reliability, feature-state messaging and recovery support. Validation requires current app builds and relevant devices; retrospective complaint counts cannot set today's priority.


## Additional finding: source-language selection can dominate an apparent competitor contrast

The requested Google Play language was changed from Indonesian to English for the same three apps, retaining country parameterID. Each additional page exposed20 distinct reviewIDs, with no overlap against its Indonesian-language sample. BYD's Indonesian-language set had19five-star ratings and one one-star; the English-language set had two five-star, one four-star and17 ratings of three or lower. These exact sample distributions demonstrate the danger of treating one public listing sample as a brand ranking. They do not estimate regional satisfaction or identify why the platform chose the records. Age, language, device, user mix, relevance selection and caching remain possible contributors. Two additional uncached BYD fetches returned the same20 IDs for each respective language, supporting short-window repeatability; this adds no independent customer records. See locale_recheck.json.

The English BYD cohort includes a cold-weather defrost account (REV-0197), reinforcing that storefront parameterID does not verify Indonesian operating context. Google account settings or platform localization may influence source display; no account geography was verified. The mToyota English cohort also emphasizes older reviews while its Indonesian-language set is2026-only. Keep these cohorts separate.

Digiroom's2026 English records report history availability (REV-0151) and a separate account reports incomplete history/catalogue plus device-setting restrictions (REV-0165). Availability and completeness are different propositions, not necessarily a contradiction. Both are individual accounts; device/current-version testing is needed.

BYD feature requests are not universal absence evidence: REV-0205 reports added smart-charging functionality, while REV-0141 requests finer charging controls. Date, vehicle, market, build and feature scope differ or are unknown. A transfer benchmark should record those conditions before recommending a duplicate capability.

## Hypothesis disposition

| Hypothesis | Evidence test actually performed | Disposition and next evidence |
|---|---|---|
| Favorable stars prove completed app service | Read ratings against reported task/actor | Contradicted as a sufficient proxy by explicit counterexamples; real completion requires operational data. |
| Current Digiroom service-history failures are common | Separate historical/current source cohorts and read records | Not established; no representative current denominator. |
| Booking handoffs can fail after a digital request | Read specific reported timelines plus positive exceptions | Plausible mechanism, reported episodes; actual system failure and prevalence unverified. |
| A connected-car feature is a transferable dealer strategy | Distinguish remote use from product/branch praise and data ownership | User utility suggested; transferability and dealer economics unresolved. |
| More negative lexical flags mean worse brand UX | Compare dates, selected page cohorts and rating/content mismatch | Invalid inference under this design; no brand ranking. |

## Quality and access

Google Play pagination and Apple RSS were excluded because their robots paths disallow collection. Those routes were never requested. Nine Android listing pages each exposed20 embedded review objects and three Apple pages exposed10. The parser's assumed comment location had changed; local extraction was corrected to the actual record array and manually checked. SEVA returned404 on both requested live listings despite indexed search records, retained as unavailable rather than empty sentiment.

Lexical flags are reproducible mentions, not validated complaint codes. A rule matching vehicle or dealer text can have false positives for a job; use AI source-inspection labels/source record. Coding is AI researcher interpretation; a second AI checked30 targeted records. No human validation or human inter-rater reliability was measured. Raw author names, promotional phone contact, full text and developer replies remain outside the public release. One promotional-contact review is explicitly excluded from experience analysis.

## What to test next

The highest-value operational validation is a small matched cohort tracing booking request→branch confirmation→arrival→work completed, with version/device and cancellation reason. Separately validate current record completeness, its timing and correction route. Contrast an existing-feature connection option, a handoff/recovery option and a new-utility option using control, implementation cost, customer benefit and net incremental contribution. No portfolio option is selected by this workstream.
