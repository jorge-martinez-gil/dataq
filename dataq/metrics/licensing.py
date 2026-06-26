# -*- coding: utf-8 -*-
"""Licensing dimension.

Percentage of ``dcat:Dataset`` resources that declare a ``dcterms:license``.

Faithful port of ``check_licensing.py`` (Martinez-Gil 2025).
"""
from __future__ import annotations

from rdflib import Graph, RDF

from ..namespaces import DCAT, DCT
from ..report import MetricResult


def licensing(graph: Graph) -> float:
    licensed = 0
    total = 0
    for subject in graph.subjects(RDF.type, DCAT.Dataset):
        total += 1
        if any(graph.triples((subject, DCT.license, None))):
            licensed += 1
    if total == 0:
        return 0.0
    return (licensed / total) * 100


def evaluate(graph: Graph) -> MetricResult:
    licensed = 0
    total = 0
    for subject in graph.subjects(RDF.type, DCAT.Dataset):
        total += 1
        if any(graph.triples((subject, DCT.license, None))):
            licensed += 1
    value = 0.0 if total == 0 else (licensed / total) * 100
    return MetricResult(
        key="licensing",
        name="Licensing",
        value=value,
        unit="percent",
        higher_is_better=True,
        details={"datasets": total, "licensed_datasets": licensed},
    )
