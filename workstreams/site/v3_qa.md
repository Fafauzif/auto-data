# Version3 cached-source reference check

Checked 11 November2026 at03:12UTC by a separate AI researcher, with no new network requests, human reviewer or browser rendering. The same fixed24source captures as v1/v2 QA were used. The production database was opened read-only and not modified.

The v3 collector now uses identified prose or the populated inner main, removing the generic article fallback. Independent parsing of the cached source bodies produces no zero-word selections in these24references. It restores the two v2 failures: the adviser profile has725selected words and the bZ4X video page has347selected words. Empty `yt-lite` media wrappers no longer override those populated page containers.

`v3_qa_reference.csv` contains expected selector, wordcount, contenthash, main-linktargetcount, numeric-Rpflag, exactcanonical, globalH1/forms, originalcapturetime, source requestID and SHA256 for every reference. No additional quoted page text is exported. This is an expected-source reference, **not confirmation that the production database has completed the v3 reparse**.

After the root finishes reparsing successful cached pages and before final export, run `v3_qa_reference.py --compare-live` using the primary Python runtime with `private_cache/site_deps` on PYTHONPATH. It performs no fetch or production write. It compares version3.0, selector, wordcount, contenthash, mainlinktargetset, numericflag, canonical, globalH1/forms, cappedtitle, capturetime and requestID against the fixed captured sources. Results go to `v3_qa_published_comparison.csv` and `v3_qa_reference_summary.json`; inspect the actual flag and passcounts rather than assuming success from this document.

Reference-stage result:24sources; two nonempty selections restored; zero expected zero-word selections; production_v3_verified=false until the stored comparison actually passes. Final global version/error counts still need root release validation. A24source check cannot certify all pages, rendered behavior, accessibility, indexing, prices or customer task outcomes. The reparse and reference rows are transformed views of earlier source captures, not24new independent sources.

## Subsequent production comparison

The actual cached-source comparison has now run. `v3_qa_reference_summary.json` records production_v3_verified=true at2026-11-11T03:21:45UTC, with every listed check passing on all24fixed sources. `v3_qa_published_comparison.csv` preserves the per-source results. A final separate read-only check finds all281successful error-free production rows are version3.0. Earlier paragraphs describe the prior reference-only stage; they are not the current production status. This is still an AI cached-source check, not human, rendered-browser or customer validation.
