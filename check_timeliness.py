# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2305.035xx, 2023

@author: Jorge Martinez-Gil
"""
import sys
from datetime import datetime, timedelta
from rdflib import Graph, RDF, Namespace

# Define some RDF prefixes
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")

def check_timeliness(rdf_data):
    """
    Checks the timeliness of an RDF data file containing a DCAT catalog.

    Args:
        rdf_data (str): The RDF data as a string.

    Returns:
        bool: True if the catalog is timely, False otherwise.
    """
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    
    # Get the modified date of the catalog
    modified_date = None
    for s, p, o in graph.triples((None, RDF.type, dcat.Catalog)):
        for s2, p2, o2 in graph.triples((s, dcterms.modified, None)):
            modified_date = o2
            break
        break
    
    # Check if the modified date is within the last year
    if modified_date:
        modified_date = datetime.strptime(modified_date, '%Y-%m-%d')
        one_year_ago = datetime.now() - timedelta(days=365)
        if modified_date > one_year_ago:
            return True
    
    return False

"""
Program that checks the timeliness of a DCAT catalog.

Usage: python check_timeliness.py filepath
"""
def main():

    # Get path to RDF data file from command line argument
    if len(sys.argv) < 2:
        print("Usage: python check_timeliness.py filepath")
        sys.exit(1)

    rdf_data_path = sys.argv[1]

    # Load RDF data from file
    with open(rdf_data_path, "r") as f:
        rdf_data = f.read()

    result = check_timeliness(rdf_data)
    print(f"The timeliness {rdf_data_path} is {result}.")
       
if __name__ == "__main__":
    main()