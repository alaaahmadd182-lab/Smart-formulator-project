"""
Step 4 runner — extract Products_json to structured CSV tables.

Usage:
    python analysis/association_mining/run_extraction.py
    python analysis/association_mining/run_extraction.py --input Products_json --output analysis/association_mining/outputs

Outputs (in --output directory):
    bo_features.csv      Base oil properties, one row per product
    ap_features.csv      Additive package properties, one row per product
    treat_rate.csv       Treat rate matrix, one row per (package × claim × grade)
    extraction_log.txt   Run summary and any warnings

Does not modify any source file.
"""

import argparse
import csv
import pathlib
import sys
import time
import warnings
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from analysis.association_mining.extractor import extract_all


def _write_csv(path: pathlib.Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("(no data)\n", encoding="utf-8")
        return
    # Collect all columns in first-row order, then add any extra from later rows
    fieldnames: list[str] = list(rows[0].keys())
    seen = set(fieldnames)
    for row in rows[1:]:
        for k in row:
            if k not in seen:
                fieldnames.append(k)
                seen.add(k)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore",
                                restval="")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Pipeline B structured table extractor")
    parser.add_argument("--input",  default="Products_json",
                        help="Path to Products_json directory")
    parser.add_argument("--output", default="analysis/association_mining/outputs",
                        help="Directory to write CSV files")
    args = parser.parse_args(argv)

    root    = pathlib.Path(args.input).resolve()
    out_dir = pathlib.Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not root.is_dir():
        sys.exit(f"ERROR: input directory not found: {root}")

    print(f"Input:  {root}")
    print(f"Output: {out_dir}")
    print("Extracting ...", flush=True)

    caught_warnings: list[str] = []
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        t0 = time.monotonic()
        tables = extract_all(root)
        elapsed = time.monotonic() - t0
        caught_warnings = [str(x.message) for x in w]

    bo_rows = tables["base_oil"]
    ap_rows = tables["additive_pkg"]
    tr_rows = tables["treat_rate"]

    _write_csv(out_dir / "bo_features.csv",  bo_rows)
    _write_csv(out_dir / "ap_features.csv",  ap_rows)
    _write_csv(out_dir / "treat_rate.csv",   tr_rows)

    # --- Summary log ---
    log_lines = [
        f"Extraction completed in {elapsed:.1f}s",
        f"Input:  {root}",
        f"Output: {out_dir}",
        "",
        f"base_oil rows:      {len(bo_rows)}",
        f"additive_pkg rows:  {len(ap_rows)}",
        f"treat_rate rows:    {len(tr_rows)}",
    ]

    if bo_rows:
        log_lines += ["", "--- Base oil column count ---",
                      f"  {len(bo_rows[0])} columns per row (sample: first row)"]
    if ap_rows:
        log_lines += ["", "--- Additive package column count ---",
                      f"  {len(ap_rows[0])} columns per row (sample: first row)"]

    # Spot-check: count non-null kv40 values
    if bo_rows:
        n_kv40 = sum(1 for r in bo_rows if r.get("kv40") is not None)
        n_vi   = sum(1 for r in bo_rows if r.get("vi") is not None)
        n_dens = sum(1 for r in bo_rows if r.get("density_t1") is not None)
        log_lines += ["", "--- Base oil coverage (non-null point values) ---",
                      f"  kv40:    {n_kv40}/{len(bo_rows)}",
                      f"  vi:      {n_vi}/{len(bo_rows)}",
                      f"  density: {n_dens}/{len(bo_rows)}"]

    if ap_rows:
        n_tbn  = sum(1 for r in ap_rows if r.get("tbn") is not None)
        n_ca   = sum(1 for r in ap_rows if r.get("ca") is not None)
        n_tr   = sum(1 for r in ap_rows if r.get("has_treat_rate_data"))
        log_lines += ["", "--- Additive package coverage (non-null point values) ---",
                      f"  tbn:               {n_tbn}/{len(ap_rows)}",
                      f"  ca:                {n_ca}/{len(ap_rows)}",
                      f"  has treat-rate:    {n_tr}/{len(ap_rows)}"]

    if caught_warnings:
        log_lines += ["", "--- Extraction warnings ---"]
        log_lines += [f"  {w}" for w in caught_warnings]

    log_text = "\n".join(log_lines)
    (out_dir / "extraction_log.txt").write_text(log_text + "\n", encoding="utf-8")

    print(log_text)
    print(f"\nFiles written to {out_dir}")


if __name__ == "__main__":
    main()
