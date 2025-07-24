# -*- coding: utf-8 -*-
"""
[Martinez-Gil2025] Jorge Martinez-Gil: Framework to automatically determine the quality of open data catalogs. Expert Syst. Appl. 289: 128379 (2025).

This script provides two functionalities:
  1. replace_attribute_value: Replaces an attribute value in RDF data.
  2. check_scalability: Checks the scalability of the replacement function by comparing its
     execution time on a small RDF dataset versus a large one.

The RDF data can be loaded from either a local file or a URL.

Usage:
    python check_scalability.py <file_or_url>

Example:
    python check_scalability.py data.ttl
    python check_scalability.py http://example.com/data.ttl

@author: Jorge Martinez-Gil
"""

import sys
import time
import requests
from rdflib import Graph, Namespace, URIRef, Literal
from typing import Optional

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

def replace_attribute_value(
    rdf_data: str,
    subject: str,
    predicate: str,
    old_value: str,
    new_value: str,
    rdf_format: str = "turtle",
    base_ns: Optional[Namespace] = None
) -> str:
    """
    Replaces an attribute value in RDF data with a new value.

    Parameters:
        rdf_data (str): The RDF data to modify.
        subject (str): The subject (local name) of the triple to modify.
        predicate (str): The predicate (local name) of the triple to modify.
        old_value (str): The old value of the triple to modify.
        new_value (str): The new value to replace the old value with.
        rdf_format (str): The RDF serialization format (default is 'turtle').
        base_ns (Optional[Namespace]): The base namespace to use for subject and predicate.
                                       Defaults to Namespace("http://example.org/").

    Returns:
        str: The modified RDF data serialized in the given format.
    """
    if base_ns is None:
        base_ns = Namespace("http://example.org/")

    g = Graph()
    try:
        g.parse(data=rdf_data, format=rdf_format)
    except Exception as e:
        print(f"Error parsing RDF data: {e}")
        return rdf_data  # Return unmodified data if parsing fails

    subject_uri = URIRef(base_ns + subject)
    predicate_uri = URIRef(base_ns + predicate)

    # Replace matching triples with the new value
    for s, p, o in g.triples((subject_uri, predicate_uri, Literal(old_value))):
        g.set((s, p, Literal(new_value)))
    
    return g.serialize(format=rdf_format)

def check_scalability(rdf_data: str, rdf_format: str = "turtle") -> str:
    """
    Checks if the replace_attribute_value function is scalable by comparing its execution time
    on a small RDF dataset versus a large RDF dataset.

    Parameters:
        rdf_data (str): The large RDF data to test.
        rdf_format (str): The RDF serialization format (default is 'turtle').

    Returns:
        str: 'scalable' if the function is scalable, 'non-scalable' otherwise.
    """
    # Define a small RDF dataset for baseline timing
    rdf_data_small = """
    @prefix ex: <http://example.org/> .
    ex:subject1 ex:predicate1 "old_value" .
    """

    # Parse the large RDF data to determine its size (number of triples)
    g_large = Graph()
    try:
        g_large.parse(data=rdf_data, format=rdf_format)
    except Exception as e:
        print(f"Error parsing large RDF data: {e}")
        return "non-scalable"
    large_size = len(g_large)
    if large_size == 0:
        print("Large RDF data contains no triples.")
        return "non-scalable"

    # Time the function on the small dataset
    start_small = time.time()
    replace_attribute_value(rdf_data_small, "subject1", "predicate1", "old_value", "new_value", rdf_format)
    end_small = time.time()
    small_time = end_small - start_small

    # Time the function on the large dataset
    start_large = time.time()
    replace_attribute_value(rdf_data, "subject1", "predicate1", "old_value", "new_value", rdf_format)
    end_large = time.time()
    # Compute average time per triple for the large dataset
    large_time_per_triple = (end_large - start_large) / large_size

    # Define a threshold: if average time per triple for large data is less than 10 times
    # the total time for the small dataset, consider it scalable.
    if large_time_per_triple < small_time * 10:
        return 'scalable'
    else:
        return 'non-scalable'

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python check_scalability.py <file_or_url>")
        sys.exit(1)

    rdf_data_source = sys.argv[1]
    rdf_data = load_rdf_data(rdf_data_source)
    result = check_scalability(rdf_data)
    print(f"The data catalog '{rdf_data_source}' is {result}.")

if __name__ == "__main__":
    main()

