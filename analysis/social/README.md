# All supplied social exports, integrated

Start with `SOCIAL_SYNTHESIS.md`, then `maps_deep/MAPS_MECHANISM_REPORT.md`. These reports link platform composition, selected original accounts and the three business prongs. They preserve distinctions among customer accounts, marketing, advice, allegations and technical claims. All report text is English; source bodies remain in the original language.

## Read the right layer

| Need | File |
|---|---|
| Corpus sizes and quality | `corpus_metrics.json` |
| Every X, Maps and YouTube record, normalized without truncating original body | `cleaned/x.jsonl`, `cleaned/maps.jsonl`, `cleaned/youtube.jsonl` |
| Exact source-run membership and one-based original row locator | `record_run_membership.csv` |
| Export names, sizes, row counts and source hashes | `source_runs.csv` |
| Descriptive branch-by-cohort sample sizes and rating counts | `maps_branch_cohort_summary.csv` |
| Pairwise X run overlap | `x_run_overlap.csv` |
| Returned YouTube videos and comment/reply counts | `youtube_video_summary.csv` |
| X/YouTube analyst-selected cases | `curated_social_evidence.jsonl` |
| Annotation for every returned YouTube comment | `youtube_analyst_annotations.jsonl` |
| Thirty-four selected Maps contrasts | `maps_deep/curated_maps_evidence.csv`, `.json` |
| Retrieval flags and interpretation rules | `codebook.json` |
| Integrity and boundary checks | `QA_SOCIAL.json` |

Original raw exports are retained in the enclosing repository's source archive. Use the repository source registry to locate the filename recorded here. The cleaned JSONL preserves the selected original body exactly in `text_original` and its exact original filename/row. `text_normalized` is a separate reading aid. Author hashes are stable within this analysis, not cross-platform person IDs. Full raw data and some private source URLs belong in a private repository.

## Rebuild offline

```bash
python build_social.py --input-dir PATH_TO_ORIGINAL_EXPORTS --output-dir OUTPUT
python curate_social.py --social-dir OUTPUT --pilot-cases PATH_TO_PILOT_CURATED_EVIDENCE_JSON
python maps_deep/build_maps_deep.py --input PATH_TO_ORIGINAL_EXPORTS --output OUTPUT/maps_deep
python verify_social.py --input-dir PATH_TO_ORIGINAL_EXPORTS --social-dir OUTPUT
```

Python 3, standard library only. No API key, paid Actor, browser or external service is required. The pilot case file is optional to `curate_social.py`, but reproducing the complete 45-entry release register requires it. It is the earlier `Auto2000_Pilot_Analysis_Followup/PRIVATE_curated_evidence.json` source, retained by the enclosing source registry. The release QA assumes the complete corpus and full pilot-inclusive curation.

## Rules for continuation

1. Preserve all source-run memberships. A duplicate post or review is not a new independent incident.
2. Keep lowest-ranking and latest Maps cohorts separate in any rate calculation. Their 266 overlapping IDs remain members of both samples; merging IDs does not erase sampling design.
3. Treat lexical flags as retrieval aids. First-person grammar does not authenticate an owner. The pilot explicitly contains a fictional purchase story.
4. A review date is not a visit date. A relative YouTube date must not be silently converted to an exact date.
5. A quoted assertion about battery life, programme terms, prices or factory status is source discourse, not an engineering or contractual fact.
6. A requested input, desired video or missing parent is not data returned by the Actor. Report actual results and gaps.
7. The three platforms do not define additive people or a representative Toyota market sample. Financial models require separately identified operating denominators and scenario assumptions.
