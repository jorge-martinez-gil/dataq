# -*- coding: utf-8 -*-
"""
[Martinez-Gil2025] Jorge Martinez-Gil: Framework to automatically determine the quality of open data catalogs. Expert Syst. Appl. 289: 128379 (2025).

This script provides a tool to evaluate the completeness of RDF-based data catalogs by analyzing
the presence of core properties defined by either the DCAT or DCT vocabularies. It processes RDF
data (in Turtle format) from a local file or URL, computes completeness scores for catalog elements 
(such as Catalog, Dataset, and Distribution), and displays the average completeness percentage.

Key functionalities:
    - Load RDF data from a local file or a URL.
    - Parse RDF data using rdflib.
    - Calculate completeness scores based on required properties from DCAT or DCT property sets.
    - Evaluate and display the average completeness of the catalog using both property sets.

Usage:
    python check_completeness.py <filepath_or_url>

Examples:
    python check_completeness.py data/catalog.ttl
    python check_completeness.py https://example.com/catalog.ttl

@author: Jorge Martinez-Gil
"""
import sys
import requests
from rdflib import Graph, RDF, Namespace
from typing import List

# Define some RDF prefixes
dcat = Namespace("http://www.w3.org/ns/dcat#")
dct = Namespace("http://purl.org/dc/terms/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# DCAT properties
dcat_properties = [
    dcat.title,
    dcat.downloadURL,
    dcat.size
]

# DCT properties
dct_properties = [
    dct.title,
    dct.identifier,
    dct.description
]


def calculate_completeness(graph: Graph, subject, required_properties: List) -> float:
    """
    Calculates the completeness of a subject based on the presence of required properties.
    
    Args:
        graph (Graph): The RDF graph.
        subject: The RDF subject to evaluate.
        required_properties (List): A list of required property URIs.
    
    Returns:
        float: The completeness percentage for the subject.
    """
    present_properties = set()
    for predicate, _ in graph.predicate_objects(subject):
        if predicate in required_properties:
            present_properties.add(predicate)
    return (len(present_properties) / len(required_properties)) * 100


def check_completeness(rdf_data: str, property_set: str, rdf_format: str = "turtle") -> float:
    """
    Checks the completeness of RDF data by evaluating the presence of core properties
    for subjects of types Catalog, Dataset, and Distribution.
    
    Args:
        rdf_data (str): The RDF data as a string.
        property_set (str): The property set to use ('dcat' or 'dct').
        rdf_format (str): The RDF format (default: "turtle").
    
    Returns:
        float: The average completeness percentage across evaluated subjects.
    """
    property_set = property_set.lower()
    required_properties = dct_properties if property_set == 'dct' else dcat_properties

    graph = Graph()
    try:
        graph.parse(data=rdf_data, format=rdf_format)
    except Exception as e:
        print(f"Error parsing RDF data: {e}")
        return 0.0

    completeness_scores = []
    for subject_type in [dcat.Catalog, dcat.Dataset, dcat.Distribution]:
        for subject in graph.subjects(RDF.type, subject_type):
            score = calculate_completeness(graph, subject, required_properties)
            completeness_scores.append(score)

    if not completeness_scores:
        print("No subjects found for the given types in the RDF data.")
        return 0.0

    return sum(completeness_scores) / len(completeness_scores)


def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python check_completeness.py filepath_or_url")
            sys.exit(1)

        rdf_data_path = sys.argv[1]
        rdf_data = ""

        # Determine if rdf_data_path is a URL or a local file
        if rdf_data_path.startswith("http://") or rdf_data_path.startswith("https://"):
            try:
                response = requests.get(rdf_data_path, timeout=10)
                response.raise_for_status()
                rdf_data = response.text
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL {rdf_data_path}: {e}")
                sys.exit(1)
        else:
            try:
                with open(rdf_data_path, "r", encoding="utf-8") as f:
                    rdf_data = f.read()
            except FileNotFoundError:
                print(f"File not found: {rdf_data_path}")
                sys.exit(1)
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")
                sys.exit(1)

        # Compute completeness for both property sets
        print("Calculating completeness using DCAT properties:")
        completeness_dcat = check_completeness(rdf_data, 'dcat')
        print(f"The completeness of '{rdf_data_path}' using DCAT properties is {completeness_dcat:.2f}%.\n")

        print("Calculating completeness using DCT properties:")
        completeness_dct = check_completeness(rdf_data, 'dct')
        print(f"The completeness of '{rdf_data_path}' using DCT properties is {completeness_dct:.2f}%.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

