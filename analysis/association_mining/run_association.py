"""
Step 10 runner — mine directed association rules from formulation candidates.

Usage:
    python analysis/association_mining/run_association.py
    python analysis/association_mining/run_association.py \\
        --input      analysis/association_mining/outputs \\
        --output     analysis/association_mining/outputs \\
        --min-sup    0.05 \\
        --min-conf   0.50 \\
        --min-score  0

Reads:
    <input>/formulation_ranked.csv

Writes:
    <output>/association_rules.csv    Rules sorted by lift desc
    <output>/association_log.txt      Summary with top rules printed

Does not modify any source file or extracted CSV.
"""

import argparse
import csv
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from analysis.association_mining.association_miner import (
    discretise_bo,
    discretise_ap,
    mine_rules,
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
    fieldnames = list(rows[0].keys())
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
# Rule serialisation
# ---------------------------------------------------------------------------

def _rule_to_row(rule: dict, rank: int) -> dict:
    ant = sorted(rule["antecedent"])
    con = sorted(rule["consequent"])
    return {
        "rank":       rank,
        "antecedent": " & ".join(ant),
        "consequent": " & ".join(con),
        "support":    f"{rule['support']:.1%}",
        "confidence": f"{rule['confidence']:.1%}",
        "lift":       f"{rule['lift']:.3f}",
        "count":      rule["count"],
        "count_ant":  rule["count_ant"],
        "support_raw":    rule["support"],
        "confidence_raw": rule["confidence"],
        "lift_raw":       rule["lift"],
    }


# ---------------------------------------------------------------------------
# Log helpers
# ---------------------------------------------------------------------------

def _top_rules_text(rows: list[dict], n: int = 20) -> list[str]:
    lines = [f"  top {min(n, len(rows))} rules (sorted by lift):"]
    for r in rows[:n]:
        lines.append(
            f"    [{r['rank']:>3}] {r['antecedent']:<30} -> {r['consequent']:<30} "
            f"sup={r['support']:>6}  conf={r['confidence']:>6}  lift={r['lift']}"
        )
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline B association rule mining runner"
    )
    parser.add_argument("--input",      default="analysis/association_mining/outputs")
    parser.add_argument("--output",     default="analysis/association_mining/outputs")
    parser.add_argument("--min-sup",    type=float, default=0.05,
                        help="Minimum support fraction (default 0.05 = 5%%)")
    parser.add_argument("--min-conf",   type=float, default=0.50,
                        help="Minimum confidence (default 0.50 = 50%%)")
    parser.add_argument("--min-score",  type=float, default=0.0,
                        help="Only include pairs with score >= this value (default 0)")
    args = parser.parse_args(argv)

    in_dir  = pathlib.Path(args.input).resolve()
    out_dir = pathlib.Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    ranked_path = in_dir / "formulation_ranked.csv"
    if not ranked_path.exists():
        sys.exit(f"ERROR: {ranked_path} not found — run run_ranking.py first")

    print(f"Input:  {in_dir}")
    print(f"Output: {out_dir}")
    print(f"Params: min_support={args.min_sup:.0%}, "
          f"min_confidence={args.min_conf:.0%}, min_score={args.min_score}")

    t0 = time.monotonic()
    all_rows = _load(ranked_path)

    # Apply score filter
    pairs_in = [
        r for r in all_rows
        if _safe_float(r.get("score")) >= args.min_score
    ]
    print(f"Using {len(pairs_in)}/{len(all_rows)} pairs "
          f"(score >= {args.min_score})")

    # Build transactions
    transactions = [
        (discretise_bo(r), discretise_ap(r))
        for r in pairs_in
    ]

    print("Mining rules …")
    rules = mine_rules(
        transactions,
        min_support=args.min_sup,
        min_confidence=args.min_conf,
    )
    elapsed = time.monotonic() - t0

    rule_rows = [_rule_to_row(rule, i + 1) for i, rule in enumerate(rules)]
    _write(out_dir / "association_rules.csv", rule_rows)

    # Lift > 1 = positively associated; count how many
    n_lift_gt1 = sum(1 for r in rules if r["lift"] > 1.0)
    n_lift_lt1 = sum(1 for r in rules if r["lift"] < 1.0)

    log_lines = [
        f"Association rule mining completed in {elapsed:.2f}s",
        f"Input:  {in_dir}",
        f"Output: {out_dir}",
        "",
        f"=== Parameters ===",
        f"  min support:    {args.min_sup:.0%}",
        f"  min confidence: {args.min_conf:.0%}",
        f"  min score:      {args.min_score}",
        "",
        f"=== Input ===",
        f"  total candidate pairs: {len(all_rows)}",
        f"  pairs after score filter: {len(pairs_in)}",
        "",
        f"=== Results ===",
        f"  rules found:         {len(rules)}",
        f"  lift > 1 (positive): {n_lift_gt1}",
        f"  lift < 1 (negative): {n_lift_lt1}",
        "",
        *_top_rules_text(rule_rows, n=20),
    ]
    log_text = "\n".join(log_lines)
    (out_dir / "association_log.txt").write_text(log_text + "\n", encoding="utf-8")
    print(log_text)
    print(f"\nassociation_rules.csv written to {out_dir}")


def _safe_float(s) -> float:
    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


if __name__ == "__main__":
    main()
