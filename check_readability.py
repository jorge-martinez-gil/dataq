# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2307.15464, 2023

@author: Jorge Martinez-Gil
"""

import sys
from rdflib import Graph, RDF, Namespace
import textstat

# Define the RDF namespaces
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
dcterms = Namespace("http://purl.org/dc/terms/")
prov = Namespace("http://www.w3.org/ns/prov#")

def check_readability(rdf_data):
    """
    Calculates the readability score for each dataset in the RDF data.
    
    Parameters:
        rdf_data (str): RDF data in turtle format
        
    Returns:
        float: the average readability score for all datasets in the RDF data, or 0 if there are no datasets
    """
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    
    # Calculate readability score for each dataset
    readability_scores = []
    for subject in graph.subjects(RDF.type, dcat.Dataset):
        title = graph.value(subject, dcat.title)
        description = graph.value(subject, dcterms.description)
        if title:
            # Calculate readability score for title
            title_score = textstat.flesch_kincaid_grade(title)
            readability_scores.append(title_score)
        if description:
            # Calculate readability score for description
            description_score = textstat.flesch_kincaid_grade(description)
            readability_scores.append(description_score)
            
    if len(readability_scores) > 0:
        average = sum(readability_scores) / len(readability_scores)
    else:
        average = 0
        
    return average

"""
Main function that loads Data Catalog from a file and calculates the readability score for the data.

Usage: python check_readability.py filepath
"""
def main():

    # Get path to RDF data file from command line argument
    if len(sys.argv) < 2:
        print("Usage: python check_readability.py filepath")
        sys.exit(1)

    rdf_data_path = sys.argv[1]

    # Load RDF data from file
    with open(rdf_data_path, "r", encoding="utf-8") as f:
        rdf_data = f.read()

    result = check_readability(rdf_data)
    print(f"The readability of {rdf_data_path} is {result}.")
    
    
if __name__ == "__main__":
    main()