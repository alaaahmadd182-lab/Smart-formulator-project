"""
Step 8 runner — SAE-grade compatibility mapping and candidate pair generation.

Usage:
    python analysis/association_mining/run_compatibility.py
    python analysis/association_mining/run_compatibility.py \\
        --input  analysis/association_mining/outputs \\
        --output analysis/association_mining/outputs

Reads:
    <input>/bo_ml.csv
    <input>/ap_ml.csv
    <input>/bo_clusters.csv
    <input>/ap_clusters.csv
    <input>/treat_rate.csv

Writes:
    <output>/bo_sae.csv               Base oils with inferred SAE high-temp grade
    <output>/formulation_candidates.csv  All (bo, ap) pairs sharing a SAE grade
    <output>/compatibility_matrix.csv    (ht_grade, bo_cluster, ap_cluster) counts
    <output>/compatibility_log.txt       Run summary

Does not modify any source file or extracted CSV.
"""

import argparse
import collections
import csv
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from analysis.association_mining.sae_grader import (
    kv100_to_ht_grade,
    parse_package_ht_grades,
    treat_rate_ht_grade,
    ht_grade_overlap,
    HT_GRADES,
)

# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

def _load(path: pathlib.Path, encoding: str = "utf-8") -> list[dict]:
    with open(path, encoding=encoding, newline="") as fh:
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
# Data helpers
# ---------------------------------------------------------------------------

