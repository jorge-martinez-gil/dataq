# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2307.15464, 2023

@author: Jorge Martinez-Gil
"""

import sys
from rdflib import Graph, Namespace, URIRef, Literal
import time

def replace_attribute_value(rdf_data, subject, predicate, old_value, new_value):
    """
    Replaces an attribute value in RDF data with a new value.

    Parameters:
    rdf_data (str): The RDF data to modify.
    subject (str): The subject of the triple to modify.
    predicate (str): The predicate of the triple to modify.
    old_value (str): The old value of the triple to modify.
    new_value (str): The new value to replace the old value with.

    Returns:
    str: The modified RDF data.
    """
    g = Graph().parse(data=rdf_data, format='turtle')
    ns = Namespace("http://example.org/")
    for s, p, o in g.triples((URIRef(ns + subject), URIRef(ns + predicate), Literal(old_value))):
        g.set((s, p, Literal(new_value)))
    return g.serialize(format='turtle')

def check_scalability(rdf_data):
    """
    Checks if the replace_attribute_value function is scalable.

    Parameters:
    rdf_data (str): The RDF data to test.

    Returns:
    str: 'scalable' if the function is scalable, 'non-scalable' otherwise.
    """
    # Small RDF data set
    rdf_data_small = """
    @prefix ex: <http://example.org/> .
    ex:subject1 ex:predicate1 "old_value" .
    """

    # Large RDF data set
    g = Graph().parse(data=rdf_data, format='turtle')
    size = len(g)

    # Time the execution of the function for the small RDF data set
    start_time = time.time()
    replace_attribute_value(rdf_data_small, "subject1", "predicate1", "old_value", "new_value")
    end_time = time.time()
    small_data_time = (end_time - start_time)/1

    # Time the execution of the function for the large RDF data set
    start_time = time.time()
    replace_attribute_value(rdf_data, "subject1", "predicate1", "old_value", "new_value")
    end_time = time.time()
    large_data_time = (end_time - start_time)/size

    # Compare the two times
    if large_data_time < small_data_time * 10:
        return 'scalable'
    else:
        return 'non-scalable'

"""
Reads a Data Catalog, replaces an attribute value, and checks if the catalog is scalable.

Usage: python check_scalability.py filepath
"""
def main():

    # Get path to Data Catalog from command line argument
    if len(sys.argv) < 2:
        print("Usage: python check_scalability.py filepath")
        sys.exit(1)

    rdf_data_path = sys.argv[1]

    # Load RDF data from file
    with open(rdf_data_path, "r") as f:
        rdf_data = f.read()

    result = check_scalability(rdf_data)
    print(f"The data catalog {rdf_data_path} is {result}.")


if __name__ == "__main__":
    main()