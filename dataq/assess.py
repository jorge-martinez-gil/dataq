# -*- coding: utf-8 -*-
"""One-call assessment orchestrator.

``assess_catalog`` parses a catalog once and runs every single-catalog quality
dimension against it, returning a structured :class:`QualityReport`.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from rdflib import Graph, RDF

from . import __version__
from .io import load_rdf_text, parse_graph
from .namespaces import DCAT
from .report import QualityReport
from .metrics import (
    accuracy,
    completeness,
    consistency,
    licensing,
    provenance,
    readability,
    scalability,
    timeliness,
)


def _entity_counts(graph: Graph) -> dict:
    return {
        "Catalog": len(set(graph.subjects(RDF.type, DCAT.Catalog))),
        "Dataset": len(set(graph.subjects(RDF.type, DCAT.Dataset))),
        "Distribution": len(set(graph.subjects(RDF.type, DCAT.Distribution))),
    }


def assess_catalog(
    source: str,
    rdf_format: str = "turtle",
    check_links: bool = False,
    strict_dates: bool = False,
    include_scalability: bool = True,
    timeout: int = 30,
) -> QualityReport:
    """Assess a single catalog across all single-catalog dimensions.

    Parameters
    ----------
    source : str
        Path or URL to the catalog.
    rdf_format : str
        rdflib parser format (default ``turtle``).
    check_links : bool
        If True, compute the Accuracy dimension including live broken-link
        checking (requires network). Default False for deterministic,
        offline assessment.
    strict_dates : bool
        If True, reproduce the original strict datetime parser for Timeliness.
    include_scalability : bool
        Include the (non-deterministic, timing-based) scalability heuristic.
    timeout : int
        Network timeout for loading remote sources / link checks.
    """
    rdf_text = load_rdf_text(source, timeout=timeout)
    graph = parse_graph(rdf_text, rdf_format=rdf_format)

    metrics = [
        completeness.evaluate(graph, "dcat"),
        completeness.evaluate(graph, "dct"),
        accuracy.evaluate(graph, "dcat", check_links=check_links, timeout=timeout),
        consistency.evaluate(graph),
        licensing.evaluate(graph),
        readability.evaluate(graph),
        timeliness.evaluate(graph, strict=strict_dates),
        provenance.evaluate(graph),
    ]
    if include_scalability:
        metrics.append(scalability.evaluate(rdf_text, rdf_format=rdf_format))

    return QualityReport(
        source=source,
        dataq_version=__version__,
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        n_triples=len(graph),
        entities=_entity_counts(graph),
        metrics=metrics,
    )
