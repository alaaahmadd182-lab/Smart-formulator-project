"""
Step 6 runner — apply feature engineering transforms and write ML-ready CSVs.

Usage:
    python analysis/association_mining/run_feature_engineering.py
    python analysis/association_mining/run_feature_engineering.py \\
        --input  analysis/association_mining/outputs \\
        --output analysis/association_mining/outputs

Reads:
    <input>/bo_features.csv
    <input>/ap_features.csv

Writes:
    <output>/bo_ml.csv       Base oil features with engineering columns added
    <output>/ap_ml.csv       Additive package features with engineering columns added
    <output>/feature_log.txt Run summary

Does not modify any source file or extracted CSV.
"""

import argparse
import collections
import csv
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from analysis.association_mining.feature_engineer import (
    engineer_base_oils,
    engineer_packages,
)


# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

def _load(path: pathlib.Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _write(path: pathlib.Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("(no data)\n", encoding="utf-8")
        return
    fieldnames: list[str] = list(rows[0].keys())
    seen = set(fieldnames)
    for r in rows[1:]:
        for k in r:
            if k not in seen:
                fieldnames.append(k)
                seen.add(k)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames,
                           extrasaction="ignore", restval="")
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------------------
# Log helpers
# ---------------------------------------------------------------------------

def _f(s) -> float | None:
    if s in (None, "", "None"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _b(s) -> bool:
    return str(s).lower() in ("true", "1")


def _summarise_bo(rows: list[dict]) -> list[str]:
    n = len(rows)
    n_density_ok   = sum(1 for r in rows if _f(r.get("density_kg_m3")) is not None)
    n_density_conv = sum(1 for r in rows if _b(r.get("density_conv_applied")))
    n_api_known    = sum(1 for r in rows if _b(r.get("api_group_known")))
    n_sulfur_wt    = sum(1 for r in rows if _f(r.get("sulfur_wt_pct")) is not None)
    n_vi_point     = sum(1 for r in rows if _f(r.get("vi_point")) is not None)
    n_vi_lb        = sum(1 for r in rows if _f(r.get("vi_lb_bound")) is not None)
    n_pp_max       = sum(1 for r in rows if _b(r.get("pour_point_is_max")))
    return [
        f"  density_kg_m3 filled:    {n_density_ok}/{n}  ({n_density_conv} converted, {n_density_ok - n_density_conv} already kg/m³)",
        f"  api_group_ord filled:    {n_api_known}/{n}  ({n - n_api_known} unknown/missing)",
        f"  sulfur_wt_pct filled:    {n_sulfur_wt}/{n}",
        f"  vi_point filled:         {n_vi_point}/{n}",
        f"  vi_lb_bound filled:      {n_vi_lb}/{n}  (minimum-bound entries)",
        f"  pour_point_is_max=True:  {n_pp_max}/{n}",
    ]


def _summarise_ap(rows: list[dict]) -> list[str]:
    n = len(rows)
    n_density_ok   = sum(1 for r in rows if _f(r.get("density_kg_m3")) is not None)
    n_density_conv = sum(1 for r in rows if _b(r.get("density_conv_applied")))
    n_mo_ok        = sum(1 for r in rows if _f(r.get("mo_wt_pct")) is not None)
    n_mo_conv      = sum(1 for r in rows if _b(r.get("mo_conv_applied")))
    n_zn_p        = sum(1 for r in rows if _f(r.get("zn_p_sum")) is not None)
    n_ca_tbn      = sum(1 for r in rows if _f(r.get("ca_tbn_ratio")) is not None)
    pkg_ctr = collections.Counter(r.get("package_type_canon", "missing") for r in rows)
    pkg_lines = [f"    {k}: {v}" for k, v in pkg_ctr.most_common()]
    return [
        f"  density_kg_m3 filled:    {n_density_ok}/{n}  ({n_density_conv} converted)",
        f"  mo_wt_pct filled:        {n_mo_ok}/{n}  ({n_mo_conv} converted from ppm)",
        f"  zn_p_sum filled:         {n_zn_p}/{n}",
        f"  ca_tbn_ratio filled:     {n_ca_tbn}/{n}",
        "  package_type_canon dist:",
        *pkg_lines,
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline B feature engineering runner"
    )
    parser.add_argument("--input",  default="analysis/association_mining/outputs")
    parser.add_argument("--output", default="analysis/association_mining/outputs")
    args = parser.parse_args(argv)

    in_dir  = pathlib.Path(args.input).resolve()
    out_dir = pathlib.Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for f in ("bo_features.csv", "ap_features.csv"):
        if not (in_dir / f).exists():
            sys.exit(f"ERROR: {in_dir / f} not found — run run_extraction.py first")

    print(f"Input:  {in_dir}")
    print(f"Output: {out_dir}")

    t0 = time.monotonic()
    bo_raw = _load(in_dir / "bo_features.csv")
    ap_raw = _load(in_dir / "ap_features.csv")

    bo_ml = engineer_base_oils(bo_raw)
    ap_ml = engineer_packages(ap_raw)

    _write(out_dir / "bo_ml.csv", bo_ml)
    _write(out_dir / "ap_ml.csv", ap_ml)
    elapsed = time.monotonic() - t0

    log_lines = [
        f"Feature engineering completed in {elapsed:.2f}s",
        f"Input:  {in_dir}",
        f"Output: {out_dir}",
        "",
        f"bo_ml.csv: {len(bo_ml)} rows, {len(bo_ml[0]) if bo_ml else 0} columns",
        "--- Base oil engineering summary ---",
        *_summarise_bo(bo_ml),
        "",
        f"ap_ml.csv: {len(ap_ml)} rows, {len(ap_ml[0]) if ap_ml else 0} columns",
        "--- Additive package engineering summary ---",
        *_summarise_ap(ap_ml),
    ]
    log_text = "\n".join(log_lines)
    (out_dir / "feature_log.txt").write_text(log_text + "\n", encoding="utf-8")
    print(log_text)
    print(f"\nFiles written to {out_dir}")


if __name__ == "__main__":
    main()
