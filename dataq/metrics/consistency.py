# -*- coding: utf-8 -*-
"""Consistency dimension.

Percentage of (subject, predicate) pairs - across DCAT Catalog, Dataset and
Distribution resources - that carry a single, non-conflicting value.

Faithful port of ``check_consistency.py`` (Martinez-Gil 2025).
"""
from __future__ import annotations

from rdflib import Graph, RDF

from ..namespaces import DCAT
from ..report import MetricResult


def consistency(graph: Graph) -> float:
    catalogs = set(graph.subjects(RDF.type, DCAT.Catalog))
    datasets = set(graph.subjects(RDF.type, DCAT.Dataset))
    distributions = set(graph.subjects(RDF.type, DCAT.Distribution))
    entities = catalogs | datasets | distributions

    pairs = {}
    for subj in entities:
        for pred, obj in graph.predicate_objects(subj):
            key = (subj, pred)
            if key in pairs:
                pairs[key].add(obj)
            else:
                pairs[key] = {obj}

    total = len(pairs)
    if total == 0:
        return 0.0
    inconsistent = sum(1 for objs in pairs.values() if len(objs) > 1)
    return ((total - inconsistent) / total) * 100


def evaluate(graph: Graph) -> MetricResult:
    catalogs = set(graph.subjects(RDF.type, DCAT.Catalog))
    datasets = set(graph.subjects(RDF.type, DCAT.Dataset))
    distributions = set(graph.subjects(RDF.type, DCAT.Distribution))
    entities = catalogs | datasets | distributions

    pairs = {}
    for subj in entities:
        for pred, obj in graph.predicate_objects(subj):
            pairs.setdefault((subj, pred), set()).add(obj)

    total = len(pairs)
    inconsistent = sum(1 for objs in pairs.values() if len(objs) > 1)
    value = 0.0 if total == 0 else ((total - inconsistent) / total) * 100
    return MetricResult(
        key="consistency",
        name="Consistency",
        value=value,
        unit="percent",
        higher_is_better=True,
        details={"pairs": total, "inconsistent_pairs": inconsistent},
    )
