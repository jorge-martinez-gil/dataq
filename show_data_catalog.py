# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d] Framework to Automatically Determine the Quality of Open Data Catalogs,
arXiv preprint arXiv:2307.15464, 2023

This module provides a command-line tool to load and parse RDF data from either a local file
or a URL. The RDF data is expected to be in Turtle format and is converted into a nested dictionary
structure for easier inspection. The tool is intended to help users quickly view the content of
an RDF data catalog by displaying each subject along with its associated predicates and objects.

Main functionalities:
    - Load RDF data from a URL or a local file.
    - Parse the RDF data into a dictionary where each subject is a key mapping to another dictionary
      containing predicates as keys and lists of object values.
    - Print the structured RDF data in a human-readable format to the console.

Usage:
    python show_data_catalog.py <file_or_url>

Examples:
    python show_data_catalog.py data/catalog.ttl
    python show_data_catalog.py http://example.com/catalog.ttl

@author: Jorge Martinez-Gil (improved version)
"""

import sys
import requests
from rdflib import Graph

def load_rdf_data(source: str) -> str:
    # Check if source is a URL
    if source.startswith("http"):
        response = requests.get(source)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    else:
        with open(source, "r", encoding="utf-8") as f:
            return f.read()

def parse_rdf_data(rdf_data: str) -> dict:
    graph = Graph().parse(data=rdf_data, format="turtle")
    rdf_dict = {}
    for subject, predicate, obj in graph:
        subject = str(subject)
        predicate = str(predicate)
        obj = str(obj)
        rdf_dict.setdefault(subject, {}).setdefault(predicate, []).append(obj)
    return rdf_dict

def main():
    if len(sys.argv) < 2:
        print("Usage: python show_data_catalog.py <file_or_url>")
        sys.exit(1)

    source = sys.argv[1]
    try:
        rdf_data = load_rdf_data(source)
    except Exception as e:
        print(f"Error loading RDF data: {e}")
        sys.exit(1)

    rdf_dict = parse_rdf_data(rdf_data)
    for subject, data in rdf_dict.items():
        print(subject)
        for predicate, objects in data.items():
            print(f"  {predicate}: {objects}")

if __name__ == "__main__":
    main()

