#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d] Framework to Automatically Determine the Quality of Open Data Catalogs,
arXiv preprint arXiv:2307.15464, 2023

This script calculates the average readability score (Flesch-Kincaid grade level) for 
datasets in RDF data. For each dataset (of type dcat:Dataset), it computes the score 
for the title (dcat:title) and description (dcterms:description) using textstat, and 
then averages these scores. The RDF data can be loaded from a local file or a URL.

Usage:
    python check_readability.py <file_or_url>

Example:
    python check_readability.py data.ttl
    python check_readability.py http://example.com/data.ttl

@author: Jorge Martinez-Gil
"""

import sys
import requests
from rdflib import Graph, RDF, Namespace
import textstat

# Define the RDF namespaces
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
dcterms = Namespace("http://purl.org/dc/terms/")
prov = Namespace("http://www.w3.org/ns/prov#")


def check_readability(rdf_data: str, rdf_format: str = "turtle") -> float:
    """
    Calculates the average Flesch-Kincaid readability score for all datasets in the RDF data.
    
    For each dataset (of type dcat:Dataset), the function calculates the readability score 
    for the title (dcat:title) and the description (dcterms:description), if available.

    Parameters:
        rdf_data (str): RDF data in Turtle format.
        rdf_format (str): The format of the RDF data (default is "turtle").

    Returns:
        float: The average readability score for all datasets, or 0 if no datasets are found.
    """
    graph = Graph()
    try:
        graph.parse(data=rdf_data, format=rdf_format)
    except Exception as e:
        print(f"Error parsing RDF data: {e}")
        return 0.0

    readability_scores = []
    for subject in graph.subjects(RDF.type, dcat.Dataset):
        # Get the title and description values
        title = graph.value(subject, dcat.title)
        description = graph.value(subject, dcterms.description)
        if title:
            try:
                title_score = textstat.flesch_kincaid_grade(str(title))
                readability_scores.append(title_score)
            except Exception as e:
                print(f"Error calculating readability for title '{title}': {e}")
        if description:
            try:
                description_score = textstat.flesch_kincaid_grade(str(description))
                readability_scores.append(description_score)
            except Exception as e:
                print(f"Error calculating readability for description '{description}': {e}")

    if readability_scores:
        return sum(readability_scores) / len(readability_scores)
    return 0.0


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
            print(f"Unicode decode error for file '{source}': {e}")
            sys.exit(1)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python check_readability.py <file_or_url>")
        sys.exit(1)

    rdf_data_source = sys.argv[1]
    rdf_data = load_rdf_data(rdf_data_source)
    result = check_readability(rdf_data)
    print(f"The average readability score of '{rdf_data_source}' is {result:.2f}.")


if __name__ == "__main__":
    main()
