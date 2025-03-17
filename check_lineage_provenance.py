#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d] Framework to Automatically Determine the Quality of Open Data Catalogs,
arXiv preprint arXiv:2307.15464, 2023

This script calculates the lineage and provenance score for an RDF graph.
The score is based on the presence of:
  - Lineage information (RDFS.subClassOf or RDFS.subPropertyOf)
  - Ancestor and descendant relationships (triples with RDFS.subClassOf)
  - Provenance information (instances of prov:Entity)
  - Data sources (prov:used) and data processing steps (prov:wasAssociatedWith) within prov:Activity

Each of the six criteria contributes approximately 1.67 points; the total is scaled to a percentage.

The RDF data can be loaded from a local file or a URL.

Usage:
    python check_lineage_provenance.py <file_or_url>

Example:
    python check_lineage_provenance.py data.ttl
    python check_lineage_provenance.py http://example.com/data.ttl

@author: Jorge Martinez-Gil
"""

import sys
from rdflib import Graph, RDF, RDFS, Namespace
from typing import Optional
import requests

# Define the RDF namespaces
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs_ns = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
dcterms = Namespace("http://purl.org/dc/terms/")
prov = Namespace("http://www.w3.org/ns/prov#")


def check_lineage_provenance(rdf_data: str, rdf_format: str = "turtle") -> float:
    """
    Calculates the lineage and provenance score for an RDF graph.

    The score is based on the presence of:
      - Lineage information (RDFS.subClassOf or RDFS.subPropertyOf)
      - Ancestor and descendant relationships (triples with RDFS.subClassOf)
      - Provenance information (instances of prov:Entity)
      - Data sources (prov:used) and data processing steps (prov:wasAssociatedWith) within prov:Activity

    Each of the six criteria contributes approximately 1.67 points; the total is scaled to a percentage.

    Parameters:
        rdf_data (str): The RDF data in Turtle format.
        rdf_format (str): The RDF serialization format (default is "turtle").

    Returns:
        float: The lineage and provenance score as a percentage.
    """
    graph = Graph()
    try:
        graph.parse(data=rdf_data, format=rdf_format)
    except Exception as e:
        print(f"Error parsing RDF data: {e}")
        return 0.0

    # Check for lineage information: any triple with RDFS.subClassOf or RDFS.subPropertyOf
    has_lineage_info = any(p in (RDFS.subClassOf, RDFS.subPropertyOf) for s, p, o in graph)

    # Check for ancestors and descendants (using the same condition here)
    has_ancestors = any(True for s, p, o in graph.triples((None, RDFS.subClassOf, None)))
    has_descendants = has_ancestors  # Both are determined by the same check

    # Check for provenance information: presence of any prov:Entity
    has_provenance_info = any(True for s, p, o in graph.triples((None, RDF.type, prov.Entity)))

    # Check for data sources (prov:used) and data processing steps (prov:wasAssociatedWith) within prov:Activity
    has_data_sources = False
    has_data_processing_steps = False
    for s, p, o in graph.triples((None, RDF.type, prov.Activity)):
        if not has_data_sources:
            has_data_sources = any(True for _ in graph.triples((s, prov.used, None)))
        if not has_data_processing_steps:
            has_data_processing_steps = any(True for _ in graph.triples((s, prov.wasAssociatedWith, None)))
        if has_data_sources and has_data_processing_steps:
            break

    # Calculate lineage score (three criteria)
    lineage_score = 0.0
    if has_lineage_info:
        lineage_score += 1.67
    if has_ancestors:
        lineage_score += 1.67
    if has_descendants:
        lineage_score += 1.67

    # Calculate provenance score (three criteria)
    provenance_score = 0.0
    if has_provenance_info:
        provenance_score += 1.67
    if has_data_sources:
        provenance_score += 1.67
    if has_data_processing_steps:
        provenance_score += 1.67

    total_score = lineage_score + provenance_score
    if total_score == 0:
        return 0.0
    else:
        # Scale the score to a percentage (approximate maximum of 100)
        return total_score * 10


def load_rdf_data(source: str) -> str:
    """
    Loads RDF data from a file or a URL.

    Args:
        source (str): A file path or a URL.

    Returns:
        str: The RDF data as a string.
    """
    if source.startswith("http://") or source.startswith("https://"):
        try:
            response = requests.get(source)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching RDF data from URL: {e}")
            sys.exit(1)
    else:
        try:
            with open(source, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"File not found: {source}")
            sys.exit(1)
        except UnicodeDecodeError as e:
            print(f"Unicode decode error: {e}")
            sys.exit(1)


def main() -> None:
    # Ensure a file path or URL is provided
    if len(sys.argv) < 2:
        print("Usage: python check_lineage_provenance.py <file_or_url>")
        sys.exit(1)

    rdf_data_source = sys.argv[1]
    rdf_data = load_rdf_data(rdf_data_source)
    result = check_lineage_provenance(rdf_data)
    print(f"The lineage and provenance score for '{rdf_data_source}' is {result:.2f}%.")


if __name__ == "__main__":
    main()
