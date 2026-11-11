# Fifty-six million stored battery-signal values demonstrate a data pipeline, not a health certificate

The public telemetry supports reproducible electrical-signal analysis. It does not validate the proposed battery-health or certification claim. The associated study's reference-capacity series is confidential, its capacity estimator is proprietary, and no health-reference field appears in the ten public variables. Millions of scalar samples from one vehicle do not replace a labelled, calibrated validation study.

This extension acquired five exact licensed MAT bundles from Pozzato and colleagues' *Real-world electric vehicle data: driving and charging*, Mendeley Data V2, DOI [10.17632/7vdkzpnjgj.2](https://doi.org/10.17632/7vdkzpnjgj.2). The catalogue identifies CC BY-NC 3.0. The source paper describes one Audi e-tron operated in the San Francisco Bay Area during November 2019–October 2020. These are auxiliary historical engineering data, not Toyota, Indonesia, Auto2000 customers, warranty outcomes or resale transactions.

## What was actually acquired

The purposeful subset uses Charge Folder1/Folder7 and Drive Folder2/Folder8/Folder16. It includes early, middle and later source-folder positions and both operating-mode labels. It is not a random sample or a representative year of charging conditions. Folder15 was initially excluded because its 171 MB size exceeded the initial per-file selection bound. The README states that the public data have already undergone the authors' cardinality-reduction pipeline, so the filenames' word “Raw” must not be interpreted as untouched original CAN logs.

| Source folder | Mode label | Exact MAT bytes | Current samples | Segments under >30 s gap rule | Supported hours under ≤1 s rule |
|---|---|---:|---:|---:|---:|
| Folder1 | Charge | 51,900,236 | 3,311,696 | 1 | 9.199 |
| Folder2 | Drive | 32,644,636 | 2,144,773 | 15 | 5.958 |
| Folder7 | Charge | 89,170,861 | 6,136,329 | 4 | 17.045 |
| Folder8 | Drive | 14,389,506 | 929,380 | 10 | 2.582 |
| Folder16 | Drive | 95,036,227 | 6,188,617 | 76 | 17.190 |

The five MAT payloads total **283,141,466 bytes**. Their exact source README adds 100,654 bytes, making the source-file appendix 283,242,120 bytes before package metadata and compression. The largest individual file is 95,036,227 bytes. Each file's retrieved SHA-256 matches the original catalogue hash.

There are **56,507,201 stored current, voltage, BMS state-of-charge and temperature scalar values**, excluding clocks and epoch values. Separately, there are 56,599,111 timestamp scalars and 91,910 epoch-alignment values. These counts describe stored numeric values. They are not independent observations, synchronized multivariate rows, full charging sessions, trips or people. Interpolated endpoint values used in analysis are not added to the acquired sample count. The 106 segments are algorithmic contiguous windows under a declared gap rule, not 106 field-verified trips.

## 1. A row number is not a universal time join

Every selected file has identical current and voltage clocks. Consequently, the electrical-power integrals in this extension pair actual current and voltage samples directly; no voltage interpolation or extrapolation is needed. The generic concern about asynchronous signals must not be overstated as a current-versus-voltage error in these selected files.

State-of-charge clocks match the current clocks exactly in two of the five bundles. Temperature clocks match in none. Temperature typically updates at about 0.5-second spacing, whereas current and voltage typically update at about 0.01 seconds. A blanket rowwise join would therefore misalign or discard information. The charging-slope diagnostic uses only common observed time support and interpolates SOC at the selected interval endpoints. It does not extrapolate endpoints or bridge the long gaps.

The practical implication for M2 is a measurement requirement: the interface needs signal definitions, clock semantics, calibrated units and an auditable alignment method. A data model accepting columns named current, voltage and SOC would not by itself establish a valid diagnostic.

## 2. Gap-aware integrals are stable within the tested bounds; unbounded integration can still be badly wrong

Folder16 spans 50.824 calendar days, but only 17.190 hours lie on retained current intervals separated by at most one second. Its largest gap is 570,669 seconds, about 6.6 days. Across all five bundles, that strict rule retains 51.974 hours. Integrating first-to-last elapsed time as though every intervening value were observed would confuse calendar coverage with operation.

For each file, the analysis computes trapezoidal integrals of signed current and signed current×voltage over retained intervals. Positive and negative magnitudes are reported separately. The absolute terminal-energy integral means the sum of the positive and negative magnitudes; it is an electrical-throughput descriptor, not wall electricity or charger efficiency.

| Bundle | Gap-aware absolute terminal integral | Naive integral bridging every gap | Naive excess |
|---|---:|---:|---:|
| Drive Folder2 | 156.206 kWh | 230.433 kWh | 47.52% |
| Drive Folder16 | 303.871 kWh | 317.539 kWh | 4.50% |
| Charge Folder1 | 4.056 kWh | 4.056 kWh | 0.00% |
| Charge Folder7 | 85.094 kWh | 85.094 kWh | 0.00% |
| Drive Folder8 | 73.147 kWh | 73.147 kWh | 0.00% |

The 1-, 30- and 300-second maximum-step rules produce the same terminal-energy and charge-throughput integrals to reported numerical precision in these selected data. They retain different durations, but the added gap endpoints carry zero current in the relevant cases. This is a useful robustness result. It does not justify extending integration across arbitrarily large gaps. The deliberately unsafe unbounded calculation increases Folder2's signed current integral by 60.36% and its absolute terminal-energy integral by 47.52%. Those extra integrals are unsupported by observations inside the gaps.

