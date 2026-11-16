# Auto2000 integrated private research

**Start with the current findings and project context.** This release integrates X, YouTube, Google Maps, the original repository research, the original casebook, mentoring notes, collection plans and all available geographic source versions. It is designed to let a new analyst continue without the originating chat.

Secondary research cutoff: **14 November 2026**. The **16 November 2026 interview integration** adds three interviews and a proposed Yaris Cross Hybrid service-record pilot. Original repository snapshot: `34498fe033ae4dcd1a52c8d2e039f870b00d08fe` (see manifest for authoritative full hash). This is a private research release with original-language sources. Main analyses and documentation are English.

## Reading route

1. [Executive findings](reports/EXECUTIVE_FINDINGS.md): decisions and their evidence.
2. [Integrated report](reports/INTEGRATED_REPORT.md): full argument, three prongs, geography, digital proposition, economics and roadmap. PDF/DOCX and the decision workbook are in `reports/`.
3. [Project context](PROJECT_CONTEXT.md): current mandate, decisions, boundaries and continuation instructions.
4. [Repository map](REPOSITORY_MAP.md) and [data guide](DATA_GUIDE.md): where to find specific evidence and reproduce results.
5. [Interview analysis](analysis/interviews/INTERVIEW_SYNTHESIS.md): all three cases, evidence comparisons, pilot decision and gates.
6. [Active insight register](data/insights.json): structured facts, interpretations, recommendations and source locators.

The original case requires digital innovation at the core, meaningful regular Digiroom use, xEV sales and aftersales GP, and a roadmap within IDR 150 billion for 2026–2028. Ordinary petrol workshop recovery supports the architecture and economics; it does not replace the xEV answer.

## Main findings

Existing eligible operator routing removes 19 of 39 modeled oil-access tails. Bandung contains 14 of 20 remaining tails, including eight at Soekarno-Hatta. Pancing and Tanjung Api-Api retain important general-workshop geometry despite zero remaining oil tails. The resulting investment choices differ: residual-access/prepared-job tests, service preservation and owned-channel routing.

The social evidence identifies paid arrivals left unacknowledged, forgotten or unresolved work, household logistics in hybrid buying, repair-versus-replacement choices and support/settlement dependencies in upgrade decisions. These selected accounts identify mechanisms rather than population complaint rates.

Digiroom should connect vehicle, job, entitlement, destination, accepted scope and final outcome across channels. Existing booking, health-check and appraisal capabilities are baselines. Measure regular useful digital activity together with incremental completed transactions and recognized Auto2000 contribution.

## Complete evidence and private originals

The source index records 2,660 logical source entries, including four private interview files, including 596 original repository files, 22 uploads, all 535 members of the newest full geographic package and historical work products. Counts are source entries, not independent evidence or customers. Byte-identical aliases resolve through the index instead of occupying duplicate files.

The integrated release contents follow a 90,000,000-byte ceiling. Older checkouts can still contain duplicated legacy files above that ceiling. Large originals have exact byte parts, hashes and a restoration index. The separate Source Container Vault is optional: it preserves original ZIP containers exactly. All their source-member content is already represented in this main repo.

## Installation and checks

For the November interview ZIP on an existing integrated checkout, see [INTERVIEW_UPDATE.md](INTERVIEW_UPDATE.md). For the earlier full release migration, read [MIGRATION.md](MIGRATION.md) before overlaying an existing checkout. Extract/Replace All does not delete old files. Run the migration dry run, review conflicts, then apply as instructed. The script protects `.git`, changed files and unknown user files.

```console
python scripts/verify_release.py
python scripts/source_archive.py verify
python scripts/reproduce_analysis.py --help
```

The integrity and current analytical checks use Python 3.10+ and the standard library. Source data do not require a paid actor or network access to reanalyze. Regenerating styled Office/PDF artifacts has separate dependencies documented with the presentation build scripts.

## Current authority

Follow [AGENTS.md](AGENTS.md) and [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md). Earlier prompts, budget balances, diagnosis-only instructions and run plans in `archive/` are historical records. Current user authorization includes integrated recommendations and a private replacement package. No GitHub push or paid scraping was performed.
