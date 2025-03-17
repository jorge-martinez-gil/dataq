# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d] Framework to Automatically Determine the Quality of Open Data Catalogs,
arXiv preprint arXiv:2307.15464, 2023

This script calculates the consistency percentage (the percentage of (subject, predicate) pairs 
with a single, consistent attribute value) from RDF data in Turtle format. The RDF data can be 
provided from a local file or a URL. It considers all DCAT entities: Catalog, Dataset, and Distribution.

Usage:
    python check_consistency.py <file_or_url>
    
Example:
    python check_consistency.py data.ttl
    python check_consistency.py http://example.com/data.ttl

@author: Jorge Martinez-Gil
"""

import sys
import requests
from rdflib import Graph, Namespace, RDF

def check_consistency(rdf_data: str) -> float:
    """
    Checks consistency in the attribute values for all DCAT entities (Catalog, Dataset, Distribution).

    For each (subject, predicate) pair among these entities, if multiple distinct object 
    values are present, it is considered inconsistent. This function calculates the percentage 
    of consistent pairs (i.e., those with exactly one object value).

    Args:
        rdf_data: A string containing RDF data in Turtle format.

    Returns:
        A float representing the percentage of (subject, predicate) pairs that are consistent.
    """
    graph = Graph()
    try:
        graph.parse(data=rdf_data, format="turtle")
    except Exception as e:
        print(f"Error parsing RDF data: {e}")
        return 0.0

    # Define namespace for DCAT
    DCAT_NS = Namespace("http://www.w3.org/ns/dcat#")

    # Get all DCAT entities: Catalog, Dataset, and Distribution
    catalogs = set(graph.subjects(RDF.type, DCAT_NS.Catalog))
    datasets = set(graph.subjects(RDF.type, DCAT_NS.Dataset))
    distributions = set(graph.subjects(RDF.type, DCAT_NS.Distribution))
    all_entities = catalogs.union(datasets).union(distributions)

    # Aggregate all (subject, predicate) pairs and their object values
    all_pairs = {}
    for entity in all_entities:
        for subj, pred, obj in graph.triples((entity, None, None)):
            key = (subj, pred)
            if key in all_pairs:
                all_pairs[key].add(obj)
            else:
                all_pairs[key] = {obj}

    # Count inconsistencies: any (subject, predicate) pair with more than one distinct object
    inconsistent_pairs = sum(1 for objects in all_pairs.values() if len(objects) > 1)
    total_pairs = len(all_pairs)

    if total_pairs == 0:
        print("No (subject, predicate) pairs found for the DCAT entities.")
        return 0.0

    # Calculate consistency percentage: pairs with only one object value are consistent
    consistency_percentage = ((total_pairs - inconsistent_pairs) / total_pairs) * 100
    return consistency_percentage

def load_rdf_data(source: str) -> str:
    """
    Loads RDF data from a file or a URL.
    
    Args:
        source: A file path or a URL.
    
    Returns:
        The RDF data as a string.
    """
    if source.startswith("http://") or source.startswith("https://"):
        try:
            response = requests.get(source)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_consistency.py <file_or_url>")
        sys.exit(1)

    source = sys.argv[1]
    rdf_data = load_rdf_data(source)
    result = check_consistency(rdf_data)
    print(f"The consistency percentage in '{source}' is {result:.2f}%.")

if __name__ == "__main__":
    main()

