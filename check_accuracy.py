# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2307.15464, 2023

@author: Jorge Martinez-Gil
"""
import sys
from collections import defaultdict
from rdflib import Graph, RDF, Namespace, URIRef
import requests

# Define some RDF prefixes
dcat = Namespace("http://www.w3.org/ns/dcat#")
dct = Namespace("http://purl.org/dc/terms/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# Example DCT properties (you can adjust as needed)
dct_properties = [
    dct.title,
    dct.identifier,
    dct.description
]

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


def core_links(rdf_data, property_set):
    """
    Calculates the percentage of missing core properties in a Data Catalog.

    Args:
        rdf_data (str): The RDF data to check for missing core properties.
        property_set (str): The property set to use ('dcat' or 'dct').

    Returns:
        float: The percentage of missing core properties in the RDF data.
    """
    required_properties = dct_properties if property_set == 'dct' else [
        dcat.title,
        rdf.type
    ]
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    completeness_scores = []
    for subject_type in [dcat.Catalog, dcat.Dataset, dcat.Distribution]:
        for subject in graph.subjects(RDF.type, subject_type):
            completeness_score = calculate_completeness(graph, subject, required_properties)
            completeness_scores.append(completeness_score)
    result = sum(completeness_scores) / len(completeness_scores)
    print(f"{result}% of core properties are not present using {property_set.upper()} properties.")
    return result


def check_accuracy(rdf_data, property_set):
    """
    Calculates the accuracy of a Data Catalog file by averaging the percentages of broken links, duplicated datasets or distributions, and missing core properties.

    Args:
        rdf_data (str): The RDF data to check for accuracy.
        property_set (str): The property set to use ('dcat' or 'dct').

    Returns:
        float: The accuracy of the RDF data file.
    """
    core_result = core_links(rdf_data, property_set)
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
        if len(sys.argv) < 3:
            print("Usage: python check_accuracy.py filepath [dcat|dct]")
            sys.exit(1)

        rdf_data_path = sys.argv[1]
        property_set = sys.argv[2]

        if property_set not in ['dcat', 'dct']:
            print("Invalid property set. Choose 'dcat' or 'dct'.")
            sys.exit(1)

        with open(rdf_data_path, "r", encoding="utf-8") as f:
            rdf_data = f.read()

        result = check_accuracy(rdf_data, property_set)
        print(f"The accuracy of {rdf_data_path} using {property_set.upper()} properties is {result}%.")

    except FileNotFoundError:
        print(f"File not found: {rdf_data_path}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}")
        sys_exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()