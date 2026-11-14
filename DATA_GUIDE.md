# Data guide

## Current social corpus

| Platform |Export rows |Unique platform IDs |Primary key |
|---|---:|---:|---|
|X |14,892 |14,291 |post ID |
|Google Maps |8,385 |8,119 |review ID |
|YouTube |74 |74 |comment ID |
|Total |23,351 |22,484 |platform plus ID |

All IDs remain in normalized/deduplicated JSONL corpora under analysis/social/cleaned, including irrelevant and promotional records. This is not a fully validated owner-only sample. Original and normalized body fields remain separate. record_run_membership.csv preserves all 23,351 source-row memberships. Hashes are in source_runs.csv. Lexical flags are nonexclusive retrieval aids, not validated topic prevalence.

Maps has 37places and 5,504reviews with text. The diagnostic all-years lowest-ranking sample overlaps the other samples by 266IDs; sampling memberships remain explicit. Latest selected cohorts contain 1,915Auto2000and932 Shop&Drive rows. Publication time is not incident time. The closed B-Quik source is retained historically and must not be used as an active destination.

X has 8,162 author keys, 6,186 replies and 5,704reply records without the immediate parent. Public author keys do not authenticate owners. YouTube covers three actual returned videos, 56top-levelcomments and 18 replies; no Toyota video is present. Relative YouTube publication strings remain relative.

## Geography

Current independent audit uses 82,296distinct outbound origin/destination comparisons across 324distinct baseline origin keys. The strict paired analysis retains 284 origins:Surabaya 59,Medan 78,Bandung 78,Palembang 69. Corrected general-workshop destination count is 29. Five-minute gaps and 15-minute accessibility are analytic definitions. The network model is not live traffic, customer demand or branch capacity.

Owned eligible OtoXpert routing changes oil-gap tails 39to20, with market counts 10to6,3to0,17to14,9to0. Bandung has 14of20 remaining origins;Soekarno-Hatta 8. Exact ties, Suci correction and separate Sidoarjo extension are retained. See analysis/geography for current methods and source map.

## Earlier research

Legacy app evidence contains 358unique IDs across 21listingcohorts. Narratives contain 95annotationunits from 38URLs. The 319-entry union comprises overlapping analytical registers, not 319 independent sources. All 27oldsolutions remain mapped to current priorities. The original casebook supplies the case facts; external tables have separate scopes and dates.

IGAR comprises 617,722 rows per label view describing the same underlying government-app corpus, with 617,703distinctcompositekeys. The two views are not two automotive samples. EV telemetry covers one historical Audi e-tron, with 56,507,201storedsignal values in five bundles, not Toyota battery-health ground truth. Raw originals and license notices are preserved privately.

## Schemas and raw access

The social codebook defines fields, deduplication and interpretation rules. Geography tables retain source IDs and metric definitions. The research union uses a namespace plus original ID. Consult the source inventory for actual stored paths and SHA256. Large originals have byte parts and can be restored exactly with scripts/source_archive.py.

Use scripts/reproduce_analysis.py to materialize input aliases and rerun the current analyses offline. This writes isolated rerun outputs rather than altering the final source corpus. Report-generation dependencies are separate from analytical standard-library code.
