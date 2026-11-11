# Customer narratives, owner forums and historical research

Research cutoff: 11 November 2026. This workstream produced 75 discovery annotations from 26 source documents and 20 fresh-source follow-up annotations from 12 additional documents. These 95 annotations include reported use, household and secondhand reports, questions, advice, employee accounts and research findings. They are not 95 verified customers, independent incidents or completed transactions. Some users recur across threads; multiple annotations share sources. The unit counts describe the curated material only.

The primary files are `narrative_units.jsonl` / `.csv`, `sources.jsonl` / `.csv`, `validation_units.jsonl` / `.csv`, and `validation_sources.jsonl` / `.csv`. `BIBLIOGRAPHY.md` lists ordinary source URLs. The build scripts recreate the structured annotations and descriptive counts offline from reviewed literals. They do not automatically discover new narratives. Public files contain concise researcher paraphrases, not a redistribution of entire third-party pages or reviewer profiles.

## What was done

Discovery used public search results and opened original forum/publisher/repository pages. It deliberately sought positive, mixed and contrary cases, not a complaint-only search. Twenty-one discovery documents are owner-forum threads and five are original publisher/repository records. One original Digiroom usability PDF was downloaded internally and its participant numbers and results were checked from extracted text. Some forum pages could only be read through search excerpts; these are labeled separately and support narrower claims. No account was opened, no private owner group joined, and no customer or employee contacted.

After the discovery corpus was coded, `validation_preregister.json` froze four follow-up predictions and competing explanations before searching fresh threads/documents. The follow-up is a purposive challenge sample, not a formal probability-sample hypothesis test. It adds new source documents but does not establish population independence or eliminate recurring commenter influence. The wording “held-out” refers to keeping these sources outside the initial discovery coding; the hypotheses were themselves developed from discovery, as disclosed.

NLP here means explicit aspect/event coding rather than a generic sentiment model. Each annotation records source, locator, actor/evidence type, brand/powertrain where known, task, short paraphrase, trigger/action/outcome when available, aspect codes, temporal limits and overlap flags. One AI researcher did source-grounded coding. No human inter-rater coefficient, automated sentiment accuracy or causal effect is claimed. The original excerpts remain traceable through URLs, locators and retrieval notes; search caches and page changes limit repeatability.

## Evidence-backed insight cards

### 1. A service promise contains several different uncertainties

Discovery records N005–N006 distinguish inspection, parts arrival and repair from ease of claim processing. Fresh record V003 describes a claimed warranty offer later questioned on an eligibility condition; V011 and V019 provide historical staff/research context about service reception and booking queues. These sources support separating entitlement, appointment confirmation and physical fulfillment in the analysis. They do not establish the current prevalence of any Auto2000 failure.

Counterevidence matters: N002–N003 describe favorable Toyota response, and V010 is simply a historical early arrival before opening, not proof that a booked slot was missed. Existing appointment features may already satisfy many customers. A possible solution direction is clearer stage-specific information or confirmations; a simpler option is better explanation of existing procedures. Whether either matters commercially remains unknown.

### 2. Customers can value an app and a human channel in the same ownership journey

N007 describes one BYD owner using app booking alongside WhatsApp reminders and feedback. Historical Auto2000 project N071 describes WhatsApp/telephone preference; N073 concerns a separate, older TASIA communication study. Together they make channel complementarity a plausible research lens. They do not show that current Digiroom users behave identically or that WhatsApp is the cause of low MAU.

The competing explanation is that customers rationally prefer a familiar channel for infrequent tasks, even if a dedicated app works well. Broad options include preserving context across assisted contact, connecting existing capabilities, or retaining the simple channel where it already performs well. The evidence does not justify making every task app-only.

### 3. A service record is decision evidence, while an official-dealer premium remains unproven

N013–N017 show a post-coverage owner weighing service cost and future resale, with contrasting views on whether official history or complete receipts matter. Fresh V001–V002 and V015–V016 extend the question to low-use ownership and used-car inspection. They support the existence of a record/condition information need. They do not establish a price premium, a willingness-to-pay figure, or that a digital record must be exclusive to the dealer.

In the historical Digiroom study, N066–N067 separately concern app/receipt consistency and history findability. These are distinct from “the feature does not exist.” Possible directions are intelligible record scope, document reconciliation or condition evidence at used purchase. A counteroption is simply improving how customers retrieve existing information. Current completeness and update timing need current-version evidence before being called a defect.

### 4. Powertrain fit depends on the household's circumstances, not a single EV attitude

N018 shows a low-mileage shopper reporting a shift away from a strongly liked EV. N035 describes a fixed-budget household considering ICE. Fresh V004 identifies an existing household ICE car as a reason a shopper becomes more willing to choose an EV for daily use. V007 shows household consensus and a salesperson's inability to answer concerns complicating an EV shortlist. V009 describes an actual early hybrid purchase/trade-in report, motivated by several product and service considerations rather than a single cost metric.

These accounts retain VH4 as a bounded descriptive hypothesis: budget, local support, intended usage and household alternatives can alter the choice. They neither demonstrate how common each mechanism is nor forecast conversion. Possible directions include household-context comparisons, plain-language trade-off explanations and evidence-backed assisted advice. A rival is genuine preference for design or driving feel that persists even when economic information is complete.

### 5. Charging reassurance has a home baseline and an occasional-trip exception

