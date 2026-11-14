# Repository research integration

Read `RESEARCH_SYNTHESIS.md` for ten evidence-led decisions, then `COMMERCIAL_MODEL_SPEC.md` for outcome and GP accounting. `DISCREPANCIES_AND_PRECEDENCE.md` prevents conflicting numbers or historical instructions from silently overriding the current release.

The original 19-page casebook was recovered and its complete extracted text inspected for this integration. Its source hash is in `original_casebook_source.json`, searchable text in `original_casebook.txt`, p11 KPIs and case constraints in `original_case_kpis.csv`, and p10 P&L in `case_business_line_inputs.csv`. The case explicitly requires digital innovation at the core, reasons for regular use, xEV sales/after-sales GP, realistic costs/risks and an implementation roadmap. The larger integrated release is research support, not itself the 15-page competition submission.

The inherited reports and registers remain frozen evidence. Current recommendations are added as interpretation rather than silently rewriting them. `solution_priority_bridge.csv` maps every old consolidated concept to the current strategy. This table is not evidence of27 proven commercial opportunities.

## Machine-readable access layers

- `legacy_document_map.csv`: all inherited Markdown documents, titles, headings and hashes. This is a catalogue of preserved documents; it does not claim that every source body cited by those documents is available.
- `legacy_register_inventory.csv`: ten selected structured registers and their counts/hashes.
- `legacy_evidence_union.jsonl`:319 analytical records with namespaced IDs, original records, source filenames, zero-based array positions and source hashes. Registers can cite the same underlying study and are not independent sample units.
- `legacy_evidence_index.csv`: short navigation index for that union.
- `legacy_app_review_metadata.jsonl`:358 unique platform record keys, retaining first-wave/extension scope and published-source metadata. Source text was excluded from the old released metadata and is not regenerated.
- `legacy_narrative_metadata.jsonl`:95 source-grounded analytical annotations across discovery and follow-up. An annotation is not automatically a customer or a separate incident.
- `integration_research_checks.json`: ten offline arithmetic/count/uniqueness checks, with no claim of human or field validation.

## Reproduction

`build_research_integration.py` uses Python's standard library and performs no network requests. Run with `--legacy-root PATH_TO_PRESERVED_REPO --case-pdf PATH_TO_ORIGINAL_CASEBOOK.pdf`. It rebuilds the access layers and case tables in this directory from the preserved original inputs. It does not recreate historical source captures or AI semantic judgments, and does not regenerate the interpretive Markdown reports.

The old raw licensed sources include government-app sentiment labels, charging inventories and a single historical Audi's telemetry. Their analytical roles and licences differ. Do not count them as Auto2000 customer observations or infer Toyota health validation from their scale.
