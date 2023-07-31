# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2307.15464, 2023

@author: Jorge Martinez-Gil
"""

import sys
from rdflib import Graph, RDF, Namespace

# Define some RDF prefixes
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

def check_completeness(rdf_data: str) -> float:
    """
    Checks the completeness of RDF data.

    Args:
        rdf_data: A string containing RDF data in Turtle format.

    Returns:
        A completeness score between 0 and 100.
    """
    required_properties = [
        dcat.title,
        dcat.downloadURL,
        dcat.size
    ]
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    completeness_scores = []
    for catalog in graph.subjects(RDF.type, dcat.Catalog):
        catalog_completeness = calculate_completeness(graph, catalog, required_properties)
        completeness_scores.append(catalog_completeness)
    for dataset in graph.subjects(RDF.type, dcat.Dataset):
        dataset_completeness = calculate_completeness(graph, dataset, required_properties)
        completeness_scores.append(dataset_completeness)
    for distribution in graph.subjects(RDF.type, dcat.Distribution):
        distribution_completeness = calculate_completeness(graph, distribution, required_properties)
        completeness_scores.append(distribution_completeness)
    return sum(completeness_scores) / len(completeness_scores)

def calculate_completeness(graph, subject, required_properties):
    """
    Calculates the completeness of a catalog.

    Args:
        graph: An RDF graph containing the subject.
        subject: An RDF subject to calculate completeness for.
        required_properties: A list of required RDF properties.

    Returns:
        A completeness score between 0 and 100.
    """
    present_properties = set()
    for predicate, obj in graph.predicate_objects(subject):
        if predicate in required_properties:
            present_properties.add(predicate)
    return len(present_properties) / len(required_properties) * 100

"""
This program checks the completeness of a Data Catalog.

Usage:
    python check_completeness.py catalog.ttl

The function `check_completeness` takes an RDF data string as input and returns a completeness score
between 0 and 100. The score represents the percentage of required properties that are present in the data.
"""
def main():
    # Get path to RDF data file from command line argument
    if len(sys.argv) < 2:
        print("Usage: python check_completeness.py filepath")
        sys.exit(1)

    rdf_data_path = sys.argv[1]

    # Load RDF data from file
    with open(rdf_data_path, "r") as f:
        rdf_data = f.read()

    result = check_completeness(rdf_data)
    print(f"The completeness of {rdf_data_path} is {result:.2f}%.")
    
    
if __name__ == "__main__":
    main()