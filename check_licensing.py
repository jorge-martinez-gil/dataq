# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2307.15464, 2023

@author: Jorge Martinez-Gil
"""
import sys
from rdflib import Graph, RDF, Namespace

# Define the RDF namespaces
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
dcterms = Namespace("http://purl.org/dc/terms/")
prov = Namespace("http://www.w3.org/ns/prov#")


def check_licensing(rdf_data):
    """
    Check the licensing of an RDF data string and return the percentage of datasets that have a license.

    Args:
        rdf_data (str): The RDF data string to check.

    Returns:
        float: The percentage of datasets that have a license, between 0 and 100.
    """
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    
    # Count licensed items and total items in all datasets
    licensed_items = 0
    total_items = 0
    for subject in graph.subjects(RDF.type, dcat.Dataset):
        for s, p, o in graph.triples((subject, dcterms.license, None)):
            licensed_items += 1
        total_items += 1
    
    # Calculate percentage of licensed items
    if total_items == 0:
        return 0
    else:
        return licensed_items / total_items * 100

"""
This program checks the licensing of a Data Catalog.

Usage: python check_licensing.py filepath
"""
def main():

    # Get path to RDF data file from command line argument
    if len(sys.argv) < 2:
        print("Usage: python check_licensing.py filepath")
        sys.exit(1)

    rdf_data_path = sys.argv[1]

    # Load RDF data from file
    with open(rdf_data_path, "r") as f:
        rdf_data = f.read()

    result = check_licensing(rdf_data)
    print(f"The licensing of {rdf_data_path} is {result}.")
    
    
if __name__ == "__main__":
    main()