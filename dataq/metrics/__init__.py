# -*- coding: utf-8 -*-
"""DataQ quality-dimension metrics.

Each module exposes a low-level numeric function (faithful to the original
``check_*.py`` scripts) and an ``evaluate(...)`` wrapper returning a
:class:`dataq.report.MetricResult`.
"""
from . import (
    accuracy,
    compatibility,
    completeness,
    consistency,
    licensing,
    provenance,
    readability,
    scalability,
    similarity,
    timeliness,
)

__all__ = [
    "accuracy",
    "compatibility",
    "completeness",
    "consistency",
    "licensing",
    "provenance",
    "readability",
    "scalability",
    "similarity",
    "timeliness",
]
