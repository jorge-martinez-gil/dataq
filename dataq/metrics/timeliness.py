# -*- coding: utf-8 -*-
"""Timeliness dimension.

A catalog is "timely" when its ``dcterms:modified`` date falls within the last
365 days.

Faithful port of ``check_timeliness.py`` (Martinez-Gil 2025), with one
reproducibility-oriented generalisation: the original required a full
``%Y-%m-%dT%H:%M:%S%z`` datetime and silently failed on plain ``xsd:date``
values (e.g. ``2023-07-15``), which are extremely common in real catalogs.
The default parser here accepts ``xsd:date`` and ``xsd:dateTime`` (with or
without timezone). Pass ``strict=True`` to reproduce the original behaviour
exactly. The metric *definition* (within 365 days) is unchanged.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from rdflib import Graph, RDF

from ..namespaces import DCAT, DCT
from ..report import MetricResult


def _parse_strict(value: str) -> Optional[datetime]:
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    except Exception:
        return None


def _parse_lenient(value: str) -> Optional[datetime]:
    raw = value.strip()
    candidate = raw.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(candidate)
    except ValueError:
        # date-only or unexpected; try a few explicit patterns
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                dt = datetime.strptime(raw, fmt)
                break
            except ValueError:
                continue
        else:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _catalog_modified(graph: Graph) -> Optional[str]:
    for s, _p, _o in graph.triples((None, RDF.type, DCAT.Catalog)):
        for _s2, _p2, o2 in graph.triples((s, DCT.modified, None)):
            return str(o2)
    return None


def timeliness(graph: Graph, strict: bool = False, max_age_days: int = 365) -> bool:
    modified = _catalog_modified(graph)
    if not modified:
        return False
    parsed = _parse_strict(modified) if strict else _parse_lenient(modified)
    if parsed is None:
        return False
    threshold = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    return parsed > threshold


def evaluate(graph: Graph, strict: bool = False, max_age_days: int = 365) -> MetricResult:
    modified = _catalog_modified(graph)
    value = timeliness(graph, strict=strict, max_age_days=max_age_days)
    note = "" if modified else "no dcterms:modified on catalog"
    return MetricResult(
        key="timeliness",
        name="Timeliness (<=365d)",
        value=value,
        unit="boolean",
        higher_is_better=True,
        note=note,
        details={"modified": modified, "max_age_days": max_age_days, "strict": strict},
    )
