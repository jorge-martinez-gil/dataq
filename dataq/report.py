# -*- coding: utf-8 -*-
"""Structured, serializable result objects for DataQ.

The original scripts only ``print()`` a number. Research reuse, benchmarking
and reproducibility require *machine-readable* results, so every metric returns
a :class:`MetricResult` and a full assessment returns a :class:`QualityReport`
that serializes to dict / JSON / Markdown / plain text.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class MetricResult:
    """The outcome of evaluating one quality dimension.

    Attributes
    ----------
    key : str
        Stable machine identifier, e.g. ``"completeness_dcat"``.
    name : str
        Human-readable dimension name.
    value : Any
        The measured value (percentage float, grade level, bool, or category).
    unit : str
        One of ``percent``, ``grade``, ``boolean``, ``category``.
    higher_is_better : Optional[bool]
        Direction of "good" for ranking/aggregation. ``None`` when not ordinal.
    details : dict
        Supporting numbers (counts, sub-scores, raw values).
    skipped : bool
        True when the metric was intentionally not computed (e.g. network
        link-checking disabled).
    note : str
        Free-text caveat shown to users (e.g. "non-deterministic").
    """

    key: str
    name: str
    value: Any
    unit: str
    higher_is_better: Optional[bool] = None
    details: Dict[str, Any] = field(default_factory=dict)
    skipped: bool = False
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def display_value(self) -> str:
        if self.skipped:
            return "skipped"
        if self.value is None:
            return "n/a"
        if self.unit == "percent":
            return f"{self.value:.2f}%"
        if self.unit == "grade":
            return f"{self.value:.2f}"
        if self.unit == "boolean":
            return "yes" if self.value else "no"
        return str(self.value)


@dataclass
class QualityReport:
    """A complete quality assessment of a single catalog."""

    source: str
    dataq_version: str
    timestamp: str
    n_triples: int
    entities: Dict[str, int]
    metrics: List[MetricResult] = field(default_factory=list)

    # -- aggregation -------------------------------------------------------
    #: Dimensions included in the convenience aggregate score. Only percentage
    #: based, higher-is-better dimensions are aggregated; readability (a grade
    #: level), timeliness (boolean) and scalability (category) are reported but
    #: deliberately excluded because averaging them is not meaningful.
    AGGREGATE_KEYS = (
        "completeness_dcat",
        "consistency",
        "licensing",
        "provenance",
        "accuracy_dcat",
    )

    def metric(self, key: str) -> Optional[MetricResult]:
        for metric in self.metrics:
            if metric.key == key:
                return metric
        return None

    @property
    def aggregate_score(self) -> Optional[float]:
        """Unweighted mean of the percentage-based dimensions.

        IMPORTANT: this is a transparent convenience indicator, *not* a score
        defined in the source paper. It averages only the not-skipped,
        percentage-valued, higher-is-better dimensions listed in
        ``AGGREGATE_KEYS``. Returns ``None`` if none are available.
        """
        values = [
            m.value
            for m in self.metrics
            if m.key in self.AGGREGATE_KEYS
            and not m.skipped
            and isinstance(m.value, (int, float))
        ]
        if not values:
            return None
        return sum(values) / len(values)

    @property
    def aggregated_dimensions(self) -> List[str]:
        return [
            m.key
            for m in self.metrics
            if m.key in self.AGGREGATE_KEYS
            and not m.skipped
            and isinstance(m.value, (int, float))
        ]

    # -- serialization -----------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "dataq_version": self.dataq_version,
            "timestamp": self.timestamp,
            "n_triples": self.n_triples,
            "entities": self.entities,
            "aggregate_score": self.aggregate_score,
            "aggregated_dimensions": self.aggregated_dimensions,
            "metrics": [m.to_dict() for m in self.metrics],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def to_markdown(self) -> str:
        lines = [
            f"# DataQ quality report",
            "",
            f"**Source:** `{self.source}`  ",
            f"**Generated:** {self.timestamp} · DataQ v{self.dataq_version}  ",
            f"**Triples:** {self.n_triples} · "
            f"Catalogs: {self.entities.get('Catalog', 0)} · "
            f"Datasets: {self.entities.get('Dataset', 0)} · "
            f"Distributions: {self.entities.get('Distribution', 0)}",
            "",
        ]
        agg = self.aggregate_score
        if agg is not None:
            lines += [
                f"**Aggregate quality score:** {agg:.2f}%  ",
                f"_(unweighted mean of: {', '.join(self.aggregated_dimensions)}; "
                "a convenience indicator, not defined in the source paper)_",
                "",
            ]
        lines += ["| Dimension | Result | Notes |", "|---|---|---|"]
        for m in self.metrics:
            note = m.note or ""
            lines.append(f"| {m.name} | {m.display_value()} | {note} |")
        lines += [
            "",
            "> Cite: Martinez-Gil, J. (2025). Framework to automatically determine "
            "the quality of open data catalogs. *Expert Systems with Applications*, "
            "289, 128379. https://doi.org/10.1016/j.eswa.2025.128379",
        ]
        return "\n".join(lines)

    def to_text(self) -> str:
        width = 60
        lines = [
            "=" * width,
            "DataQ quality report",
            "=" * width,
            f"Source     : {self.source}",
            f"Generated  : {self.timestamp}  (DataQ v{self.dataq_version})",
            f"Triples    : {self.n_triples}",
            f"Entities   : "
            f"{self.entities.get('Catalog', 0)} catalog(s), "
            f"{self.entities.get('Dataset', 0)} dataset(s), "
            f"{self.entities.get('Distribution', 0)} distribution(s)",
            "-" * width,
        ]
        for m in self.metrics:
            label = m.name.ljust(28)
            lines.append(f"{label}: {m.display_value()}"
                         + (f"   [{m.note}]" if m.note else ""))
        lines.append("-" * width)
        agg = self.aggregate_score
        if agg is not None:
            lines.append(f"{'Aggregate score'.ljust(28)}: {agg:.2f}%")
            lines.append(f"  (mean of: {', '.join(self.aggregated_dimensions)};")
            lines.append("   convenience indicator, not from the source paper)")
        lines.append("=" * width)
        return "\n".join(lines)
