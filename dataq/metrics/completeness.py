# -*- coding: utf-8 -*-
"""Completeness dimension.

Measures the presence of core DCAT or Dublin Core Terms (DCT) properties on
the catalog's ``Catalog``, ``Dataset`` and ``Distribution`` resources.

Faithful port of ``check_completeness.py`` from the original framework
(Martinez-Gil 2025, ESWA 289:128379). Numerical behaviour is unchanged.
"""
from __future__ import annotations

from typing import List

from rdflib import Graph, RDF

from ..namespaces import DCAT, DCT
from ..report import MetricResult

DCAT_PROPERTIES: List = [DCAT.title, DCAT.downloadURL, DCAT.size]
DCT_PROPERTIES: List = [DCT.title, DCT.identifier, DCT.description]

ENTITY_TYPES = [DCAT.Catalog, DCAT.Dataset, DCAT.Distribution]


def _subject_completeness(graph: Graph, subject, required_properties: List) -> float:
    present = set()
    for predicate, _ in graph.predicate_objects(subject):
        if predicate in required_properties:
            present.add(predicate)
    return (len(present) / len(required_properties)) * 100


def completeness(graph: Graph, property_set: str = "dcat") -> float:
    """Average completeness percentage across catalog resources.

    Parameters
    ----------
    graph : rdflib.Graph
    property_set : str
        ``"dcat"`` (default) or ``"dct"``.
    """
    property_set = property_set.lower()
    required = DCT_PROPERTIES if property_set == "dct" else DCAT_PROPERTIES

    scores = []
    for subject_type in ENTITY_TYPES:
        for subject in graph.subjects(RDF.type, subject_type):
            scores.append(_subject_completeness(graph, subject, required))

    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def evaluate(graph: Graph, property_set: str = "dcat") -> MetricResult:
    value = completeness(graph, property_set)
    pset = property_set.upper()
    required = DCT_PROPERTIES if property_set.lower() == "dct" else DCAT_PROPERTIES
    return MetricResult(
        key=f"completeness_{property_set.lower()}",
        name=f"Completeness ({pset})",
        value=value,
        unit="percent",
        higher_is_better=True,
        details={
            "property_set": pset,
            "required_properties": [str(p) for p in required],
        },
    )
