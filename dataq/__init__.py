# -*- coding: utf-8 -*-
"""DataQ - automated quality assessment of open data catalogs.

DataQ evaluates DCAT/RDF open data catalogs across eight FAIR-aligned quality
dimensions (accuracy, completeness, consistency, scalability, timeliness,
provenance, readability, licensing) plus cross-catalog compatibility and
similarity.

Reference implementation for:

    Martinez-Gil, J. (2025). Framework to automatically determine the quality
    of open data catalogs. Expert Systems with Applications, 289, 128379.
    https://doi.org/10.1016/j.eswa.2025.128379

Quick start
-----------
>>> from dataq import assess_catalog
>>> report = assess_catalog("example001.ttl")
>>> print(report.to_text())
>>> report.to_dict()["aggregate_score"]
"""
__version__ = "1.0.0"

from .io import load_graph, load_rdf_text, parse_graph, RDFLoadError  # noqa: E402
from .report import MetricResult, QualityReport  # noqa: E402
from .assess import assess_catalog  # noqa: E402

__all__ = [
    "__version__",
    "assess_catalog",
    "load_graph",
    "load_rdf_text",
    "parse_graph",
    "RDFLoadError",
    "MetricResult",
    "QualityReport",
]
