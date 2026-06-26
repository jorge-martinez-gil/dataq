# -*- coding: utf-8 -*-
"""Parity tests: the refactored package must reproduce the EXACT numbers of the
original standalone ``check_*.py`` scripts.

This is the scientific-integrity guardrail: the package is a faithful
refactor, not a re-derivation. If any of these fail, the refactor changed a
published result and must be fixed.
"""
import pytest

from dataq.io import parse_graph
from dataq.metrics import (
    accuracy,
    completeness,
    compatibility,
    consistency,
    licensing,
    provenance,
    readability,
    timeliness,
)
from conftest import CATALOGS, load_original

TOL = 1e-9


@pytest.mark.parametrize("property_set", ["dcat", "dct"])
def test_completeness_parity(catalog_text, property_set):
    orig = load_original("check_completeness")
    expected = orig.check_completeness(catalog_text, property_set)
    graph = parse_graph(catalog_text)
    got = completeness.completeness(graph, property_set)
    assert got == pytest.approx(expected, abs=TOL)


def test_consistency_parity(catalog_text):
    orig = load_original("check_consistency")
    expected = orig.check_consistency(catalog_text)
    graph = parse_graph(catalog_text)
    got = consistency.consistency(graph)
    assert got == pytest.approx(expected, abs=TOL)


def test_licensing_parity(catalog_text):
    orig = load_original("check_licensing")
    expected = orig.check_licensing(catalog_text)
    graph = parse_graph(catalog_text)
    got = licensing.licensing(graph)
    assert got == pytest.approx(expected, abs=TOL)


def test_readability_parity(catalog_text):
    orig = load_original("check_readability")
    expected = orig.check_readability(catalog_text)
    graph = parse_graph(catalog_text)
    got = readability.readability(graph)
    assert got == pytest.approx(expected, abs=TOL)


def test_provenance_parity(catalog_text):
    orig = load_original("check_lineage_provenance")
    expected = orig.check_lineage_provenance(catalog_text)
    graph = parse_graph(catalog_text)
    got = provenance.provenance(graph)
    assert got == pytest.approx(expected, abs=TOL)


def test_timeliness_strict_parity(catalog_text):
    """New strict mode must match the original (strict datetime parser)."""
    orig = load_original("check_timeliness")
    expected = orig.check_timeliness(catalog_text)
    graph = parse_graph(catalog_text)
    got = timeliness.timeliness(graph, strict=True)
    assert got == expected


def test_accuracy_components_parity(catalog_text):
    """Accuracy's offline building blocks (core completeness + duplicates)."""
    orig = load_original("check_accuracy")
    graph = parse_graph(catalog_text)
    for pset in ("dcat", "dct"):
        assert accuracy._core_completeness(graph, pset) == pytest.approx(
            orig.core_links(catalog_text, pset), abs=TOL
        )
    assert accuracy.duplicates(graph) == pytest.approx(
        orig.calculate_duplicates(catalog_text), abs=TOL
    )


def test_compatibility_parity():
    orig = load_original("check_compatibility")
    texts = [open(p, encoding="utf-8").read() for p in CATALOGS]
    # a handful of representative pairs (incl. identical-graph case)
    pairs = [(0, 0), (0, 1), (1, 2)]
    for i, j in pairs:
        if i >= len(texts) or j >= len(texts):
            continue
        expected = orig.check_compatibility(texts[i], texts[j])
        g1, g2 = parse_graph(texts[i]), parse_graph(texts[j])
        got = compatibility.compatibility(g1, g2)
        if expected is None:
            assert got is None
        else:
            assert got == pytest.approx(expected, abs=TOL)
