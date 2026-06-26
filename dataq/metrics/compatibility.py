# -*- coding: utf-8 -*-
"""Cross-catalog compatibility.

Percentage of triples from the first catalog that also appear in the second.

Faithful port of ``check_compatibility.py`` (Martinez-Gil 2025).
"""
from __future__ import annotations

from typing import Optional

from rdflib import Graph

from ..report import MetricResult


def compatibility(graph1: Graph, graph2: Graph) -> Optional[float]:
    triples1 = set(graph1)
    triples2 = set(graph2)
    total = len(triples1)
    if total == 0:
        return None
    common = len(triples1 & triples2)
    return (common / total) * 100


def evaluate(graph1: Graph, graph2: Graph) -> MetricResult:
    value = compatibility(graph1, graph2)
    return MetricResult(
        key="compatibility",
        name="Cross-catalog compatibility",
        value=value,
        unit="percent",
        higher_is_better=None,
        details={"triples_first": len(set(graph1))},
    )
