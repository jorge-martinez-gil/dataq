# -*- coding: utf-8 -*-
"""Lineage & provenance dimension.

Scores six criteria (each ~1.67 points, scaled x10 to a 0-100 range):
  - lineage info  (rdfs:subClassOf / rdfs:subPropertyOf present)
  - ancestors     (rdfs:subClassOf triples present)
  - descendants   (same check as ancestors)
  - provenance    (any prov:Entity)
  - data sources  (prov:used within a prov:Activity)
  - processing    (prov:wasAssociatedWith within a prov:Activity)

Faithful port of ``check_lineage_provenance.py`` (Martinez-Gil 2025).
"""
from __future__ import annotations

from rdflib import Graph, RDF, RDFS

from ..namespaces import PROV
from ..report import MetricResult


def _criteria(graph: Graph):
    has_lineage_info = any(
        p in (RDFS.subClassOf, RDFS.subPropertyOf) for _s, p, _o in graph
    )
    has_ancestors = any(True for _ in graph.triples((None, RDFS.subClassOf, None)))
    has_descendants = has_ancestors
    has_provenance_info = any(
        True for _ in graph.triples((None, RDF.type, PROV.Entity))
    )

    has_data_sources = False
    has_processing = False
    for s, _p, _o in graph.triples((None, RDF.type, PROV.Activity)):
        if not has_data_sources:
            has_data_sources = any(True for _ in graph.triples((s, PROV.used, None)))
        if not has_processing:
            has_processing = any(
                True for _ in graph.triples((s, PROV.wasAssociatedWith, None))
            )
        if has_data_sources and has_processing:
            break

    return {
        "lineage_info": has_lineage_info,
        "ancestors": has_ancestors,
        "descendants": has_descendants,
        "provenance_info": has_provenance_info,
        "data_sources": has_data_sources,
        "processing_steps": has_processing,
    }


def provenance(graph: Graph) -> float:
    crit = _criteria(graph)
    score = 1.67 * sum(1 for v in crit.values() if v)
    if score == 0:
        return 0.0
    return score * 10


def evaluate(graph: Graph) -> MetricResult:
    crit = _criteria(graph)
    score = 1.67 * sum(1 for v in crit.values() if v)
    value = 0.0 if score == 0 else score * 10
    return MetricResult(
        key="provenance",
        name="Lineage & provenance",
        value=value,
        unit="percent",
        higher_is_better=True,
        details=crit,
    )
