# Second-agent review of cross-app annotations

Scope: a targeted, nonblind audit of 20 records from the 150-row initial review corpus produced by the reviews workstream. This is AI-agent source inspection, not independent human annotation, representative validation or a reliability estimate. It checks whether the derived descriptions stay within the reviewed source text. It does not verify that the underlying reviewer experience occurred.

Inspected initial normalized-record indices: 0, 2, 8, 19, 29, 34, 61, 68, 88, 107, 115, 121, 123, 129, 130, 136, 139, 140, 147 and 149. Matching evidence IDs: REV-0001, REV-0003, REV-0009, REV-0020, REV-0030, REV-0035, REV-0062, REV-0069, REV-0089, REV-0108, REV-0116, REV-0122, REV-0124, REV-0130, REV-0131, REV-0137, REV-0140, REV-0141, REV-0148 and REV-0150. Stable review keys, rather than row positions, are used in the review workstream's frozen labels.

## Corrections requested and reported applied

1. The annotation script described its work as “human annotations.” That was inaccurate for AI-performed coding. The reviews agent replaced that description and added AI-inspection / human-validation provenance fields.
2. The label `observed_app_job` could imply independently observed use. The reviews agent renamed it `self_reported_app_job`; the source's claim remains unverified.
3. REV-0141 describes generic positive app use and a charging-feature wishlist. It does not identify a completed specific job. The reviews agent changed its status to unknown rather than including it in the task-use category.
4. An exclusion flag mixed promotional-content exclusion with eligibility for app-task analysis. The reviews agent separated `excluded_promotional_content` from `eligible_for_app_task_analysis`. Prospective, unknown, branch and product-only material cannot establish app task completion.

The other 19 targeted records' scoped descriptions were consistent with their inspected text at this audit. This statement is not a 95% accuracy estimate: the sample was deliberately selected, not blind or random, and labels are not a ground-truth set.

## Checks that supported the current design

The code confines `pre_digiroom_relaunch` to Digiroom and leaves it null for other apps. Review dates, source platform and available app versions remain explicit. Lexical mention flags are labeled as mentions, not complaints, sentiment or verified defects. Promotional contact content is excluded from experience interpretation. High ratings can coexist with a reported problem, a prospective comment or an updated resolution; the audit found examples of each in its selected records.

Specific historical cohorts must remain separate from current-app interpretation. Source-selected listing samples do not support brand rankings, task-success rates or prevalence estimates. A review praising a branch, a vehicle or future purchase interest should not be converted into evidence that a booking or service was completed through the app.

## Version boundary

The reviews agent reported the corrections applied to the initial 150 rows. Later new source records, if appended, need their own annotation and provenance checks; this audit does not automatically validate them. The reviewers' agreement is not independent evidence about customer truth.

## Appended-cohort audit

A further targeted, nonblind second-AI inspection covered REV-0151, REV-0165, REV-0179, REV-0184, REV-0191, REV-0197, REV-0203, REV-0205, REV-0207 and REV-0209 after the corpus grew to 210 rows. Their scoped codes and app-task eligibility were consistent with inspected text; no additional label correction was requested. Thus 30 targeted source texts received this second-agent check, not all 210.

Two substantive boundaries emerged. An English-language ID-storefront review discusses snow and ice, so storefront/language cannot establish Indonesian residence or use conditions. One review says smart-charging controls were added, while another asks for charging controls; model, market, version and timing may differ. Neither should be converted into a universal BYD feature-absence claim. The explicit unknown label on a generic daily-trip-summary request remains appropriately conservative.

A final file inspection confirmed the corrected provenance fields and app-task eligibility flags in the 210-row derived CSV. This is verification of annotation scope and file fields, not verification of customer truth or a human reliability result.
