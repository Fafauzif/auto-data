# Review source records, raw metadata and counting rules

This release support layer adds source-record metadata for all210 unique app-store review IDs already analyzed in the reviews workstream. It performs no new scraping and does not add210 new customer experiences to the dataset. The same records are represented in different useful tables.

## Added files

`review_source_records_nontext.csv` preserves210 original source recordIDs, platform, app, requestedlocale, sourceURL, sourcecapture/requestID, capturetimestamp and contenthash, sourcepublishedtimestamp, rating, reviewcreatedversion where present, thumbs-up count where present, developerreply presence and reviewtext hash. It excludes the review text itself, title, author name, image, contact details and developer reply text. No verbatim excerpts were needed for the findings, so this layer republishes none.

`review_source_capture_index.csv` contains12 unique public page sources, with exactURLs, requestIDs, captureUTC, originalcaptureSHA256 and record counts. One source page can carry20 reviews; one Apple page carried10. A source page is not an independent reviewer. Locale mirrors may select different IDs and dates; locale/country parameters never verify reviewer residence.

`review_source_metadata_validation.json` verifies all210 source records join to transport/capture provenance, all have sourcebody hashes, and180 Google source epoch timestamps were recovered directly from the embedded review arrays. Apple dates were already source ISO strings. There are no duplicate platformreviewIDs or exact text hashes in this retrieved sample; this does not prove210 independent people or incidents.

`build_review_source_metadata.py` deterministically reconstructs these public metadata views from the run's private capture objects and derivedreviewIDs. It requires the root private transportcache for source hashes. It is not an upload tool, collector or proof of original-source licensing.

## Reacquisition and limits

The reviews workstream supplies collector/parser scripts that request only the allowed public Google Play details pages and Apple public review pages used here. They can reacquire whatever those public pages show later. Because source selection and site markup change, a future run may not return the same records. The current metadata preserves original reviewIDs, timestamps and capturehashes so this boundary is explicit. The source fulltext/HTML remains outside the public archive. A source locator alone cannot guarantee later fulltext recovery.

The installed parser's review callback location had drifted. This run corrected extraction locally and used source-grounded AI inspection; no human reviewer or verified customer outcome exists. No prohibited Play pagination or Apple RSS requests were sent. The public `reviews_derived.csv` records all210 sourceIDs/locators and the actual AI coding and check status. Full current review texts are not bulk-republished simply to make the ZIP bigger. Licensed raw corpora elsewhere in the release retain their separate status and unit definitions.

## Units that must not be summed as independent evidence

| Layer | Unit | Count relationship |
|---|---|---|
| reviews_derived.csv |One platformreviewID|210 original reviews in this workstream.|
| review_source_records_nontext.csv |Metadata view of the same platformreviewID|210 rows, zero additional reviews.|
| manual_audit.csv |AI interpretation/checkstatus for the same reviewID|210 annotations, zero additional reviews.|
| review_source_capture_index.csv |One requested public page/locale capture|12 sources carrying the210 reviews.|
| locale_recheck.json |A repeated retrieval of two BYD language variants|Zero additional reviewIDs.|
| Mention flags, ratingcells, aspectcodes, embeddings |A derived measurement or annotation|Never new people, reviews or independent source facts.|

At final release, count unique original units by source dataset first. Report derived feature/label rows separately, overlaps/joins explicitly, byte sizes honestly and unverifiable observations as such. A millions-sized matrix of labels or token-level fields must not be described as millions of original customer experiences.
