"""
Step 7 runner — compute pairwise similarity and cluster products.

Usage:
    python analysis/association_mining/run_similarity.py
    python analysis/association_mining/run_similarity.py \\
        --input  analysis/association_mining/outputs \\
        --output analysis/association_mining/outputs \\
        --top-n  50

Reads:
    <input>/bo_ml.csv
    <input>/ap_ml.csv

Writes:
    <output>/bo_clusters.csv      Base oil cluster assignments + key features
    <output>/ap_clusters.csv      Additive package cluster assignments + key features
    <output>/bo_top_pairs.csv     Top-N most similar base oil pairs
    <output>/ap_top_pairs.csv     Top-N most similar additive package pairs
    <output>/similarity_log.txt   Run summary with feature coverage and cluster stats

Does not modify any source file or extracted CSV.
"""

import argparse
import csv
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from analysis.association_mining.similarity import (
    BO_FEATURE_COLS,
    AP_FEATURE_COLS,
    feature_matrix,
    normalise,
    pairwise_cosine,
    top_pairs,
    kmeans,
    best_k,
    silhouette_score,
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
# Float helper
# ---------------------------------------------------------------------------

def _f(s) -> float | None:
    if s in (None, "", "None"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Cluster CSV builders
# ---------------------------------------------------------------------------

_BO_DISPLAY_COLS = (
    "product_key", "supplier", "product_id",
    "api_group", "kv40", "kv100",
    "vi_point", "vi_lb_bound",
    "density_kg_m3", "api_group_ord", "sulfur_wt_pct",
    "pour_point",
)

_AP_DISPLAY_COLS = (
    "product_key", "supplier", "product_id",
    "package_type_canon", "tbn", "sulfated_ash",
    "ca", "zn", "p", "density_kg_m3", "zn_p_sum",
)


def _build_cluster_rows(
    rows: list[dict],
    labels: list[int],
    sim: list[list[float | None]],
    display_cols: tuple[str, ...],
) -> list[dict]:
    """Build cluster CSV rows with cluster_id, nearest_neighbor, and display columns."""
    n = len(rows)
    out = []
    for i, (row, lbl) in enumerate(zip(rows, labels)):
        # nearest neighbour in full similarity matrix (excluding self)
        best_j, best_s = None, -2.0
        for j in range(n):
            if j == i:
                continue
            s = sim[i][j]
            if s is not None and s > best_s:
                best_j, best_s = j, s

        rec: dict = {"cluster_id": lbl}
        for col in display_cols:
            rec[col] = row.get(col, "")
        rec["nearest_neighbor"] = rows[best_j].get("product_key", "") if best_j is not None else ""
        rec["nearest_sim"] = round(best_s, 6) if best_j is not None else ""
        out.append(rec)
    return out


# ---------------------------------------------------------------------------
# Log helpers
# ---------------------------------------------------------------------------

def _feature_coverage(
    matrix: list[list[float | None]],
    cols: tuple[str, ...],
) -> list[str]:
    n = len(matrix)
    if n == 0:
        return []
    lines = []
    for j, col in enumerate(cols):
        present = sum(1 for row in matrix if row[j] is not None)
        lines.append(f"    {col:<20} {present:>4}/{n}  ({100*present/n:.0f}%)")
    return lines


def _cluster_stats(
    rows: list[dict],
    labels: list[int],
    sil: float,
    sil_scores: dict[int, float],
    chosen_k: int,
) -> list[str]:
    from collections import Counter
    ctr = Counter(labels)
    lines = [
        f"  chosen k = {chosen_k}  (silhouette = {sil:.4f})",
        f"  k candidates: " + ", ".join(f"k={k}->{s:.4f}" for k, s in sorted(sil_scores.items())),
        "  cluster sizes:",
    ]
    for lbl in sorted(ctr):
        lines.append(f"    cluster {lbl}: {ctr[lbl]} products")
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline B similarity and clustering runner"
    )
    parser.add_argument("--input",  default="analysis/association_mining/outputs")
    parser.add_argument("--output", default="analysis/association_mining/outputs")
    parser.add_argument("--top-n",  type=int, default=50,
                        help="Number of top similar pairs to write per product type")
    args = parser.parse_args(argv)

    in_dir  = pathlib.Path(args.input).resolve()
    out_dir = pathlib.Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for f in ("bo_ml.csv", "ap_ml.csv"):
        if not (in_dir / f).exists():
            sys.exit(f"ERROR: {in_dir / f} not found — run run_feature_engineering.py first")

    print(f"Input:  {in_dir}")
    print(f"Output: {out_dir}")

    t0 = time.monotonic()
    bo_rows = _load(in_dir / "bo_ml.csv")
    ap_rows = _load(in_dir / "ap_ml.csv")

    bo_ids = [r.get("product_key", str(i)) for i, r in enumerate(bo_rows)]
    ap_ids = [r.get("product_key", str(i)) for i, r in enumerate(ap_rows)]

    # --- Base oils ---
    print("Computing base oil similarity …")
    bo_mat_raw = feature_matrix(bo_rows, "bo")
    bo_norm_none, bo_norm_imp, bo_stats = normalise(bo_mat_raw)
    bo_sim = pairwise_cosine(bo_norm_none)
    bo_top = top_pairs(bo_sim, bo_ids, n=args.top_n)

    bo_k, bo_sil_map = best_k(bo_norm_imp, ks=(3, 4, 5, 6), seed=42)
    bo_labels = kmeans(bo_norm_imp, bo_k, seed=42)
    bo_sil = silhouette_score(bo_norm_imp, bo_labels)
    print(f"  base oils: k={bo_k}, silhouette={bo_sil:.4f}")

    # --- Additive packages ---
    print("Computing additive package similarity …")
    ap_mat_raw = feature_matrix(ap_rows, "ap")
    ap_norm_none, ap_norm_imp, ap_stats = normalise(ap_mat_raw)
    ap_sim = pairwise_cosine(ap_norm_none)
    ap_top = top_pairs(ap_sim, ap_ids, n=args.top_n)

    ap_k, ap_sil_map = best_k(ap_norm_imp, ks=(3, 4, 5), seed=42)
    ap_labels = kmeans(ap_norm_imp, ap_k, seed=42)
    ap_sil = silhouette_score(ap_norm_imp, ap_labels)
    print(f"  additive packages: k={ap_k}, silhouette={ap_sil:.4f}")

    elapsed = time.monotonic() - t0

    # --- Write outputs ---
    bo_cluster_rows = _build_cluster_rows(bo_rows, bo_labels, bo_sim, _BO_DISPLAY_COLS)
    ap_cluster_rows = _build_cluster_rows(ap_rows, ap_labels, ap_sim, _AP_DISPLAY_COLS)

    _write(out_dir / "bo_clusters.csv", bo_cluster_rows)
    _write(out_dir / "ap_clusters.csv", ap_cluster_rows)
    _write(out_dir / "bo_top_pairs.csv", bo_top)
    _write(out_dir / "ap_top_pairs.csv", ap_top)

    # --- Log ---
    log_lines = [
        f"Similarity and clustering completed in {elapsed:.2f}s",
        f"Input:  {in_dir}",
        f"Output: {out_dir}",
        "",
        f"=== Base oils ({len(bo_rows)} products) ===",
        f"Feature columns ({len(BO_FEATURE_COLS)}):",
        *_feature_coverage(bo_mat_raw, BO_FEATURE_COLS),
        "Clustering:",
        *_cluster_stats(bo_rows, bo_labels, bo_sil, bo_sil_map, bo_k),
        f"Top {len(bo_top)} similar pairs written to bo_top_pairs.csv",
        "",
        f"=== Additive packages ({len(ap_rows)} products) ===",
        f"Feature columns ({len(AP_FEATURE_COLS)}):",
        *_feature_coverage(ap_mat_raw, AP_FEATURE_COLS),
        "Clustering:",
        *_cluster_stats(ap_rows, ap_labels, ap_sil, ap_sil_map, ap_k),
        f"Top {len(ap_top)} similar pairs written to ap_top_pairs.csv",
    ]
    log_text = "\n".join(log_lines)
    (out_dir / "similarity_log.txt").write_text(log_text + "\n", encoding="utf-8")
    print(log_text)
    print(f"\nFiles written to {out_dir}")


if __name__ == "__main__":
    main()
