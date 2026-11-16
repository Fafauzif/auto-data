# Private Auto2000 interview update

This ZIP is a repository-root overlay for the integrated release on main at commit `bc1b282378bf1500c231ced1f82cac12781550ff`. It includes private participant materials. Use a local or private checkout.

## Apply the ZIP

1. If you have local edits to files listed in `manifests/interview_overlay.json`, back them up or commit them separately before applying the ZIP.
2. Extract into the repository root where README.md and .git already exist. Choose **Replace All** when prompted for the updated files. The ZIP uses repository-relative paths without a wrapper folder.
3. Open [the current executive findings](reports/EXECUTIVE_FINDINGS.md) and [the interview synthesis](analysis/interviews/INTERVIEW_SYNTHESIS.md). The refreshed integrated report and decision workbook are in reports/.

Optional offline checks from the repo root:

```console
python scripts/verify_interview_update.py
python scripts/verify_release.py --release-only
python scripts/source_archive.py verify
python scripts/verify_analysis.py
```

The overlay updates only the listed additions and replacements. The standard checkout-wide verifier already finds two oversized root-level legacy files on this baseline. The `--release-only` check verifies the official integrated release manifest while reporting legacy paths separately. Source copies and earlier versions are preserved. [MIGRATION.md](MIGRATION.md) covers the separate legacy migration if you want the older root-level duplicates moved to a sibling backup.

## Where to start

- [Executive findings](reports/EXECUTIVE_FINDINGS.md) and [integrated report](reports/INTEGRATED_REPORT.md)
- [Interview synthesis and pilot](analysis/interviews/INTERVIEW_SYNTHESIS.md)
- [Answer-level evidence and source locators](analysis/interviews/evidence_records.json)
- [Cross-source comparison](analysis/interviews/cross_source_matrix.csv) and [option priority update](analysis/interviews/solution_priority_update.csv)
- [Original private sources](sources/interviews/README.md)
- [QA results](qa/INTERVIEW_UPDATE_QA.json)
