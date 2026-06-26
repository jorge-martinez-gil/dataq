# -*- coding: utf-8 -*-
"""Reproducible benchmark over the bundled catalogs.

Runs the full DataQ assessment on every example and "Official catalogs"
catalog and writes a comparison table to ``benchmark/results.csv`` and
``benchmark/results.md``. All numbers are computed live - nothing is
hard-coded - so the table is fully reproducible:

    python examples/run_benchmark.py

Add ``--check-links`` to include the network-dependent Accuracy dimension.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from dataq import assess_catalog

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "benchmark"
DIMENSIONS = [
    ("completeness_dcat", "Completeness(DCAT)%"),
    ("completeness_dct", "Completeness(DCT)%"),
    ("consistency", "Consistency%"),
    ("licensing", "Licensing%"),
    ("provenance", "Provenance%"),
    ("readability", "Readability(FK)"),
    ("timeliness", "Timely"),
]


def catalogs():
    paths = sorted(ROOT.glob("example*.ttl"))
    paths += sorted((ROOT / "Official catalogs").glob("*.ttl"))
    return paths


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    check_links = "--check-links" in argv
    OUT.mkdir(exist_ok=True)
    rows = []
    for path in catalogs():
        report = assess_catalog(str(path), check_links=check_links)
        row = {"catalog": path.name, "triples": report.n_triples,
               "aggregate%": round(report.aggregate_score, 2)
               if report.aggregate_score is not None else None}
        for key, label in DIMENSIONS:
            m = report.metric(key)
            v = None if (m is None or m.skipped) else m.value
            row[label] = round(v, 2) if isinstance(v, float) else v
        rows.append(row)
        print(f"assessed {path.name}: aggregate={row['aggregate%']}")

    header = ["catalog", "triples", "aggregate%"] + [lbl for _, lbl in DIMENSIONS]
    with open(OUT / "results.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    lines = ["# DataQ benchmark over bundled catalogs", "",
             "Computed live by `examples/run_benchmark.py` (no hard-coded values).",
             "", "| " + " | ".join(header) + " |",
             "|" + "|".join(["---"] * len(header)) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(h, "")) for h in header) + " |")
    (OUT / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT/'results.csv'} and {OUT/'results.md'} ({len(rows)} catalogs).")


if __name__ == "__main__":
    main()
