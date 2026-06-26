# -*- coding: utf-8 -*-
"""Scalability dimension.

Heuristic that times an attribute-replacement operation on a tiny baseline
graph versus the catalog under test, returning ``"scalable"`` or
``"non-scalable"``.

Faithful port of ``check_scalability.py`` (Martinez-Gil 2025).

NOTE: this dimension is timing-based and therefore environment-dependent and
non-deterministic; it is reported but excluded from the aggregate score.
"""
from __future__ import annotations

import time
from typing import Optional

from rdflib import Graph, Namespace, URIRef, Literal

from ..report import MetricResult

_SMALL_RDF = """
@prefix ex: <http://example.org/> .
ex:subject1 ex:predicate1 "old_value" .
"""


def replace_attribute_value(rdf_data: str, subject: str, predicate: str,
                            old_value: str, new_value: str,
                            rdf_format: str = "turtle",
                            base_ns: Optional[Namespace] = None) -> str:
    if base_ns is None:
        base_ns = Namespace("http://example.org/")
    g = Graph()
    try:
        g.parse(data=rdf_data, format=rdf_format)
    except Exception:
        return rdf_data
    subject_uri = URIRef(base_ns + subject)
    predicate_uri = URIRef(base_ns + predicate)
    for s, p, _o in g.triples((subject_uri, predicate_uri, Literal(old_value))):
        g.set((s, p, Literal(new_value)))
    return g.serialize(format=rdf_format)


def scalability(rdf_data: str, rdf_format: str = "turtle") -> str:
    g_large = Graph()
    try:
        g_large.parse(data=rdf_data, format=rdf_format)
    except Exception:
        return "non-scalable"
    large_size = len(g_large)
    if large_size == 0:
        return "non-scalable"

    start_small = time.time()
    replace_attribute_value(_SMALL_RDF, "subject1", "predicate1",
                            "old_value", "new_value", rdf_format)
    small_time = time.time() - start_small

    start_large = time.time()
    replace_attribute_value(rdf_data, "subject1", "predicate1",
                            "old_value", "new_value", rdf_format)
    large_time_per_triple = (time.time() - start_large) / large_size

    return "scalable" if large_time_per_triple < small_time * 10 else "non-scalable"


def evaluate(rdf_data: str, rdf_format: str = "turtle") -> MetricResult:
    value = scalability(rdf_data, rdf_format=rdf_format)
    return MetricResult(
        key="scalability",
        name="Scalability",
        value=value,
        unit="category",
        higher_is_better=None,
        note="timing-based heuristic; non-deterministic",
        details={},
    )
