# -*- coding: utf-8 -*-
"""Unified RDF input/output for DataQ.

The original framework re-implemented "load from file or URL" in every single
``check_*.py`` script. This module provides that capability once, so every
quality dimension loads catalogs through identical, well-tested code paths.

Public API
----------
load_rdf_text(source)   -> str     Raw RDF/Turtle text from a path or URL.
load_graph(source, ...) -> Graph   A parsed ``rdflib.Graph``.
"""
from __future__ import annotations

import sys
from typing import Optional

import requests
from rdflib import Graph


class RDFLoadError(Exception):
    """Raised when RDF data cannot be loaded or parsed."""


def is_url(source: str) -> bool:
    """Return True if ``source`` looks like an HTTP(S) URL."""
    return source.startswith("http://") or source.startswith("https://")


def load_rdf_text(source: str, timeout: int = 30) -> str:
    """Load raw RDF text from a local file path or an HTTP(S) URL.

    Parameters
    ----------
    source : str
        A local file path or an ``http(s)://`` URL.
    timeout : int
        Request timeout in seconds (URLs only).

    Returns
    -------
    str
        The RDF document as text.

    Raises
    ------
    RDFLoadError
        If the file is missing or the URL cannot be fetched.
    """
    if is_url(source):
        try:
            response = requests.get(source, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as exc:  # pragma: no cover
            raise RDFLoadError(f"Error fetching URL {source}: {exc}") from exc
    try:
        with open(source, "r", encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError as exc:
        raise RDFLoadError(f"File not found: {source}") from exc
    except UnicodeDecodeError as exc:  # pragma: no cover
        raise RDFLoadError(f"Unicode decode error for {source}: {exc}") from exc


def load_graph(source: str, rdf_format: str = "turtle", timeout: int = 30) -> Graph:
    """Load ``source`` and return a parsed :class:`rdflib.Graph`.

    Parameters
    ----------
    source : str
        Local path or URL.
    rdf_format : str
        rdflib parser format (``turtle``, ``xml``/``rdfxml``, ``json-ld``,
        ``nt``, ``n3`` ...). Default ``turtle``.
    timeout : int
        Request timeout for URLs.

    Returns
    -------
    rdflib.Graph
    """
    text = load_rdf_text(source, timeout=timeout)
    return parse_graph(text, rdf_format=rdf_format)


def parse_graph(rdf_text: str, rdf_format: str = "turtle") -> Graph:
    """Parse RDF text into a graph, raising :class:`RDFLoadError` on failure."""
    graph = Graph()
    try:
        graph.parse(data=rdf_text, format=rdf_format)
    except Exception as exc:
        raise RDFLoadError(f"Error parsing RDF data: {exc}") from exc
    return graph


def as_graph(source_or_graph, rdf_format: str = "turtle") -> Graph:
    """Accept either a path/URL string or an already-parsed Graph.

    Lets metric functions be called flexibly from the CLI (paths) or from
    notebooks/tests (in-memory graphs) without duplicate parsing.
    """
    if isinstance(source_or_graph, Graph):
        return source_or_graph
    return load_graph(source_or_graph, rdf_format=rdf_format)
