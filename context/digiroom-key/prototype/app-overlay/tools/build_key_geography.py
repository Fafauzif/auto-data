"""Build the competition map from the reviewed research checkout and Natural Earth 5.1.2.
Usage: python tools/build_key_geography.py AUTO_DATA NATURAL_EARTH_DIRECTORY
The basemap inputs are the four Natural Earth GeoJSON layers named in LAYERS.
"""
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
RESEARCH, ATLAS = map(Path, sys.argv[1:3])
OUTPUT = Path(__file__).resolve().parents[1] / "src/key/data"
BASE = RESEARCH / "archive/session_work_products/analysis_followup/geographic_source/Auto2000_Geographic_Study/workstreams"
LATEST = RESEARCH / "sources/geography_latest/Auto2000_Lanjutan/work/coordinates"
TABLES = RESEARCH / "analysis/geography/tables"
MARKETS = {
    "Bandung": (107.34, -7.20, 107.93, -6.62),
    "Surabaya": (112.42, -7.56, 113.00, -6.98),
    "Medan": (98.37, 3.27, 98.98, 3.96),
    "Palembang": (104.43, -3.26, 105.02, -2.69),
}
LAYERS = {
    "land": "land",
    "urban_areas": "urban",
    "rivers_lake_centerlines": "water",
    "admin_1_states_provinces_lines": "boundary",
}
def read(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))
def output(name, value):
    (OUTPUT / name).write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
def coord(row):
    return [round(float(row["latitude"]), 7), round(float(row["longitude"]), 7)]
def key(row):
    return (row["market"], row["origin_id"])
def main():
    centers = {key(row): coord(row) for row in read(BASE / "routing/output/origins.csv")}
    operators = {"otoxpert:" + row["provider_id"]: row for row in read(BASE / "context/otoxpert_official_inventory.csv")}
    directory = {r["name"].casefold(): r for r in read(BASE / "branches/official_branches_unique.csv")}
    portfolio = {r["branch_id"]: r for r in read(TABLES / "branch_portfolio.csv")}
    counts = {r["market"]: r for r in read(TABLES / "raw_recomputed_markets.csv")}
    model = read(TABLES / "raw_recomputed_origins.csv")
    corrections = [dict(row, kind="auto2000") for row in read(LATEST / "corrected_endpoints.csv")]
    supplemental = read(BASE / "routing/inputs/supplement_destinations.csv")
    markets = {}
    for market in MARKETS:
        inputs = read(BASE / "routing/inputs" / (market.lower() + "_destinations.csv"))
        outlets = {}
        for row in inputs + supplemental + corrections:
            if row["market"] != market or row["kind"] not in {"auto2000", "otoxpert", "shopanddrive"}:
                continue
            destination = row["destination_id"]
            operator = operators.get(destination, {})
            kind = "dealer" if row["kind"] == "auto2000" else "owned" if operator.get("auto2000_operator", "").lower() == "true" else "comparison"
            branch = portfolio.get(destination, {})
            official = directory.get(row["name"].casefold(), {})
            if destination == "auto2000:suci_corrected":
                official = {"directory_url": "https://auto2000.co.id/dealer-toyota/bandung/auto2000bandungsuci"}
            outlets[destination] = {
                "id": destination, "name": row["name"].split(" - Dealer")[0].replace("Soekarno - Hatta", "Soekarno-Hatta"),
                "position": coord(row), "kind": kind, "oilComparator": row["kind"] != "auto2000",
                "operator": "Auto2000" if kind == "dealer" else operator.get("operator", "Shop & Drive"),
                "url": official.get("directory_url") or row["source_url"], "hours": operator.get("published_hours", ""),
                "residual": int(branch.get("oil_gap_gt5_after_owned_network_n", 0)),
            }
        origins = []
        for row in model:
            if row["market"] != market:
                continue
            destination_ids = [row["assigned_branch_id"], row["owned_destination_id"], row["oil_destination_id"]]
            assert all(destination in outlets for destination in destination_ids), (market, destination_ids)
            origins.append({
                "id": row["origin_id"], "position": centers[key(row)], "dealer": destination_ids[0],
                "owned": destination_ids[1], "comparator": destination_ids[2], "ties": row["tie_ids"].split(";"),
                "dealerSeconds": float(row["auto_seconds"]), "ownedSeconds": float(row["owned_seconds"]), "comparatorSeconds": float(row["oil_seconds"]),
                "before": float(row["oil_gap_min"]), "after": float(row["owned_gap_min"]),
            })
        expected = counts[market]
        assert [len(origins), sum(o["before"] > 5 for o in origins), sum(o["after"] > 5 for o in origins)] == [
            int(expected[k]) for k in ("paired_origins_n", "oil_tail_before_n", "oil_tail_after_n")
        ]
        markets[market] = {"origins": origins, "outlets": list(outlets.values())}
    assert sum(o["after"] > 5 and "Soekarno-Hatta" in next(d["name"] for d in markets["Bandung"]["outlets"] if d["id"] == o["dealer"]) for o in markets["Bandung"]["origins"]) == 8
    revision = subprocess.check_output(["git", "-C", str(RESEARCH), "rev-parse", "HEAD"], text=True).strip()
    output("geo-v1.json", {"version": 1, "revision": revision, "cutoff": "2026-11-14", "markets": markets})
    fallback = {}
    with tempfile.TemporaryDirectory() as temp:
        clipped = Path(temp) / "clip.geojson"
        for market, bbox in MARKETS.items():
            features = []
            for filename, category in LAYERS.items():
                clipped.unlink(missing_ok=True)
                subprocess.run(["ogr2ogr", "-overwrite", "-f", "GeoJSON", str(clipped), str(ATLAS / (filename + ".geojson")), "-spat", *map(str, bbox), "-clipsrc", *map(str, bbox), "-lco", "COORDINATE_PRECISION=5"], check=True)
                for feature in json.loads(clipped.read_text())["features"]:
                    features.append({"type": "Feature", "properties": {"category": category}, "geometry": feature["geometry"]})
            fallback[market] = {"type": "FeatureCollection", "features": features}
    output("atlas-v1.json", fallback)
if __name__ == "__main__":
    main()
