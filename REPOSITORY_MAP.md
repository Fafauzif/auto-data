# Repository map

| Path | Role | Start with |
|---|---|---|
| `PROJECT_CONTEXT.md`, `context/` |Current mandate, reconstructed session history, decisions, status and continuation questions |PROJECT_CONTEXT.md |
| `reports/` |Integrated English argument, executive findings, editable/report/workbook outputs |EXECUTIVE_FINDINGS.md |
| `data/` |Machine-readable active insights and evidence crosswalk |insights.json |
| `analysis/social/` |All X/Maps/YouTube normalized records, run membership, codebook, curated cases and scripts |README.md, SOCIAL_SYNTHESIS.md |
| `analysis/social/maps_deep/` |Branch-specific qualitative mechanisms and selected positive/negative contrasts |MAPS_MECHANISM_REPORT.md |
| `analysis/geography/` |Independent raw-route audit and new branch/job portfolio analysis |GEOGRAPHY_INTEGRATION_REPORT.md |
| `analysis/research/` |Original case, prior capabilities, market, economics, external studies and 27alternatives |RESEARCH_SYNTHESIS.md |
| `archive/legacy_repo/` |Original repository snapshot excluding Git internals |Original READ_FIRST.md is historical |
| `sources/session/uploads/` |Original supplied exports, PDFs, text and context |Resolve through source inventory |
| `sources/geography_latest/` |Newest full geography members, with deduplication aliases |Resolve/materialize through source inventory |
| `sources/archive_members/` |Members from older ZIP packages |Source inventory/container register |
| `archive/session_work_products/` |Original pilot/run plans, Apify inputs, scripts, reports and handoffs |Collection/context chronology |
| `manifests/` |Source provenance, aliases, original container metadata, hashes and release integrity |source_inventory.jsonl |
| `scripts/` |Verification, source restoration, migration and offline current-analysis rebuild |reproduce_analysis.py --help |
| `qa/` |Current analytical/release checks |RELEASE_QA.json |

A logical source path may resolve to an existing file at another path when bytes are identical. `manifests/source_inventory.jsonl` is authoritative. `source_archive.py restore` reconstructs one exact logical source under ignored `.restored/`. The source-container companion preserves exact old ZIP bytes and is not needed for routine analysis.
