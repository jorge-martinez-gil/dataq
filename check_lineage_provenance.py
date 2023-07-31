# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2307.15464, 2023

@author: Jorge Martinez-Gil
"""

import sys
from rdflib import Graph, RDF, RDFS, Namespace

# Define the RDF namespaces
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
dcterms = Namespace("http://purl.org/dc/terms/")
prov = Namespace("http://www.w3.org/ns/prov#")

def check_lineage_provenance(rdf_data):
    """
    Calculates the lineage and provenance score for an RDF graph.

    Parameters:
    rdf_data (str): The RDF data in Turtle format.

    Returns:
    float: The lineage and provenance score as a percentage.
    """
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    
    # Check for lineage information
    has_lineage_info = False
    for s, p, o in graph.triples((None, None, None)):
        if p == RDFS.subClassOf or p == RDFS.subPropertyOf:
            has_lineage_info = True
            break
    
    # Check for ancestors and descendants
    has_ancestors = False
    has_descendants = False
    for s, p, o in graph.triples((None, RDFS.subClassOf, None)):
        has_ancestors = True
        break
    for s, p, o in graph.triples((None, RDFS.subClassOf, None)):
        has_descendants = True
        break
    
    # Check for provenance information
    has_provenance_info = False
    for s, p, o in graph.triples((None, RDF.type, prov.Entity)):
        has_provenance_info = True
        break
    
    # Check for data sources and data processing steps
    has_data_sources = False
    has_data_processing_steps = False
    for s, p, o in graph.triples((None, RDF.type, prov.Activity)):
        for s2, p2, o2 in graph.triples((s, prov.used, None)):
            has_data_sources = True
            break
        for s2, p2, o2 in graph.triples((s, prov.wasAssociatedWith, None)):
            has_data_processing_steps = True
            break
    
    # Calculate lineage and provenance scores
    lineage_score = 0
    if has_lineage_info:
        lineage_score += 1.67
    if has_ancestors:
        lineage_score += 1.67
    if has_descendants:
        lineage_score += 1.67
    
    provenance_score = 0
    if has_provenance_info:
        provenance_score += 1.67
    if has_data_sources:
        provenance_score += 1.67
    if has_data_processing_steps:
        provenance_score += 1.67
    
    # Calculate average scores
    if lineage_score == 0 and provenance_score == 0:
        return 0
    else:
        return (lineage_score + provenance_score) * 10

"""
This program parses the command line arguments and calculates the lineage and provenance score for the specified Data Catalog.

Usage: python check_lineage_provenance.py filepath
"""
def main():

    # Get path to RDF data file from command line argument
    if len(sys.argv) < 2:
        print("Usage: python check_lineage_provenance.py filepath")
        sys.exit(1)

    rdf_data_path = sys.argv[1]

    # Load RDF data from file
    with open(rdf_data_path, "r") as f:
        rdf_data = f.read()

    result = check_lineage_provenance(rdf_data)
    print(f"The lineage and provenance {rdf_data_path} is {result}%.")
    
    
if __name__ == "__main__":
    main()