# Reproduce the selected battery analysis

The full package already contains the exact five licensed MAT bundles under `raw_licensed_data/EV_TELEMETRY_CC_BY_NC_3_0/{Charge,Drive}/Folder*/Raw.mat`. No network or private working cache is needed to rerun analysis. Keep this directory structure.

Install Python with numpy, pandas, scipy, h5py and matplotlib. Exact analysis-environment versions are recorded in `REPRODUCTION_ENVIRONMENT.json`. Both MATLAB7.3/HDF5 and MATLAB5-compatible files occur in the subset.

From the package root, run:

```bash
python workstreams/extension_battery/analyze.py
python workstreams/extension_battery/verify.py
```

The analysis first checks its original working cache and otherwise falls back to the included licensed raw appendix. `signals.py` reads both file formats. Outputs use elapsed or aggregate time and retain no absolute driving chronology in the figures. The original MAT files do retain the source epoch metadata. See the privacy/rights review.

`collect.py` and `download_subset.py` preserve the original acquisition workflow; their initial catalogue-listing responses were working-cache intermediates. For independent reacquisition without those intermediates, the stable original file download URLs and expected SHA256 hashes are in `SOURCE_FILE_MANIFEST.json`. Download each URL into the indicated Charge/Drive folder and verify the source hash before analysis. Publication requires source attribution and compliance with CC BY-NC3.0. The source paper fulltext is not part of this package.

Do not call scalar samples independent customers, five bundles five sessions, partial SOC slopes capacity, pack-terminal electrical throughput charger wall energy, or source data a Toyota-health validation set. The source authors already applied cardinality reduction. These constraints are part of the reproduction, not optional plotting preferences.
