# Public EV charging stations in Indonesia (SPKLU) - version 2.0

A geocoded inventory of Indonesia's public EV charging stations. Station records
were collected from the national charging map petaspklu.id on 16 June 2026 and
enriched with official administrative codes, provincial population and GDP, and
road-network spatial indicators.

Version 2.0 supersedes version 1.0. It resolves duplicate map entries, so the
station table describes 2,454 unique physical sites rather than 3,029 raw
records. It also adds nearest-neighbour road distance and multi-radius station
density for every site.

## Reading order
`spklu_data_dictionary.csv` defines every field in every file.
`data/spklu_stations.csv` is the primary table with one row per unique station.
`data/spklu_chargers.csv` breaks each station into its charger boxes and joins
on `station_id`.

## Contents

| Folder | File | Rows | Role |
|---|---|---|---|
| data/ | spklu_stations.csv | 2,454 | Primary table, one row per unique station after duplicate resolution (44 columns) |
| data/ | spklu_chargers.csv | 3,767 | One row per charger box (join on station_id) |
| reference/ | spklu_province_coverage.csv | 34 | Province coverage metrics |
| reference/ | spklu_province_indicators.csv | 34 | Population, GDP, EV inputs |
| reference/ | spklu_regency_codes.csv | 375 | Regency BPS-code crosswalk |
| (root) | spklu_data_dictionary.csv | 89 | Field-level definitions for every data file |
| (root) | PROCESSING_LOG.md | - | Method notes, limitations, and per-step provenance |

## Headline figures
- 2,454 unique stations across 34 provinces, consolidated from 3,029 raw records
- 3,767 charger boxes, 7,593 charger units, 4,665 connectors
- 89,871 kW of installed fast-charging-capable power
- Operator split: PLN / SPKLU network 1,607, independent CPO 470, automaker dealership 351, unknown 26

## Known constraints
The source publishes active stations only. This release is a single snapshot and
records no closures or growth over time.

`provider_type` and `location_type` are keyword classifications derived from
station names rather than verified operator records.

Population dates from 2020, GDP from 2025, and the station snapshot from 2026.

## Sources and attribution

**Charging-station records.** Peta SPKLU national public EV charging map,
petaspklu.id, JSON endpoint `/api/v1/spklu/all`, accessed 16 June 2026. Operated
by Solopos with underlying data from PT PLN (Persero). Served publicly without
authentication.

**Administrative codes.** Peraturan Menteri Dalam Negeri (Permendagri) No. 72
Tahun 2019 (Kode dan Data Wilayah Administrasi Pemerintahan), Kementerian Dalam
Negeri, Jakarta, 2019. Supplemented by the open emsifa/api-wilayah-indonesia
regency master (https://github.com/emsifa/api-wilayah-indonesia). Codes follow
the pre-2022 34-province structure.

**Population.** Badan Pusat Statistik, Hasil Sensus Penduduk 2020 (SP2020),
Jakarta, 2021. Provincial values sum to the published national total of
270,203,917.

**Regional GDP.** Badan Pusat Statistik, Produk Domestik Regional Bruto
Provinsi-Provinsi di Indonesia, nominal PDRB ADHB 2025. The values in this
deposit come from a secondary compilation of these figures rather than the
primary BPS table.

**Road network and routing.** OpenStreetMap contributors, available under the
Open Database License (ODbL), https://www.openstreetmap.org/copyright. Distances
were queried through the public Open Source Routing Machine (OSRM) demonstration
server using the Table service and driving profile. See D. Luxen, C. Vetter,
Real-time routing with OpenStreetMap data, ACM SIGSPATIAL 2011, pp. 513-516,
https://doi.org/10.1145/2093973.2094062.
