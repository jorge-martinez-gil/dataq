# -*- coding: utf-8 -*-
"""DataQ command-line interface.

One command to assess a catalog and emit a structured report:

    dataq assess example001.ttl
    dataq assess https://example.org/catalog.ttl --format json -o report.json
    dataq assess catalog.ttl --check-links          # include live link checks

Cross-catalog tools:

    dataq similarity a.ttl b.ttl
    dataq compatibility a.ttl b.ttl

Inspect a catalog:

    dataq show catalog.ttl
"""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .io import load_graph, RDFLoadError
from .assess import assess_catalog
from .metrics import similarity as similarity_metric
from .metrics import compatibility as compatibility_metric


def _add_format_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--rdf-format", default="turtle",
        help="rdflib input format (turtle, xml, json-ld, nt, n3). Default: turtle.",
    )


def _cmd_assess(args: argparse.Namespace) -> int:
    try:
        report = assess_catalog(
            args.source,
            rdf_format=args.rdf_format,
            check_links=args.check_links,
            strict_dates=args.strict_dates,
            include_scalability=not args.no_scalability,
        )
    except RDFLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        output = report.to_json()
    elif args.format == "markdown":
        output = report.to_markdown()
    else:
        output = report.to_text()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output + "\n")
        print(f"Wrote {args.format} report to {args.output}")
    else:
        print(output)
    return 0


def _cmd_similarity(args: argparse.Namespace) -> int:
    try:
        g1 = load_graph(args.source1, rdf_format=args.rdf_format)
        g2 = load_graph(args.source2, rdf_format=args.rdf_format)
    except RDFLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    value = similarity_metric.similarity(g1, g2, prefer_nltk=not args.offline)
    print(f"The similarity of '{args.source1}' and '{args.source2}' is {value:.2f}%.")
    return 0


def _cmd_compatibility(args: argparse.Namespace) -> int:
    try:
        g1 = load_graph(args.source1, rdf_format=args.rdf_format)
        g2 = load_graph(args.source2, rdf_format=args.rdf_format)
    except RDFLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    value = compatibility_metric.compatibility(g1, g2)
    if value is None:
        print("No triples found in the first catalog or a parsing error occurred.")
        return 1
    print(f"The compatibility of '{args.source1}' and '{args.source2}' is {value:.2f}%.")
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    try:
        graph = load_graph(args.source, rdf_format=args.rdf_format)
    except RDFLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    structured: dict = {}
    for subject, predicate, obj in graph:
        structured.setdefault(str(subject), {}).setdefault(str(predicate), []).append(str(obj))
    for subject, data in structured.items():
        print(subject)
        for predicate, objects in data.items():
            print(f"  {predicate}: {objects}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dataq",
        description="Automated quality assessment of open data catalogs (DCAT/RDF).",
        epilog="Cite: Martinez-Gil, J. (2025). ESWA 289:128379. "
               "https://doi.org/10.1016/j.eswa.2025.128379",
    )
    parser.add_argument("--version", action="version", version=f"dataq {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_assess = sub.add_parser("assess", help="Assess one catalog across all dimensions.")
    p_assess.add_argument("source", help="Path or URL to the catalog.")
    p_assess.add_argument("-f", "--format", choices=["text", "json", "markdown"],
                          default="text", help="Output format. Default: text.")
    p_assess.add_argument("-o", "--output", help="Write the report to a file.")
    p_assess.add_argument("--check-links", action="store_true",
                          help="Include the Accuracy dimension with live HTTP "
                               "broken-link checking (requires network).")
    p_assess.add_argument("--strict-dates", action="store_true",
                          help="Use the original strict datetime parser for Timeliness.")
    p_assess.add_argument("--no-scalability", action="store_true",
                          help="Skip the non-deterministic scalability heuristic.")
    _add_format_args(p_assess)
    p_assess.set_defaults(func=_cmd_assess)

    p_sim = sub.add_parser("similarity", help="Jaccard similarity between two catalogs.")
    p_sim.add_argument("source1")
    p_sim.add_argument("source2")
    p_sim.add_argument("--offline", action="store_true",
                       help="Force the offline tokenizer (do not use NLTK data).")
    _add_format_args(p_sim)
    p_sim.set_defaults(func=_cmd_similarity)

    p_compat = sub.add_parser("compatibility", help="Triple-overlap compatibility of two catalogs.")
    p_compat.add_argument("source1")
    p_compat.add_argument("source2")
    _add_format_args(p_compat)
    p_compat.set_defaults(func=_cmd_compatibility)

    p_show = sub.add_parser("show", help="Print a catalog as subject/predicate/object.")
    p_show.add_argument("source")
    _add_format_args(p_show)
    p_show.set_defaults(func=_cmd_show)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
