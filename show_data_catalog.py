# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2305.035xx, 2023

@author: Jorge Martinez-Gil
"""

import sys
from rdflib import Graph

def parse_rdf_data(rdf_data: str) -> dict:
    """
    Parses RDF data into a dictionary.

    Args:
        rdf_data: A string containing RDF data in Turtle format.

    Returns:
        A dictionary containing the RDF triples.
    """
    # Load RDF data into graph
    graph = Graph().parse(data=rdf_data, format="turtle")

    # Create a dictionary to store the RDF triples
    rdf_dict = {}

    # Iterate through the RDF triples and add them to the dictionary
    for subject, predicate, obj in graph:
        subject = str(subject)
        predicate = str(predicate)
        obj = str(obj)

        if subject not in rdf_dict:
            rdf_dict[subject] = {}

        if predicate not in rdf_dict[subject]:
            rdf_dict[subject][predicate] = []

        rdf_dict[subject][predicate].append(obj)

    return rdf_dict

"""
This program provides a function for printing a DCAT data catalog.

Usage:
    python show_data_catalog.py catalog.ttl

The function `parse_rdf_data` takes an RDF data string as input and returns a dictionary
containing the RDF triples.

"""
def main():
    # Get path to Data Catalog from command line argument
    if len(sys.argv) < 2:
        print("Usage: python show_data_catalog.py catalog.ttl")
        sys.exit(1)

    rdf_data_path = sys.argv[1]

    # Load RDF data from file
    with open(rdf_data_path, "r") as f:
        rdf_data = f.read()

    # Parse RDF data into dictionary
    rdf_dict = parse_rdf_data(rdf_data)

    # Print the dictionary
    for subject, data in rdf_dict.items():
        print(subject)
        for predicate, objects in data.items():
            print(f"  {predicate}: {objects}")

if __name__ == "__main__":
    main()