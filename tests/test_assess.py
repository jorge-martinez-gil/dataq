# -*- coding: utf-8 -*-
"""Behavioural tests for the unified assessor, report model, and CLI."""
import json

import pytest

from dataq import assess_catalog, __version__
from dataq.report import QualityReport, MetricResult
from dataq.metrics import similarity, scalability
from dataq.io import parse_graph


def test_assess_returns_report(catalog_path):
    report = assess_catalog(catalog_path)
    assert isinstance(report, QualityReport)
    assert report.dataq_version == __version__
    assert report.n_triples > 0
    # every expected dimension key is present
    keys = {m.key for m in report.metrics}
    for expected in {
        "completeness_dcat", "completeness_dct", "accuracy_dcat",
        "consistency", "licensing", "readability", "timeliness",
        "provenance", "scalability",
    }:
        assert expected in keys


def test_percent_metrics_in_range(catalog_path):
    report = assess_catalog(catalog_path)
    for m in report.metrics:
        if m.unit == "percent" and not m.skipped and m.value is not None:
            assert 0.0 <= m.value <= 100.0


def test_accuracy_skipped_by_default(catalog_path):
    report = assess_catalog(catalog_path)
    acc = report.metric("accuracy_dcat")
    assert acc is not None and acc.skipped is True


def test_json_roundtrip(catalog_path):
    report = assess_catalog(catalog_path)
    payload = json.loads(report.to_json())
    assert payload["source"] == catalog_path
    assert "metrics" in payload and len(payload["metrics"]) >= 8
    assert "aggregate_score" in payload


def test_markdown_and_text_render(catalog_path):
    report = assess_catalog(catalog_path)
    assert "DataQ quality report" in report.to_markdown()
    assert "DataQ quality report" in report.to_text()


def test_aggregate_is_mean_of_listed_dimensions(catalog_path):
    report = assess_catalog(catalog_path)
    agg = report.aggregate_score
    listed = report.aggregated_dimensions
    if agg is not None:
        vals = [report.metric(k).value for k in listed]
        assert agg == pytest.approx(sum(vals) / len(vals))


def test_similarity_identical_is_100(catalog_text):
    g = parse_graph(catalog_text)
    g2 = parse_graph(catalog_text)
    assert similarity.similarity(g, g2, prefer_nltk=False) == pytest.approx(100.0)


def test_similarity_offline_runs(catalog_text):
    """Offline tokenizer path must work without NLTK data downloads."""
    g1 = parse_graph(catalog_text)
    g2 = parse_graph(catalog_text)
    val = similarity.similarity(g1, g2, prefer_nltk=False)
    assert 0.0 <= val <= 100.0


def test_scalability_category(catalog_text):
    assert scalability.scalability(catalog_text) in {"scalable", "non-scalable"}


def test_metricresult_display():
    assert MetricResult("k", "n", 42.0, "percent").display_value() == "42.00%"
    assert MetricResult("k", "n", True, "boolean").display_value() == "yes"
    assert MetricResult("k", "n", None, "percent", skipped=True).display_value() == "skipped"
