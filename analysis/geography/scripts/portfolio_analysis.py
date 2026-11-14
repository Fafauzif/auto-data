#!/usr/bin/env python3
"""Recompute geographic portfolio implications from the saved 29-endpoint table.

No network calls. Counts are analytic origins, never customers or inferred demand.
Run with --table PATH --output DIR. Source table is the 14 Nov corrected release.
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def run(table, output):
    output.mkdir(parents=True, exist_ok=True)
    with table.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    summary = defaultdict(lambda: {"endpoints_n": 0, "assigned_origins_n": 0,
                                  "oil_tail_before_owned_network_n": 0,
                                  "oil_tail_after_owned_network_n": 0,
                                  "unique_15min_service_origins_n": 0})
    decisions = []
    for r in rows:
        market = r["market"]
        n = int(r["nearest_origins_n"])
        tail = int(r["oil_gap_gt5_n"])
        own_tail = int(r["owned_network_gap_gt5_n"])
        protected = int(r["grid_loses_15min_without_branch_n"])
        d = summary[market]
        d["endpoints_n"] += 1
        d["assigned_origins_n"] += n
        d["oil_tail_before_owned_network_n"] += tail
        d["oil_tail_after_owned_network_n"] += own_tail
        d["unique_15min_service_origins_n"] += protected
        d["paired_origins_n"] = int(r["paired_market_n"])
        if "Sidoarjo" in r["branch_name"]:
            family = "Correct coordinate and retain southern routing; six of six targeted extension origins choose Sidoarjo"
        elif n == 0:
            family = "Boundary review; no demand inference"
        elif own_tail and protected:
            family = "Protect full-scope availability and test residual access"
        elif own_tail:
            family = "Residual job-specific access; one-visit/THS test before subsidy"
        elif protected:
            family = "Protect accepted slot and completion; use owned channels for eligible jobs"
        else:
            family = "Use existing operator/job routing and monitor completion"
        decisions.append({
            "market": market, "branch_id": r["branch_id"],
            "branch_name": r["branch_name"], "assigned_grid_origins_n": n,
            "oil_gap_gt5_before_owned_network_n": tail,
            "oil_gap_gt5_after_owned_network_n": own_tail,
            "origins_losing_15min_general_branch_access_if_removed_n": protected,
            "second_general_branch_penalty_median_min": r["second_branch_penalty_median_min"],
            "decision_family": family,
            "meaning": "Finite-grid network geometry; no customer, capacity, closure or uplift inference"
        })
    total_tail = sum(x["oil_tail_after_owned_network_n"] for x in summary.values())
    market_rows = []
    for market, d in summary.items():
        assert d["assigned_origins_n"] == d["paired_origins_n"], (market, d)
        d["removed_tail_n"] = d["oil_tail_before_owned_network_n"] - d["oil_tail_after_owned_network_n"]
        d["share_of_pooled_residual_model_origins"] = d["oil_tail_after_owned_network_n"] / total_tail if total_tail else 0
        market_rows.append({"market": market, **d})
    for name, data in [("branch_portfolio.csv", decisions), ("market_portfolio.csv", market_rows)]:
        with (output / name).open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    result = {"source": str(table), "source_endpoints_n": len(rows),
              "market_summaries": market_rows,
              "total_origin_comparisons": sum(x["paired_origins_n"] for x in summary.values()),
              "pooled_tail_before_n": sum(x["oil_tail_before_owned_network_n"] for x in summary.values()),
              "pooled_tail_after_n": total_tail,
              "warning": "Pooling describes allocation of this model's cells, not geographic demand or population shares.",
              "checks": {"origin_partition_matches_each_market": True,
                         "branches_n": len(rows), "network_tail_does_not_increase": all(int(r["owned_network_gap_gt5_n"]) <= int(r["oil_gap_gt5_n"]) for r in rows)}}
    (output / "portfolio_audit.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    repo = Path(__file__).resolve().parents[3]
    parser.add_argument("--table", type=Path, default=repo/"sources/geography/latest/Auto2000_Lanjutan/output/tables/branch_decision_table_29.csv")
    parser.add_argument("--output", type=Path, default=repo/"analysis/geography/tables")
    args = parser.parse_args()
    run(args.table, args.output)
