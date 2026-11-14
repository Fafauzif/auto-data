#!/usr/bin/env python3
"""Independent standard-library audit of the 14 Nov corrected geographic release.

Reads preserved OD records, official OtoXpert operator labels and the published
29-endpoint decision table. Writes fresh origin and branch checks without changing
the release or using any network service. --source-root is Auto2000_Lanjutan.
"""
import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def read(p):
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(p, rows):
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def audit(root, out):
    out.mkdir(parents=True, exist_ok=True)
    baseline = root / "extracted/baseline/Auto2000_Geographic_Study"
    main = read(baseline / "workstreams/routing/output/od_pairs.csv")
    supplement = read(baseline / "workstreams/routing/supplement/supplement_od_pairs.csv")
    corrected = [r for r in read(root / "work/coordinates/corrected_endpoint_od.csv") if r["direction"] == "outbound"]
    operators = read(baseline / "workstreams/context/otoxpert_official_inventory.csv")
    owned = {"otoxpert:" + r["provider_id"] for r in operators if r["auto2000_operator"].lower() == "true"}
    decisions = read(root / "output/tables/branch_decision_table_29.csv")
    baseline_groups = defaultdict(list)
    groups = defaultdict(list)
    for r in main + supplement + corrected:
        if not r.get("duration_seconds"):
            continue
        if float(r["origin_snap_metres"]) > 250 or float(r["destination_snap_metres"]) > 250:
            continue
        r = dict(r, seconds=float(r["duration_seconds"]))
        key = (r["market"], r["origin_id"])
        groups[key].append(r)
    for r in main + supplement:
        if r.get("duration_seconds") and float(r["origin_snap_metres"]) <= 250 and float(r["destination_snap_metres"]) <= 250:
            baseline_groups[(r["market"], r["origin_id"])].append(dict(r, seconds=float(r["duration_seconds"])))
    origins = []
    for (market, oid), records in groups.items():
        auto = [r for r in records if r["kind"] == "auto2000"]
        oil = [r for r in records if r["kind"] in {"otoxpert", "shopanddrive"}]
        own = [r for r in records if r["kind"] == "auto2000" or r["destination_id"] in owned]
        generic = [r for r in records if r["kind"] == "independent"]
        if not auto or not oil:
            continue
        a = min(auto, key=lambda r: r["seconds"])
        o = min(oil, key=lambda r: r["seconds"])
        w = min(own, key=lambda r: r["seconds"])
        seconds = sorted(r["seconds"] for r in auto)
        old = min((r for r in baseline_groups[(market, oid)] if r["kind"] == "auto2000"), key=lambda r: r["seconds"])
        origins.append({"market": market, "origin_id": oid, "assigned_branch_id": a["destination_id"],
                        "assigned_branch_name": a["destination_name"], "old_branch_id": old["destination_id"],
                        "auto_seconds": a["seconds"], "oil_seconds": o["seconds"], "owned_seconds": w["seconds"],
                        "oil_gap_min": round((a["seconds"]-o["seconds"])/60,12),
                        "owned_gap_min": round((w["seconds"]-o["seconds"])/60,12),
                        "own_network_saving_min": (a["seconds"]-w["seconds"])/60,
                        "generic_gap_min": (a["seconds"]-min(r["seconds"] for r in generic))/60 if generic else None,
                        "second_branch_penalty_min": (seconds[1]-seconds[0])/60 if len(seconds)>1 else None,
                        "tie_ids": ";".join(r["destination_id"] for r in auto if abs(r["seconds"]-a["seconds"])<1e-7),
                        "second_seconds": seconds[1] if len(seconds)>1 else None,
                        "oil_destination_id": o["destination_id"], "owned_destination_id": w["destination_id"]})
    errors = []
    branch_checks = []
    for d in decisions:
        rr = [r for r in origins if r["market"] == d["market"] and r["assigned_branch_id"] == d["branch_id"]]
        obs = {"nearest_origins_n": len(rr),
               "oil_gap_gt5_n": sum(r["oil_gap_min"] > 5 for r in rr),
               "owned_network_gap_gt5_n": sum(r["owned_gap_min"] > 5 for r in rr),
               "median_oil_gap_min": statistics.median(r["oil_gap_min"] for r in rr) if rr else None,
               "median_owned_network_gap_min": statistics.median(r["owned_gap_min"] for r in rr) if rr else None,
               "second_branch_penalty_median_min": statistics.median(r["second_branch_penalty_min"] for r in rr) if rr else None}
        for threshold in [10,15,20,30]:
            obs[f"grid_loses_{threshold}min_without_branch_n"] = sum(r["auto_seconds"]<=threshold*60 and (r["second_seconds"] is None or r["second_seconds"]>threshold*60) for r in rr)
        for field, val in obs.items():
            expected = float(d[field]) if d.get(field) else None
            okay = val is None and expected is None or val is not None and expected is not None and abs(val-expected)<1e-9
            branch_checks.append({"market": d["market"], "branch_id": d["branch_id"], "branch_name": d["branch_name"], "field": field, "recomputed": val, "published": expected, "matches": okay})
            if not okay:
                errors.append(branch_checks[-1])
    market_checks = []
    for market in ["Surabaya", "Medan", "Bandung", "Palembang"]:
        rr = [r for r in origins if r["market"] == market]
        market_checks.append({"market": market, "paired_origins_n": len(rr),
                              "median_generic_gap_min": statistics.median(r["generic_gap_min"] for r in rr),
                              "median_oil_gap_min": statistics.median(r["oil_gap_min"] for r in rr),
                              "median_owned_gap_min": statistics.median(r["owned_gap_min"] for r in rr),
                              "oil_tail_before_n": sum(r["oil_gap_min"]>5 for r in rr),
                              "oil_tail_after_n": sum(r["owned_gap_min"]>5 for r in rr),
                              "changed_nearest_branch_n": sum(r["assigned_branch_id"]!=r["old_branch_id"] for r in rr)})
    for filename, rows in [("raw_recomputed_origins.csv",origins), ("raw_recomputed_markets.csv",market_checks), ("raw_branch_checks.csv",branch_checks)]:
        write(out / filename, rows)
    raw_rows = main + supplement + corrected
    pair_keys = {(r["market"], r["origin_id"], r["destination_id"]) for r in raw_rows}
    origin_keys = {(r["market"], r["origin_id"]) for r in raw_rows}
    result = {"source_root": str(root), "raw_OD_rows": {"main": len(main), "supplement": len(supplement), "corrected_outbound": len(corrected)},
              "raw_unique_outbound_pair_keys": len(pair_keys), "raw_unique_market_origin_keys": len(origin_keys),
              "paired_strict_origins": len(origins), "branch_checks": len(branch_checks), "errors_n": len(errors), "errors": errors,
              "market_results": market_checks, "pass": not errors,
              "commercial_scope": "Model geometry only; OtoXpert operators from official directory; advertised job fit, no actual slot, quote, demand or GP claim."}
    (out / "raw_independent_audit.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    repo = Path(__file__).resolve().parents[3]
    p.add_argument("--source-root", type=Path, default=repo/"sources/geography/latest/Auto2000_Lanjutan")
    p.add_argument("--output", type=Path, default=repo/"analysis/geography/tables")
    a = p.parse_args(); audit(a.source_root, a.output)
