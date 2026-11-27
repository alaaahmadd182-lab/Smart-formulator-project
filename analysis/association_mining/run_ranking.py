"""
Step 9 runner — score and rank formulation candidates.

Usage:
    python analysis/association_mining/run_ranking.py
    python analysis/association_mining/run_ranking.py \\
        --input  analysis/association_mining/outputs \\
        --output analysis/association_mining/outputs

Reads:
    <input>/formulation_candidates.csv
    <input>/bo_ml.csv
    <input>/ap_ml.csv

Writes:
    <output>/formulation_ranked.csv    All pairs scored and sorted (best first)
    <output>/ranking_log.txt           Score distribution and top-10 pairs

Does not modify any source file or extracted CSV.
"""

import argparse
import collections
import csv
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from analysis.association_mining.scorer import (
    score_pair,
    WEIGHTS,
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
# Log helpers
# ---------------------------------------------------------------------------

def _score_distribution(rows: list[dict]) -> list[str]:
    """Bucket scores into 10-point bands and return summary lines."""
    bands = collections.Counter()
    for r in rows:
        try:
            s = float(r["score"])
        except (ValueError, KeyError):
            continue
        band = int(s // 10) * 10
        bands[band] += 1

    lines = ["  score distribution:"]
    for lo in range(0, 100, 10):
        hi = lo + 10
        label = f"  {lo:>3}-{hi:<3}"
        lines.append(f"    {label}: {bands.get(lo, 0):>4} pairs")
    return lines


def _top_n(rows: list[dict], n: int = 10) -> list[str]:
    lines = [f"  top {n} candidates:"]
    for i, r in enumerate(rows[:n], 1):
        lines.append(
            f"    {i:>2}. score={r['score']:>5}  "
            f"bo={r['bo_product_id'][:30]:<30}  "
            f"ap={r['ap_product_id'][:30]:<30}  "
            f"grade={r['bo_ht_grade']}  tr={r['treat_rate_pct_med']}"
        )
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline B formulation candidate ranking runner"
    )
    parser.add_argument("--input",  default="analysis/association_mining/outputs")
    parser.add_argument("--output", default="analysis/association_mining/outputs")
    args = parser.parse_args(argv)

    in_dir  = pathlib.Path(args.input).resolve()
    out_dir = pathlib.Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for f in ("formulation_candidates.csv", "bo_ml.csv", "ap_ml.csv"):
        if not (in_dir / f).exists():
            sys.exit(f"ERROR: {in_dir / f} not found — run earlier pipeline steps first")

    print(f"Input:  {in_dir}")
    print(f"Output: {out_dir}")

    t0 = time.monotonic()

    candidates = _load(in_dir / "formulation_candidates.csv")
    bo_rows    = _load(in_dir / "bo_ml.csv")
    ap_rows    = _load(in_dir / "ap_ml.csv")

    # Index ml rows by product_key for fast lookup
    bo_idx = {r["product_key"]: r for r in bo_rows if r.get("product_key")}
    ap_idx = {r["product_key"]: r for r in ap_rows if r.get("product_key")}

    print(f"Scoring {len(candidates)} candidate pairs …")
    ranked: list[dict] = []
    for cand in candidates:
        bo_row = bo_idx.get(cand.get("bo_product_key", ""), {})
        ap_row = ap_idx.get(cand.get("ap_product_key", ""), {})
        scores = score_pair(bo_row, ap_row, cand)
        ranked.append({**cand, **scores})

    ranked.sort(key=lambda r: float(r["score"]), reverse=True)
    elapsed = time.monotonic() - t0

    _write(out_dir / "formulation_ranked.csv", ranked)

    # Summary stats
    scores = [float(r["score"]) for r in ranked]
    mean_s = sum(scores) / len(scores) if scores else 0.0
    median_s = sorted(scores)[len(scores) // 2] if scores else 0.0

    log_lines = [
        f"Ranking completed in {elapsed:.2f}s",
        f"Input:  {in_dir}",
        f"Output: {out_dir}",
        "",
        f"=== Score weights ===",
        *[f"  {k:<14} {v:.0%}" for k, v in WEIGHTS.items()],
        "",
        f"=== Score summary ({len(ranked)} pairs) ===",
        f"  min:    {min(scores):.1f}",
        f"  max:    {max(scores):.1f}",
        f"  mean:   {mean_s:.1f}",
        f"  median: {median_s:.1f}",
        *_score_distribution(ranked),
        "",
        *_top_n(ranked, 10),
    ]
    log_text = "\n".join(log_lines)
    (out_dir / "ranking_log.txt").write_text(log_text + "\n", encoding="utf-8")
    print(log_text)
    print(f"\nformulation_ranked.csv written to {out_dir}")


if __name__ == "__main__":
    main()