def _f(s) -> float | None:
    if s in (None, "", "None"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _index_by(rows: list[dict], key: str) -> dict[str, dict]:
    """Build {key_value: last_row} index — ignores rows where key is empty."""
    return {r[key]: r for r in rows if r.get(key)}


def _build_treat_rate_index(
    treat_rows: list[dict],
) -> dict[tuple[str, str], list[float]]:
    """Build {(product_key, ht_grade): [treat_rate_pct, ...]} from treat_rate.csv."""
    idx: dict[tuple[str, str], list[float]] = collections.defaultdict(list)
    for row in treat_rows:
        pk = row.get("product_key", "")
        ht = treat_rate_ht_grade(row.get("sae_grade", ""))
        tr = _f(row.get("treat_rate"))
        if pk and ht and tr is not None:
            idx[(pk, ht)].append(tr)
    return dict(idx)


# ---------------------------------------------------------------------------
# Base oil SAE rows
# ---------------------------------------------------------------------------

def build_bo_sae_rows(bo_rows: list[dict], cluster_idx: dict[str, dict]) -> list[dict]:
    """Add inferred SAE high-temp grade and cluster_id to each base oil row."""
    out = []
    for row in bo_rows:
        pk = row.get("product_key", "")
        kv = _f(row.get("kv100"))
        grade = kv100_to_ht_grade(kv) if kv is not None else None
        clust = cluster_idx.get(pk, {}).get("cluster_id", "")
        out.append({
            "product_key":  pk,
            "supplier":     row.get("supplier", ""),
            "product_id":   row.get("product_id", ""),
            "kv100":        kv if kv is not None else "",
            "kv40":         row.get("kv40", ""),
            "api_group":    row.get("api_group", ""),
            "api_group_ord": row.get("api_group_ord", ""),
            "ht_grade":     grade if grade is not None else "",
            "cluster_id":   clust,
        })
    return out


# ---------------------------------------------------------------------------
# Candidate pair generation
# ---------------------------------------------------------------------------

def build_candidates(
    bo_sae_rows:   list[dict],
    ap_rows:       list[dict],
    ap_cluster_idx: dict[str, dict],
    treat_idx:     dict[tuple[str, str], list[float]],
) -> list[dict]:
    """Cross-join base oils × additive packages on shared SAE high-temp grade."""
    candidates = []

    for ap in ap_rows:
        ap_pk    = ap.get("product_key", "")
        ap_grades = parse_package_ht_grades(ap.get("sae_grades_canon", ""))
        if not ap_grades:
            continue
        ap_clust = ap_cluster_idx.get(ap_pk, {}).get("cluster_id", "")

        for bo in bo_sae_rows:
            bo_grade = bo.get("ht_grade", "")
            if not bo_grade:
                continue
            bo_set = frozenset([bo_grade])
            overlap = ht_grade_overlap(bo_set, ap_grades)
            if not overlap:
                continue

            # Treat rate lookup: take median over all entries for this grade
            tr_vals: list[float] = []
            for g in overlap:
                tr_vals.extend(treat_idx.get((ap_pk, g), []))
            tr_median = ""
            tr_min    = ""
            tr_max    = ""
            if tr_vals:
                tr_vals_sorted = sorted(tr_vals)
                n = len(tr_vals_sorted)
                mid = n // 2
                tr_median = round(
                    tr_vals_sorted[mid] if n % 2 else
                    (tr_vals_sorted[mid - 1] + tr_vals_sorted[mid]) / 2,
                    2,
                )
                tr_min = round(min(tr_vals), 2)
                tr_max = round(max(tr_vals), 2)

            candidates.append({
                "bo_product_key":      bo.get("product_key", ""),
                "bo_supplier":         bo.get("supplier", ""),
                "bo_product_id":       bo.get("product_id", ""),
                "bo_cluster":          bo.get("cluster_id", ""),
                "bo_api_group":        bo.get("api_group", ""),
                "bo_kv100":            bo.get("kv100", ""),
                "bo_ht_grade":         bo_grade,
                "ap_product_key":      ap_pk,
                "ap_supplier":         ap.get("supplier", ""),
                "ap_product_id":       ap.get("product_id", ""),
                "ap_cluster":          ap_clust,
                "ap_package_type":     ap.get("package_type_canon", ""),
                "ap_tbn":              ap.get("tbn", ""),
                "shared_ht_grades":    ",".join(overlap),
                "n_shared_grades":     len(overlap),
                "treat_rate_pct_med":  tr_median,
                "treat_rate_pct_min":  tr_min,
                "treat_rate_pct_max":  tr_max,
            })

    return candidates


# ---------------------------------------------------------------------------
# Compatibility matrix
# ---------------------------------------------------------------------------

def build_compat_matrix(candidates: list[dict]) -> list[dict]:
    """Aggregate candidate pairs by (ht_grade, bo_cluster, ap_cluster)."""
    Cell = collections.namedtuple("Cell", ["bo_set", "ap_set", "count"])
    table: dict[tuple[str, str, str], Cell] = {}

    for c in candidates:
        for grade in c["shared_ht_grades"].split(","):
            key = (grade, str(c["bo_cluster"]), str(c["ap_cluster"]))
            if key not in table:
                table[key] = Cell(set(), set(), 0)
            cell = table[key]
            cell.bo_set.add(c["bo_product_key"])
            cell.ap_set.add(c["ap_product_key"])
            table[key] = Cell(cell.bo_set, cell.ap_set, cell.count + 1)

    rows = []
    for (grade, bo_cl, ap_cl), cell in sorted(table.items(),
                                               key=lambda kv: (int(kv[0][0]), kv[0][1], kv[0][2])):
        rows.append({
            "ht_grade":    grade,
            "bo_cluster":  bo_cl,
            "ap_cluster":  ap_cl,
            "n_bo":        len(cell.bo_set),
            "n_ap":        len(cell.ap_set),
            "n_pairs":     cell.count,
        })
    return rows


# ---------------------------------------------------------------------------
# Log helpers
# ---------------------------------------------------------------------------

def _grade_summary(bo_sae: list[dict], candidates: list[dict]) -> list[str]:
    from collections import Counter
    bo_grade_ctr = Counter(r["ht_grade"] for r in bo_sae if r["ht_grade"])
    no_grade = sum(1 for r in bo_sae if not r["ht_grade"])
    pair_grade_ctr: Counter = Counter()
    for c in candidates:
        for g in c["shared_ht_grades"].split(","):
            pair_grade_ctr[g] += 1

    lines = ["  base oil ht-grade distribution (from kv100):"]
    for g in HT_GRADES:
        cnt = bo_grade_ctr.get(g, 0)
        if cnt:
            lines.append(f"    SAE {g}: {cnt} base oils")
    lines.append(f"    no grade (kv100 missing or < 5.6): {no_grade}")
    lines.append("  candidate pairs by grade:")
    for g in HT_GRADES:
        cnt = pair_grade_ctr.get(g, 0)
        if cnt:
            lines.append(f"    SAE {g}: {cnt} pairs")
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline B SAE-grade compatibility runner"
    )
    parser.add_argument("--input",  default="analysis/association_mining/outputs")
    parser.add_argument("--output", default="analysis/association_mining/outputs")
    args = parser.parse_args(argv)

    in_dir  = pathlib.Path(args.input).resolve()
    out_dir = pathlib.Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for f in ("bo_ml.csv", "ap_ml.csv", "bo_clusters.csv",
              "ap_clusters.csv", "treat_rate.csv"):
        if not (in_dir / f).exists():
            sys.exit(f"ERROR: {in_dir / f} not found — run earlier pipeline steps first")

    print(f"Input:  {in_dir}")
    print(f"Output: {out_dir}")

    t0 = time.monotonic()

    bo_rows     = _load(in_dir / "bo_ml.csv")
    ap_rows     = _load(in_dir / "ap_ml.csv")
    bo_clusters = _load(in_dir / "bo_clusters.csv")
    ap_clusters = _load(in_dir / "ap_clusters.csv")
    treat_rows  = _load(in_dir / "treat_rate.csv")

    bo_cl_idx = _index_by(bo_clusters, "product_key")
    ap_cl_idx = _index_by(ap_clusters, "product_key")
    treat_idx = _build_treat_rate_index(treat_rows)

    print(f"Building base oil SAE grade table …")
    bo_sae = build_bo_sae_rows(bo_rows, bo_cl_idx)

    print(f"Building formulation candidates …")
    candidates = build_candidates(bo_sae, ap_rows, ap_cl_idx, treat_idx)

    compat_matrix = build_compat_matrix(candidates)
    elapsed = time.monotonic() - t0

    _write(out_dir / "bo_sae.csv",                  bo_sae)
    _write(out_dir / "formulation_candidates.csv",  candidates)
    _write(out_dir / "compatibility_matrix.csv",    compat_matrix)

    # Packages with no SAE grade data
    n_ap_no_grade = sum(
        1 for r in ap_rows if not parse_package_ht_grades(r.get("sae_grades_canon", ""))
    )
    n_ap_with_grade = len(ap_rows) - n_ap_no_grade
    n_with_tr = sum(1 for c in candidates if c["treat_rate_pct_med"] != "")

    log_lines = [
        f"Compatibility mapping completed in {elapsed:.2f}s",
        f"Input:  {in_dir}",
        f"Output: {out_dir}",
        "",
        f"=== Input ===",
        f"  base oils:          {len(bo_rows)}",
        f"  additive packages:  {len(ap_rows)}  ({n_ap_with_grade} with SAE grade data, {n_ap_no_grade} without)",
        f"  treat rate rows:    {len(treat_rows)}",
        "",
        f"=== Grade mapping ===",
        *_grade_summary(bo_sae, candidates),
        "",
        f"=== Candidates ===",
        f"  total pairs:        {len(candidates)}",
        f"  pairs with treat rate data: {n_with_tr}",
        f"  compatibility matrix rows:  {len(compat_matrix)}",
    ]
    log_text = "\n".join(log_lines)
    (out_dir / "compatibility_log.txt").write_text(log_text + "\n", encoding="utf-8")
    print(log_text)
    print(f"\nFiles written to {out_dir}")


if __name__ == "__main__":
    main()
