# -*- coding: utf-8 -*-
"""Accuracy dimension (plus its building blocks: duplicates and broken links).

Faithful port of ``check_accuracy.py`` (Martinez-Gil 2025, ESWA 289:128379).

    Accuracy = 100 - mean(missing_core_pct, duplicates_pct, broken_links_pct)

Note on reproducibility: broken-link checking performs a live HTTP request for
every distinct URI in the graph. It is therefore *opt-in* in the package API
(``check_links``) so that offline assessment is deterministic. The original
formula and numbers are reproduced exactly when ``check_links=True``.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Optional

import requests
from rdflib import Graph, RDF, URIRef

from ..namespaces import DCAT, DCT, RDF_NS
from ..report import MetricResult

DCT_PROPERTIES = [DCT.title, DCT.identifier, DCT.description]


def duplicates(graph: Graph) -> float:
    """Percentage of duplicated dataset/distribution titles or download URLs."""
    counts = defaultdict(int)
    for _s, p, o in graph.triples((None, None, None)):
        if p == DCAT.title or p == DCAT.downloadURL:
            counts[o] += 1
    total = len(counts)
    if total == 0:
        return 0.0
    dup = sum(1 for c in counts.values() if c > 1)
    return (dup / total) * 100


def broken_links(graph: Graph, timeout: int = 5, session: Optional[requests.Session] = None) -> float:
    """Percentage of URIRef objects that do not resolve with HTTP 200.

    Performs live network requests. Returns 0.0 when there are no links.
    """
    link_counts = defaultdict(int)
    for _s, _p, o in graph:
        if isinstance(o, URIRef):
            link_counts[str(o)] += 1

    total_links = sum(link_counts.values())
    if total_links == 0:
        return 0.0

    own_session = session is None
    session = session or requests.Session()
    broken = 0
    try:
        for url, count in link_counts.items():
            try:
                response = session.get(url, timeout=timeout)
                if response.status_code != 200:
                    broken += count
            except requests.exceptions.RequestException:
                broken += count
    finally:
        if own_session:
            session.close()
    return (broken / total_links) * 100


def _core_completeness(graph: Graph, property_set: str) -> float:
    """Completeness term used *inside* the accuracy formula.

    Mirrors ``core_links`` in the original script, where the DCAT required set
    is ``[dcat:title, rdf:type]`` (intentionally different from the standalone
    completeness dimension).
    """
    if property_set == "dct":
        required = DCT_PROPERTIES
    else:
        required = [DCAT.title, RDF_NS.type]

    scores = []
    for subject_type in (DCAT.Catalog, DCAT.Dataset, DCAT.Distribution):
        for subject in graph.subjects(RDF.type, subject_type):
            present = set()
            for predicate, _ in graph.predicate_objects(subject):
                if predicate in required:
                    present.add(predicate)
            scores.append((len(present) / len(required)) * 100)
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def accuracy(graph: Graph, property_set: str = "dcat", check_links: bool = True,
             timeout: int = 5) -> float:
    """Overall accuracy percentage (see module docstring)."""
    completeness_pct = _core_completeness(graph, property_set)
    missing_core_pct = 100 - completeness_pct
    duplicates_pct = duplicates(graph)
    broken_links_pct = broken_links(graph, timeout=timeout) if check_links else 0.0
    avg_error = (missing_core_pct + duplicates_pct + broken_links_pct) / 3
    return 100 - avg_error


def evaluate(graph: Graph, property_set: str = "dcat", check_links: bool = False,
             timeout: int = 5) -> MetricResult:
    completeness_pct = _core_completeness(graph, property_set)
    duplicates_pct = duplicates(graph)
    pset = property_set.upper()

    if not check_links:
        return MetricResult(
            key=f"accuracy_{property_set.lower()}",
            name=f"Accuracy ({pset})",
            value=None,
            unit="percent",
            higher_is_better=True,
            skipped=True,
            note="enable --check-links (live HTTP); requires network",
            details={
                "core_completeness_pct": completeness_pct,
                "duplicates_pct": duplicates_pct,
                "broken_links_pct": None,
            },
        )

    broken_links_pct = broken_links(graph, timeout=timeout)
    avg_error = ((100 - completeness_pct) + duplicates_pct + broken_links_pct) / 3
    value = 100 - avg_error
    return MetricResult(
        key=f"accuracy_{property_set.lower()}",
        name=f"Accuracy ({pset})",
        value=value,
        unit="percent",
        higher_is_better=True,
        details={
            "core_completeness_pct": completeness_pct,
            "duplicates_pct": duplicates_pct,
            "broken_links_pct": broken_links_pct,
        },
    )
