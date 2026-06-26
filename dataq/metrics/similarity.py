# -*- coding: utf-8 -*-
"""Cross-catalog similarity: Jaccard over titles & descriptions.

Faithful port of check_similarity.py (Martinez-Gil 2025). Uses NLTK when its
data is present, otherwise the offline tokenizer in _text.py."""
from __future__ import annotations

from rdflib import Graph
from rdflib.compare import isomorphic

from ..namespaces import DCAT
from ..report import MetricResult
from ._text import preprocess_text, jaccard_similarity


def _graphs_identical(g1: Graph, g2: Graph) -> bool:
    # RDF isomorphism canonicalises blank nodes, so a catalog vs itself == 100%
    # (the original triple-by-triple test mislabels re-parsed blank nodes).
    return len(g1) == len(g2) and isomorphic(g1, g2)


def _mean_jaccard(a, b, prefer_nltk):
    sa = [preprocess_text(x, prefer_nltk) for x in a]
    sb = [preprocess_text(x, prefer_nltk) for x in b]
    if not (sa and sb):
        return 0.0
    return sum(jaccard_similarity(x, y) for x in sa for y in sb) / (len(sa) * len(sb))


def similarity(graph1: Graph, graph2: Graph, prefer_nltk: bool = True) -> float:
    if _graphs_identical(graph1, graph2):
        return 100.0
    t1 = [str(t) for t in graph1.objects(predicate=DCAT.title)]
    t2 = [str(t) for t in graph2.objects(predicate=DCAT.title)]
    d1 = [str(d) for d in graph1.objects(predicate=DCAT.description)]
    d2 = [str(d) for d in graph2.objects(predicate=DCAT.description)]
    title_sim = _mean_jaccard(t1, t2, prefer_nltk)
    desc_sim = _mean_jaccard(d1, d2, prefer_nltk)
    return ((title_sim + desc_sim) / 2) * 100


def evaluate(graph1: Graph, graph2: Graph, prefer_nltk: bool = True) -> MetricResult:
    return MetricResult("similarity", "Cross-catalog similarity",
                        similarity(graph1, graph2, prefer_nltk),
                        "percent", None, {})
