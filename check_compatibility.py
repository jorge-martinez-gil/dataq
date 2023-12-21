# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2307.15464, 2023

@author: Jorge Martinez-Gil
"""
import sys
from rdflib import Graph

def check_compatibility(rdf_data, rdf_data2):
    """
    Checks the compatibility of two Data Catalogs by calculating the percentage of triples they have in common.

    Args:
        rdf_data (str): The first RDF data to check for compatibility.
        rdf_data2 (str): The second RDF data to check for compatibility.

    Returns:
        float: The percentage of triples the two Data Catalogs have in common.
    """
    graph1 = Graph()
    graph1.parse(data=rdf_data, format="turtle")
    
    graph2 = Graph()
    graph2.parse(data=rdf_data2, format="turtle")
    
    # Calculate intersection of triples in both graphs
    triples1 = set(graph1)
    triples2 = set(graph2)
    common_triples = triples1.intersection(triples2)
    
    # Calculate percentage of triples in common
    total_triples = len(triples1)
    if total_triples == 0:
        return None
    else:
        common_triples_count = len(common_triples)
        return (common_triples_count / total_triples) * 100

"""
This program checks the compatibility of two Data Catalogs by calculating the percentage of triples they have in common.

Usage: python check_compatibility.py filepath1 filepath2
"""
def main():
    try:
        # Get paths to RDF data files from command line arguments
        if len(sys.argv) < 3:
            print("Usage: python check_compatibility.py filepath1 filepath2")
            sys.exit(1)

        rdf_data_path = sys.argv[1]
        rdf_data_path2 = sys.argv[2]

        # Load RDF data from files
        with open(rdf_data_path, "r", encoding="utf-8") as f:
            rdf_data = f.read()
        
        with open(rdf_data_path2, "r", encoding="utf-8") as f:
            rdf_data2 = f.read()

        result = check_compatibility(rdf_data, rdf_data2)
        if result is None:
            print("No triples found in the RDF data.")
        else:
            print(f"The compatibility of {rdf_data_path} and {rdf_data_path2} is {result}%.")

    except FileNotFoundError:
        print(f"File not found: {rdf_data_path} or {rdf_data_path2}")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()