# -*- coding: utf-8 -*-
"""Readability dimension: mean Flesch-Kincaid grade of dataset titles and
descriptions. Faithful port of check_readability.py (Martinez-Gil 2025)."""
from __future__ import annotations

import textstat
from rdflib import Graph, RDF

from ..namespaces import DCAT, DCT
from ..report import MetricResult


def _scores(graph):
    out, present = [], 0
    for s in graph.subjects(RDF.type, DCAT.Dataset):
        for text in (graph.value(s, DCAT.title), graph.value(s, DCT.description)):
            if text:
                present += 1
                try:
                    out.append(textstat.flesch_kincaid_grade(str(text)))
                except Exception:
                    pass
    return out, present


def readability(graph: Graph) -> float:
    out, _ = _scores(graph)
    return sum(out) / len(out) if out else 0.0


def evaluate(graph: Graph) -> MetricResult:
    out, present = _scores(graph)
    if present and not out:
        return MetricResult("readability", "Readability (FK grade)", None,
                            "grade", False, {"texts_present": present},
                            skipped=True, note="textstat backend unavailable")
    val = sum(out) / len(out) if out else 0.0
    note = "FK grade; lower = easier" if present else "no titles/descriptions"
    return MetricResult("readability", "Readability (FK grade)", val,
                        "grade", False, {"texts_scored": len(out)}, note=note)
