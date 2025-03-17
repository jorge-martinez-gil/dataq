# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d] Framework to Automatically Determine the Quality of Open Data Catalogs,
arXiv preprint arXiv:2307.15464, 2023

This script provides a tool for evaluating the overall quality of an open data catalog by analyzing its RDF data.
It computes several quality metrics based on the structure and content of the RDF data, including:

    - Broken Links: Checks the percentage of links in the RDF graph that are broken.
    - Duplicated Datasets/Distributions: Determines the percentage of duplicate items based on specific properties.
    - Completeness: Assesses the presence of core properties for catalog elements, using either DCAT or DCT vocabularies.

The overall accuracy of the data catalog is computed using the formula:
    
    Accuracy = 100 - (average error percentage)

where the error percentage is derived from:
    - Missing core properties (100 - completeness)
    - Duplicated datasets or distributions
    - Broken links

Key functionalities:
    - Load RDF data from either a local file or a URL.
    - Parse the RDF data (assumed to be in Turtle format) using rdflib.
    - Evaluate and display quality metrics separately for both DCAT and DCT property sets.

Usage:
    python check_accuracy.py <filepath_or_url>

Examples:
    python check_accuracy.py data/catalog.ttl
    python check_accuracy.py http://example.com/catalog.ttl

@author: Jorge Martinez-Gil
"""

import sys
from collections import defaultdict
from rdflib import Graph, RDF, Namespace, URIRef
import requests

# Define some RDF prefixes
dcat = Namespace("http://www.w3.org/ns/dcat#")
dct = Namespace("http://purl.org/dc/terms/")
rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# Example DCT properties (you can adjust as needed)
dct_properties = [
    dct.title,
    dct.identifier,
    dct.description
]

def check_links(rdf_data, timeout=5):
    """
    Checks the links in an RDF graph to see if they are broken.

    Args:
        rdf_data (str): The RDF data to check for broken links.
        timeout (int): The timeout in seconds for HTTP requests.

    Returns:
        float: The percentage of broken links in the RDF data.
    """
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    
    # Count occurrences of each URIRef to avoid checking duplicates
    link_counts = defaultdict(int)
    for _, _, o in graph:
        if isinstance(o, URIRef):
            link_counts[str(o)] += 1

    total_links = sum(link_counts.values())
    broken_links = 0

    session = requests.Session()
    for url, count in link_counts.items():
        try:
            response = session.get(url, timeout=timeout)
            if response.status_code != 200:
                broken_links += count
        except requests.exceptions.RequestException:
            broken_links += count

    if total_links == 0:
        print("No links found in the RDF data.")
        return 0
    else:
        percentage_broken = (broken_links / total_links) * 100
        print(f"{percentage_broken:.2f}% of links are broken.")
        return percentage_broken


def calculate_duplicates(rdf_data):
    """
    Calculates the percentage of duplicated datasets or distributions in a Data Catalog.

    Args:
        rdf_data (str): The RDF data to check for duplicates.

    Returns:
        float: The percentage of duplicated datasets or distributions in the RDF data.
    """
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")

    duplicates = defaultdict(int)
    # Check for duplicates in dcat.title and dcat.downloadURL
    for s, p, o in graph.triples((None, None, None)):
        if p == dcat.title or p == dcat.downloadURL:
            duplicates[o] += 1

    total_items = len(duplicates)
    duplicates_count = sum(1 for count in duplicates.values() if count > 1)
    if total_items == 0:
        print("No datasets or distributions found in the RDF data.")
        return 0
    else:
        percentage_duplicates = (duplicates_count / total_items) * 100
        print(f"{percentage_duplicates:.2f}% of datasets or distributions are duplicated.")
        return percentage_duplicates


def calculate_completeness(graph, subject, required_properties):
    """
    Calculates the completeness of a subject in an RDF graph by checking if it has all the required properties.

    Args:
        graph (rdflib.Graph): The RDF graph to check for completeness.
        subject (rdflib.term.URIRef): The subject to check for completeness.
        required_properties (list): The list of required properties.

    Returns:
        float: The completeness percentage.
    """
    present_properties = set()
    for predicate, _ in graph.predicate_objects(subject):
        if predicate in required_properties:
            present_properties.add(predicate)
    return (len(present_properties) / len(required_properties)) * 100


def core_links(rdf_data, property_set):
    """
    Calculates the completeness (core properties present) of a Data Catalog.

    Args:
        rdf_data (str): The RDF data to check for core properties.
        property_set (str): The property set to use ('dcat' or 'dct').

    Returns:
        float: The percentage of core properties that are present.
    """
    if property_set == 'dct':
        required_properties = dct_properties
    else:
        # Using dcat.title and rdf:type as required for 'dcat'
        required_properties = [dcat.title, rdf_ns.type]

    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    completeness_scores = []

    for subject_type in [dcat.Catalog, dcat.Dataset, dcat.Distribution]:
        for subject in graph.subjects(RDF.type, subject_type):
            completeness_score = calculate_completeness(graph, subject, required_properties)
            completeness_scores.append(completeness_score)

    if not completeness_scores:
        print("No subjects found for the given types in the RDF data.")
        return 0

    result = sum(completeness_scores) / len(completeness_scores)
    print(f"{result:.2f}% of core properties are present using {property_set.upper()} properties.")
    return result


def check_accuracy(rdf_data, property_set):
    """
    Calculates the overall accuracy of a Data Catalog file by combining three error metrics:
    - Missing core properties (derived as 100 - completeness)
    - Duplicated datasets or distributions
    - Broken links

    The final accuracy is computed as:
        Accuracy = 100 - (average error percentage)

    Args:
        rdf_data (str): The RDF data to check for accuracy.
        property_set (str): The property set to use ('dcat' or 'dct').

    Returns:
        float: The overall accuracy percentage of the RDF data file.
    """
    completeness_percentage = core_links(rdf_data, property_set)
    missing_core_percentage = 100 - completeness_percentage
    duplicates_percentage = calculate_duplicates(rdf_data)
    broken_links_percentage = check_links(rdf_data)
    
    avg_error = (missing_core_percentage + duplicates_percentage + broken_links_percentage) / 3
    accuracy = 100 - avg_error
    return accuracy


def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python check_accuracy.py filepath_or_url")
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

        # Compute accuracy for both property sets
        print("\nCalculating accuracy using DCAT properties:")
        accuracy_dcat = check_accuracy(rdf_data, 'dcat')
        print(f"\nThe overall accuracy of {rdf_data_path} using DCAT properties is {accuracy_dcat:.2f}%.")

        print("\nCalculating accuracy using DCT properties:")
        accuracy_dct = check_accuracy(rdf_data, 'dct')
        print(f"\nThe overall accuracy of {rdf_data_path} using DCT properties is {accuracy_dct:.2f}%.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