N036–N038 contain both holiday charging inconvenience and workable long-distance/home charging accounts. These are compatible once trip timing, access and household charging differ. Fresh V004 and V015 reinforce that a household backup car or limited local dealer support can change the practical question. No technical claim or infrastructure availability estimate is inferred from these anecdotes.

Possible directions are fit assessment around actual routes and charging access, clearer scope for existing information, or adviser support for exceptional trips. A universal charger-map feature might add little for an owner who primarily charges at home. Conversely, home charging does not settle destination or peak-season access. This is an insight about segmentation and information questions, not a recommendation to build infrastructure.

### 6. “Free service” and “warranty” do not identify one uniform entitlement

N050 reports a BYD coverage dispute; N058 asks about specific Toyota warranty work; fresh V003 describes a disputed exception and V018 repeats an unverified second-owner warranty distinction. These narratives establish questions or allegations, not the correctness of any claim. Fresh V020, Toyota's program page, explicitly represents different labor/parts benefits for different programs. That policy source supports the need to reconcile exact model, program, date and terms before declaring a mismatch.

VH3 remains mixed: genuine exclusions, understood terms or noncovered circumstances can explain charges without a communication failure. Possible directions include task-specific entitlement summaries, clearer source links and separating a quote from a covered benefit. Generic promises or financial forecasts would exceed the evidence.

### 7. Viral brand sentiment can obscure who controls the outcome

N024 presents an alternative account assigning an accident-repair dispute to insurer approval; N075 questions the issuer of a viral Zenix estimate. Neither resolves the incident, but both show why workshop, insurer, finance company, OEM and adviser roles must be distinguished. N034 captures contested peer diagnosis, not a technical finding. A suspected fault, an accident, an eligibility denial and a communications delay require different evidence.

Possible directions include source-attributed facts, clear responsibility information or explanation of existing processes. The current corpus cannot assign legal or technical fault, estimate defect rates, or declare a brand unreliable from a viral incident. Removing hearsay and unresolved attribution is an analytical requirement before using social data for a business conclusion.

### 8. Staff incentives and authority may shape the promise customers receive

Historical N059–N060 describe an alleged reversed discount promise and a separate favorable escalation. Fresh staff-role annotations V012–V014 concern documentation/workload, overlapping duties and price authority. They are self-reported employee experiences, not internal operating measurements. They make roles and authority a legitimate stakeholder question rather than a proven Digiroom bottleneck.

V011 also describes a positive working context with a scheduling challenge. The source platform's employee rating is not a customer satisfaction score. A possible direction is clearer public commitments or more coherent information authority; another is retaining local flexibility where it benefits customers. No staffing, incentive redesign, implementation or rollout is selected here.

## Follow-up hypothesis assessment

| Hypothesis | Fresh-source result | What remains unresolved |
|---|---|---|
| VH1: entitlement, scheduling and physical fulfillment are distinct | Limited descriptive support; current narrative plus historical staff/queueing material. Some apparent wait evidence was not informative. | Current frequency, customer interpretation, actual appointment adherence and transaction effect. |
| VH2: records matter, but dealer-exclusive resale value is contested | Mixed. Questions and advice recur; fresh used-car shopper values checks and confidence. | Actual resale outcomes, dealer-history premium and whether receipts substitute in the relevant transaction. |
| VH3: benefit labels can leave conditions/counterparties unresolved | Mixed, with explicit positive dealer experience and published program distinctions as counterevidence. | Whether customers misunderstood, terms were misrepresented, exceptions were correctly applied or invoices differ. |
| VH4: household context conditions powertrain fit | Retained as a descriptive mechanism across fresh shopper and owner accounts. | Population prevalence, causal effect of information, and completed choices for question-only threads. |

The assessment labels in `validation_units.jsonl` can be inspected record by record. Counting supporting annotations is not a vote or a significance test. One staff review, a research abstract and an owner account carry different evidentiary roles. The descriptive counts therefore should not be collapsed into a synthetic confidence score.

## YouTube transcript probe

`probe_video.py` retrieved YouTube robots rules and an official Digiroom booking video watch page through the shared transport. The page returned HTTP200 and contained an Indonesian ASR-caption track marker. `probe_captions.py` inspected the endpoint metadata and found the caption endpoint robots-disallowed; it made no caption request. Thus the result is accessible watch-page/caption metadata, zero transcript captures and zero transcript-derived customer events. The caption URL's transient signed parameters are excluded from public output. `video_probe.json` and `caption_probe.json` retain request IDs, statuses and the reason for stopping. Neither transcript package was preinstalled. No claim of a working no-key bulk YouTube-comment or transcript route is made.

## Interpretation limits

This is a purposive, platform-selected corpus, not a representative survey. Positive/negative counts reflect source choices and coding, not prevalence. Public account identities and ownership are unverified. Source date, capture date and app/model version are not interchangeable; some search and opened snapshots disagree on relative timestamps. The 2009 and 2020–2023 materials illustrate historical mechanisms and cannot diagnose the 2026 app. Unknown outcomes remain unknown. Quotes, prices, consumptions, technical diagnoses and asserted warranty terms in forum discussion are not adopted as verified facts.

The strongest output is a set of decision-relevant questions, descriptive mechanisms and broad options with counterevidence. It does not select a winning strategy, attribute incremental gross profit, design a rollout or present an implementation plan.
