# Findings from the finite-window routing study

## What was acquired

Four explicitly hand-set origin rectangles, 81 regular cell-centre origins per market, 324 origins total. Expanded destination rectangles add 0.08 degrees on each side. The primary calculation acquired 76,221 directed OD comparisons to 941 finite inventoried destination rows (905 conservatively filtered mapped repair/service candidates, 27 Auto2000 location candidates and 9 OtoXpert outlets). These are matrix calculations, not observed customer trips or independent customers. Candidate identity/capability and branch capacity remain unverified at the exact model/job/appointment level.

All primary origin matrices are complete. The API returned baseline profile-model routes without observed traffic. Routes are optimised under the server's profile objective; choosing the lowest returned duration across destinations is not proof of a globally minimum-duration path. Matrix duration, not the OSRM route weight, is the reported time variable.

## Primary access contrasts

| Market | All-routed median A2000 minutes | Mapped-candidate minutes | Median paired A2000-minus-candidate minutes | Snap-screen retained origins | Screened paired gap minutes |
|---|---:|---:|---:|---:|---:|
| Surabaya | 7.78 | 4.24 | 3.47 | 59/81 | 3.62 |
| Medan | 8.21 | 3.79 | 3.93 | 78/81 | 4.09 |
| Bandung | 8.98 | 3.30 | 5.18 | 78/81 | 5.20 |
| Palembang | 10.32 | 5.59 | 3.32 | 69/81 | 3.43 |

The screen removes OD pairs with either endpoint more than 250 metres from its returned road-snap location. It is an analyst diagnostic, not field confirmation. In Surabaya it removes 22 of 81 origins from both main nearest-provider comparisons. A rectangular origin sample can include water, inaccessible land and disconnected spaces. Screened and unscreened denominators must remain visible; do not interpret these origins as population weights or Toyota owners.

The mapped candidate advantage remains positive under each reported descriptive sensitivity, but its magnitude depends strongly on which candidates count. Raising the source confidence threshold to0.9 reduces median paired gaps to2.26,2.04,2.96,1.50 minutes in Surabaya,Medan,Bandung,Palembang. Requiring an explicit car/mobil name reduces them to1.55,1.65,3.35,2.55 minutes. Neither filter verifies job suitability. This is evidence against presenting a single convenient gap as universal or causal.

Nested25 and central49 are subsets of the original81 origins, not newly sampled grids, shifted grids, additional observations or validation cohorts. Sensitivities are in `output/candidate_sensitivity_summary.csv`; all individual origin recalculations are retained.

## Why the commercial inference remains open

A nearer mapped generic repair provider is not established to offer the selected Toyota oil or brake job today. The contrast identifies a convenience hypothesis and potential locations for further evidence. It does not establish that owners currently use those garages, that travel causes switching, that an owner values a few modelled minutes, or that the destination can take a paid job. An apparently favourable branch catchment does not identify installed customer base or available bays.

The primary inventory's general repair categories also omit some legitimate oil-service channels. A separately sourced official Shop&Drive and documented DokterMobil scenario is therefore acquired in `supplement/`, together with selected other authorised Toyota providers. This is a challenge to the completeness of the generic-pool model, not an independent population sample. Source records may overlap across scenarios. The combined nearest-channel calculation must not be described as an exhaustive Toyota or workshop network.

## Branch-level interpretation

`output/branch_influence.csv` has all27 Auto2000 rows in two snap scenarios. It reports nearest-origin assignments,20minute access and leave-one-out effects. `output/focal12_branches.csv` selects three per market by nearest screened grid origins. Ties use the maximum access increase if omitted. These finite-grid catchments are not actual trade areas, throughput, closure economics or revenue contributions. Leave-one-out is a geographic sensitivity only.

## Validation

`output/QA_RECEIPT.json` contains24 arithmetic, network-integrity and geometry checks, all passing. These checks independently constrain impossible distances and monotonic relationships but do not establish field truth. Independent human/customer validation was not performed.

## Named advertised oil-channel challenge

The supplementary run adds all67 official Shop&Drive coordinate candidates within the four expanded windows (28Surabaya,8Medan,22Bandung,9Palembang), three locally oil-advertised DokterMobil outlets with separately identified matched coordinates, and three selected other authorised Toyota destinations. These73 scenario endpoints generate5,913 OD calculations at the same324 origins. They are not73 newly verified independent garages; cross-scenario overlap is possible. Combining primary and supplementary calculations gives82,134 OD comparisons, not that many observations or trips.

The headline named oil-channel comparator is the minimum returned time to the collected OtoXpert or Shop&Drive destinations. DokterMobil is reported separately rather than silently changing this definition. Exact Toyota model/parts/job bundle, current price, stock, service slot and physical entrance remain unconfirmed.

| Market | Screened A2000 median minutes | Screened S&D median minutes | Screened OtoXpert+S&D median minutes | Median paired A2000-minus-OtoXpert/S&D minutes |
|---|---:|---:|---:|---:|
| Surabaya | 6.74 | 5.41 | 5.41 | 0.97 |
| Medan | 8.18 | 7.35 | 7.17 | 0.35 |
| Bandung | 8.88 | 5.62 | 5.62 | 2.64 |
| Palembang | 9.23 | 7.25 | 6.97 | 2.64 |

The smaller named-channel contrast challenges a generic-map narrative that Auto2000 faces a uniformly large convenience penalty. It does not establish negligible inconvenience or equivalent service; there is no validated customer tolerance for these modelled minutes. It also shows why a category-driven generic garage search can miss a relevant oil-service chain that a map classifies as auto parts retail. The primary candidate pool remains useful as a sensitivity scenario rather than a complete service market.

`supplement/combined_market_summary.csv` also shows the minimum to collected Auto2000 and selected other authorised Toyota destinations. The other-authorised sample is intentionally incomplete, so this is not an exhaustive Toyota-network map or a Toyota-wide sales/profit analysis. OtoXpert operators differ, and neither channel routing nor corporate affiliation identifies whose contribution margin a completed job would generate.

Supplement QA:8checks pass, including5,913expected rows, uniqueness, complete acquisition, nonnegative values and correct minimum aggregation. Network and directory correctness remain outside those checks.