This falsifies the proposition that a straightforward integral over adjacent array rows is necessarily a valid energy feature. It does not establish an actual error in a production BMS or prove that every folder is gap-sensitive. No claimed interval energy is usable battery capacity, total-trip consumption, energy sold by a charger or a state-of-health value.

## 3. Checking distributions prevents a false sign-reversal claim

The README describes charging current as negative. The two Charge bundles agree overwhelmingly with that convention. Folder1 has 99.8509% negative-current samples and Folder7 has 99.9096%. Only 63 and 176 samples, respectively, are positive. The positive fractions are 0.00190% and 0.00287%. Their gap-aware signed current integrals are −9.18484 Ah and −201.58483 Ah, while their reported SOC endpoints rise.

Positive maxima of 19 A therefore do **not** mean charging current is mostly positive. The correct documentation issue is narrow: the README's absolute “always negative” wording has rare positive observations. Their physical cause is not identified here. They could reflect transitions, auxiliary loads, signal processing or another mechanism; these remain alternatives, not findings.

The data support checking and documenting the convention. They do not support claiming a reversed charging convention, a corrupted charging trace or a battery-health failure from a min/max summary.

## 4. Partial-interval SOC slopes vary, with no health ground truth to interpret them

Four charge segments satisfy the specified common-support, duration-at-least-ten-minutes and SOC-gain-at-least-one-percentage-point rules. Their observed negative-Ah magnitudes per reported SOC percentage point range from **1.570 to 2.195**, a 39.8% maximum-to-minimum difference. They differ in SOC window, current, temperature and history.

| Charge interval | SOC gain | Negative Ah on common support | Ah per reported SOC point | Mean pack temperature |
|---|---:|---:|---:|---:|
| Folder1 / segment1 | 5.85 points | 9.185 | 1.570 | 23.89°C |
| Folder7 / segment1 | 51.30 points | 112.191 | 2.187 | 15.98°C |
| Folder7 / segment2 | 23.15 points | 50.810 | 2.195 | 13.51°C |
| Folder7 / segment4 | 17.85 points | 38.585 | 2.162 | 17.70°C |

All stored current values lie on an integer-ampere grid in these files. Folder1's median absolute current is 1 A, while Folder7's is 12 A. That is a numerical-resolution observation, not a calibrated current-error bound. The dataset does not specify a rounding-error model that would justify inventing a ±0.5 A accuracy guarantee. Low current, SOC quantization, different windows, thermal conditions and hidden BMS processing all complicate an interpretation of these ratios.

The analysis deliberately does not rescale the partial slopes into claimed full capacity, compare them with nominal capacity as a health score, or infer degradation from four nonrandom intervals. Temperature and time are confounded, especially because the selected charging bundles do not cover the full year. A varying partial slope is not proof of degradation or BMS error. It is evidence that a universal uncalibrated conversion from partial SOC gain to a health certificate is unsupported by this exercise.

## What this means for the battery concept

The public dataset makes telemetry ingestion, signal audits and explicit interval calculations reviewable. It does not establish the accuracy, portability or customer value of a proposed M2 health certificate. The missing reference matters more than the row count: the source README explicitly excludes the confidential capacity series shown in Figure2, and the associated paper says that the onboard capacity-estimation algorithm is proprietary. Actual public variables contain no independent capacity or SOH reference label.

A defensible research test would require an authorized Toyota-specific diagnostic interface, the meaning and calibration of each signal, an independent reference-health protocol under stated conditions, and validation across vehicles and relevant operating environments. Customer trust, warranty obligations and residual-value effects require separate evidence. These are evidence requirements, not a selected implementation or a claim that current Toyota diagnostics lack those capabilities.

## Exact raw files, privacy and reproduction

The source appendix is `raw_licensed_data/EV_TELEMETRY_CC_BY_NC_3_0`, preserving the original Charge/Drive folder paths. It contains five exact MAT files and the exact dataset README, plus a separate manifest. It does not change the earlier 17-source-file manifest. The full source paper is cited and held only in private working cache; it is not redistributed.

The actual ten raw fields are numeric current, voltage, SOC, temperature, their clocks and epoch timing. No GPS, VIN, owner-name or contact field was detected. Absolute published epoch timing remains in the exact originals. It could support linkage with external records, so the field screen is not a complete anonymity certification. Public analysis figures use aggregate or relative time and do not publish an absolute trip chronology. The exact raw source retains its noncommercial CC BY-NC 3.0 qualification.

Reproduce with Python plus numpy, pandas, scipy, h5py and matplotlib. Run `python workstreams/extension_battery/analyze.py` after placing the exact source files under the working cache paths described by `SOURCE_FILE_MANIFEST.json`, or use the included Charge/Drive appendix paths in the loader. Both MATLAB7.3/HDF5 and MATLAB5-compatible files occur in the selected subset. `scalar_count_receipt.csv`, `bundle_signal_audit.csv`, `gap_aware_signed_integrals.csv`, `gap30_segment_metrics.csv`, `charging_interval_soc_slope_diagnostics.csv` and `RAW_PRIVACY_AND_LICENSE_REVIEW.json` expose the units, assumptions and limits. Acquisition scripts preserve original source URLs, statuses, file sizes and hashes.

Associated primary paper: Pozzato et al. (2023), *Analysis and key findings from real-world electric vehicle field data*, Joule, DOI [10.1016/j.joule.2023.07.018](https://doi.org/10.1016/j.joule.2023.07.018). Dataset licence and README support the source-file appendix; no blanket rights claim is made for the research package.
