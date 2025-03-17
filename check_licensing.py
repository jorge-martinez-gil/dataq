# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d] Framework to Automatically Determine the Quality of Open Data Catalogs,
arXiv preprint arXiv:2307.15464, 2023

This script calculates the percentage of datasets (of type dcat:Dataset) that have a license 
defined (using dcterms:license) in the provided RDF data. The RDF data can be loaded from a local 
file or a URL.

Usage:
    python check_licensing.py <file_or_url>

Example:
    python check_licensing.py data.ttl
    python check_licensing.py http://example.com/data.ttl

@author: Jorge Martinez-Gil
"""

import sys
from rdflib import Graph, RDF, Namespace

# Define the RDF namespaces
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
dcterms = Namespace("http://purl.org/dc/terms/")
prov = Namespace("http://www.w3.org/ns/prov#")

def check_licensing(rdf_data: str, rdf_format: str = "turtle") -> float:
    """
    Check the licensing of an RDF data string and return the percentage of datasets 
    (dcat:Dataset) that have a license (dcterms:license).

    Args:
        rdf_data (str): The RDF data string to check.
        rdf_format (str): The format of the RDF data (default: "turtle").

    Returns:
        float: The percentage of datasets that have a license, between 0 and 100.
    """
    graph = Graph()
    try:
        graph.parse(data=rdf_data, format=rdf_format)
    except Exception as e:
        print(f"Error parsing RDF data: {e}")
        return 0.0

    licensed_items = 0
    total_items = 0

    # Iterate through all datasets in the RDF graph
    for subject in graph.subjects(RDF.type, dcat.Dataset):
        total_items += 1
        # Check if the dataset has a license defined using dcterms:license
        if any(graph.triples((subject, dcterms.license, None))):
            licensed_items += 1

    if total_items == 0:
        print("No datasets found in the RDF data.")
        return 0.0

    return (licensed_items / total_items) * 100

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
            import requests
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
    if len(sys.argv) < 2:
        print("Usage: python check_licensing.py <file_or_url>")
        sys.exit(1)

    rdf_data_source = sys.argv[1]
    rdf_data = load_rdf_data(rdf_data_source)
    result = check_licensing(rdf_data)
    print(f"The licensing of '{rdf_data_source}' is {result:.2f}%.")

if __name__ == "__main__":
    main()

