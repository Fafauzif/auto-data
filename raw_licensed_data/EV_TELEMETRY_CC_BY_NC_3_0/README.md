# Selected real-world EV battery telemetry, exact licensed source files

Source: Pozzato, G.; Allam, A.; Pulvirenti, L.; Negoita, A.; Paxton, W.; Onori, S. (2023). *Real-world electric vehicle data: driving and charging*, Mendeley Data V2. https://doi.org/10.17632/7vdkzpnjgj.2 . License: **CC BY-NC 3.0**. Noncommercial restrictions apply to these source files. This is not a blanket license for the entire research package.

This appendix preserves five exact source MAT bundles plus the dataset README. It uses the original Charge/Drive folder structure, which can be opened in MATLAB. Python reproduction supports both HDF5 MATLAB7.3 and MATLAB5-compatible files. See the separate `SOURCE_FILE_MANIFEST.json` for exact bytes, hashes and original download URLs. The pre-existing raw-data manifest for other datasets is separate and does not cover these new files.

The purposeful subset comprises Charge Folder1/Folder7 and Drive Folder2/Folder8/Folder16. These are multi-interval folder windows, not five trips or five independent vehicles. The source study observes one Audi e-tron in California during2019–2020. This is auxiliary historical engineering data, not Toyota, Indonesian customer or Auto2000 data. The raw data have already undergone the source authors’ cardinality-reduction pipeline.

The five MAT files contain56,507,201 stored Curr/Volt/SoC/Temp scalar signal values, excluding clock arrays and Epoch values. Some signals share clocks and others do not. These counts are not independent events, synchronized multivariate rows or people. No upsampled rows are counted as observations. Source filenames are all Raw.mat; the distinct folder paths identify the bundles.

Actual raw fields are numeric battery current, voltage, BMS state of charge, pack temperature, their clocks, and absolute epoch timing. No GPS, VIN, owner-name or contact field was detected. Published epoch timing is retained in these exact originals. It could support linkage to external records; no complete anonymity certification is claimed. Public analysis figures use elapsed or aggregate time and do not expose an absolute trip chronology.

SOC is not state of health. The public source omits the confidential reference-capacity data discussed in the associated paper, and its capacity-estimation method is proprietary. The source README says charging current is always negative. Selected Charge data are overwhelmingly negative but include a tiny fraction of positive transients, a narrow exception rather than a reversed convention. Clock gaps can span days. Reproduction splits large gaps and reports sensitivity; do not integrate blindly across all adjacent array rows or infer usable capacity or health from partial charging intervals.

The associated full research paper is cited by DOI10.1016/j.joule.2023.07.018 but is not redistributed here. See `workstreams/extension_battery/BATTERY_TELEMETRY_REPORT.md` and its reproducible original analyses in the main package.
