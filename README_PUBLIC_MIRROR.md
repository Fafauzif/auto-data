# Main download and public backup are different variants

The main **Auto2000_Research_Project_Full.zip** contains the original licensed IGAR Rating_labeled.csv and VADER_labeled.csv, alongside all reports, derived tables, other licensed raw datasets and both earlier ZIPs. It is the complete primary research release for the requesting user.

The anonymously hosted **Auto2000_Research_Public_Backup.zip** omits exactly those two original IGAR CSVs. An aggregate offline screen found a plausible self-disclosed phone number and additional identity/member-number flags. These are disclosure-risk flags, not verified identities. A redistribution license does not establish consent to anonymously mirror personal information. A simple pattern mask would not establish that the remaining free text lacks other disclosures.

The public backup retains the **617,722-row, 15-column nontext feature table** at workstreams/datasets/IGAR_AUXILIARY_nontext_features.csv.gz. It includes pseudonymous record keys, coarse month and analytical fields. It omits review content, translation, reviewer names/handles and exact timestamps. These are derived features of the same auxiliary corpus, not additional customer observations. The SPKLU raw inventory, attributed BPS table objects, all analytical outputs, original IGAR hashes and source acquisition instructions remain included.

In the public variant, the top-level manifest.json is the authoritative list of files actually present. It sets release_mode to public, lists the two withheld paths and marks igar_original_raw_text_included false. Original-file source manifests and primary-release QA receipts remain documentary records of the main release. They must not be read as claims that the omitted source files are present in this mirror. Likewise, report statements that both original IGAR files are included describe the primary release.

Original source: Isnan, M., and Pardamean, B. (2025), IGAR: Indonesian Government App Review Dataset, version 2, Mendeley Data, CC BY 4.0, https://doi.org/10.17632/7zryc6k76z.2. Source filenames, download URLs, provenance and original SHA256 values appear in raw_licensed_data/DATASET_SOURCE_MANIFEST.json and workstreams/datasets/igar_acquisition_log.jsonl. See reports/REPRODUCIBILITY.md for exact-input versus nontext-only reproduction boundaries. Do not interpret access to the original public source as a certification of personal-data consent.

The public variant is a useful additional copy of the analysis and nontext data. It is **not a byte-for-byte backup of the main ZIP**. Each archive has its own checksum and actual upload receipt. Temporary hosting is not permanent preservation.

## Smaller-host volume layout

For hosts with a 100 MB limit, **Auto2000_Public_Backup_Core.zip** contains the public-safe reports, context, metadata, code and nontext data, while the five exact MAT files are distributed in **Auto2000_Telemetry_Volume_01.zip** through **Auto2000_Telemetry_Volume_05.zip**. Each is a complete, independently extractable ZIP, with one complete MAT file and attribution. Extract all six into the same directory; their shared Auto2000_Research_Project folder restores the public variant. No binary concatenation is required and no MAT file is truncated.

The core manifest marks telemetry_separate_volumes true. The external backup index supplies checksums, actual links and upload verification status. These volumes preserve the selected telemetry scope. They still omit the original IGAR text files for the stated privacy reason.
