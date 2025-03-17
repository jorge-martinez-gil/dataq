# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d] Framework to Automatically Determine the Quality of Open Data Catalogs,
arXiv preprint arXiv:2307.15464, 2023

This script provides a tool to assess the compatibility between two RDF-based Data Catalogs.
Compatibility is defined as the percentage of triples from the first catalog that are also present
in the second catalog. This metric helps evaluate how similar or consistent two data catalogs are,
which can be useful for data integration, quality control, or migration processes.

Key functionalities:
    - Load RDF data from a local file or a URL for two separate catalogs.
    - Parse RDF data (in Turtle format by default) using rdflib.
    - Calculate the intersection of triples between the two RDF graphs.
    - Compute and display the compatibility percentage:
          (common triples in both catalogs / total triples in the first catalog) * 100.
    - Gracefully handle parsing errors and file or URL-related exceptions.

Usage:
    python check_compatibility.py <source1> <source2>

Examples:
    python check_compatibility.py data/catalog1.ttl data/catalog2.ttl
    python check_compatibility.py http://example.com/catalog1.ttl http://example.com/catalog2.ttl

@author: Jorge Martinez-Gil
"""

import sys
from rdflib import Graph
from typing import Optional
import requests


def load_rdf_data(source: str) -> str:
    """
    Loads RDF data from a given source, which can be a local file or a URL.

    Args:
        source (str): A URL (starting with 'http://' or 'https://') or a local file path.

    Returns:
        str: The RDF data as a string.

    Raises:
        Exception: If the source cannot be loaded.
    """
    if source.startswith("http://") or source.startswith("https://"):
        try:
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching URL {source}: {e}")
    else:
        try:
            with open(source, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading file {source}: {e}")


def check_compatibility(rdf_data: str, rdf_data2: str, rdf_format: str = "turtle") -> Optional[float]:
    """
    Checks the compatibility of two Data Catalogs by calculating the percentage of triples
    from the first catalog that are also present in the second catalog.

    Args:
        rdf_data (str): The first RDF data to check for compatibility.
        rdf_data2 (str): The second RDF data to check for compatibility.
        rdf_format (str): The format of the RDF data (default "turtle").

    Returns:
        Optional[float]: The percentage of triples in the first RDF data that are found in the second.
                         Returns None if the first graph contains no triples or if a parsing error occurs.
    """
    graph1 = Graph()
    graph2 = Graph()

    try:
        graph1.parse(data=rdf_data, format=rdf_format)
    except Exception as e:
        print(f"Error parsing first RDF data: {e}")
        return None

    try:
        graph2.parse(data=rdf_data2, format=rdf_format)
    except Exception as e:
        print(f"Error parsing second RDF data: {e}")
        return None

    # Calculate intersection of triples in both graphs
    triples1 = set(graph1)
    triples2 = set(graph2)
    common_triples = triples1.intersection(triples2)

    total_triples = len(triples1)
    if total_triples == 0:
        return None
    else:
        common_triples_count = len(common_triples)
        return (common_triples_count / total_triples) * 100


def main():
    """
    Main function to evaluate the compatibility between two RDF-based Data Catalogs.

    The function performs the following steps:
        - Ensures two sources (file paths or URLs) are provided as command-line arguments.
        - Loads RDF data from the specified sources.
        - Computes the compatibility percentage using the check_compatibility function.
        - Displays the result to the console.

    Usage:
        python check_compatibility.py <source1> <source2>
    """
    try:
        # Ensure two sources are provided
        if len(sys.argv) < 3:
            print("Usage: python check_compatibility.py <source1> <source2>")
            sys.exit(1)

        source1 = sys.argv[1]
        source2 = sys.argv[2]

        # Load RDF data from provided sources (file or URL)
        rdf_data = load_rdf_data(source1)
        rdf_data2 = load_rdf_data(source2)

        result = check_compatibility(rdf_data, rdf_data2)
        if result is None:
            print("No triples found in the first RDF data or a parsing error occurred.")
        else:
            print(f"The compatibility of '{source1}' and '{source2}' is {result:.2f}%.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

