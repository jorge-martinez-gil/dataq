# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2305.035xx, 2023

@author: Jorge Martinez-Gil
"""
import sys
from collections import defaultdict
from rdflib import Graph, RDF, Namespace, URIRef
import requests

# Define some RDF prefixes
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

def check_links(rdf_data):
    """
    Checks the links in an RDF graph to see if they are broken.

    Args:
        rdf_data (str): The RDF data to check for broken links.

    Returns:
        float: The percentage of broken links in the RDF data.
    """
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    total_links = 0
    broken_links = 0
    for s, p, o in graph:
        if isinstance(o, URIRef):
            total_links += 1
            try:
                response = requests.get(o)
                if response.status_code != 200:
                    broken_links += 1
            except:
                broken_links += 1
    if total_links == 0:
        print("No links found in the RDF data.")
        return 0
    else:
        percentage_broken = (broken_links / total_links) * 100
        print(f"{percentage_broken}% of links are broken.")
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
        print(f"{percentage_duplicates}% of datasets or distributions are duplicated.")
        return percentage_duplicates


def core_links(rdf_data):
    """
    Calculates the percentage of missing core properties in a Data Catalog.

    Args:
        rdf_data (str): The RDF data to check for missing core properties.

    Returns:
        float: The percentage of missing core properties in the RDF data.
    """
    required_properties = [
        dcat.title,
        rdf.type
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
    result = sum(completeness_scores) / len(completeness_scores)
    print(f"{result}% of core properties are not present.")
    return result


def check_accuracy(rdf_data):
    """
    Calculates the accuracy of a Data Catalog file by averaging the percentages of broken links, duplicated datasets or distributions, and missing core properties.

    Args:
        rdf_data (str): The RDF data to check for accuracy.

    Returns:
        float: The accuracy of the RDF data file.
    """
    core_result = core_links(rdf_data)
    duplicates_result = calculate_duplicates(rdf_data)
    check_links_result = check_links(rdf_data)
    mean = (core_result + duplicates_result + check_links_result) / 3
    return mean
    
    
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
    for predicate, obj in graph.predicate_objects(subject):
        if predicate in required_properties:
            present_properties.add(predicate)
    return len(present_properties) / len(required_properties) * 100
    
"""
This program checks the accuracy of a Data Catalog by calculating the percentage of broken links, duplicated datasets or distributions, and missing core properties.

Usage: python check_accuracy.py filepath
"""
def main():
    try:
        # Get path to Data Catalog file from command line argument
        if len(sys.argv) < 2:
            print("Usage: python check_accuracy.py filepath")
            sys.exit(1)

        rdf_data_path = sys.argv[1]

        # Load RDF data from file
        with open(rdf_data_path, "r") as f:
            rdf_data = f.read()

        result = check_accuracy(rdf_data)
        print(f"The accuracy of {rdf_data_path} is {result}%.")

    except FileNotFoundError:
        print(f"File not found: {rdf_data_path}")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()