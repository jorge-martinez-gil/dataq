# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2307.15464, 2023

@author: Jorge Martinez-Gil
"""
import sys
from rdflib import Graph, Namespace, RDF

def check_consistency(rdf_data: str, entity_type: str) -> float:
    """
    Checks if there are inconsistencies in the attribute values for a specific entity type.

    Args:
        rdf_data: A string containing RDF data in Turtle format.
        entity_type: The type of entity to compare (e.g. "catalog", "dataset", "distribution").

    Returns:
        A float representing the percentage of (subject, predicate) pairs that have inconsistent attribute values for the specified entity type.
    """
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")

    contradictions = set()

    # Define namespaces for RDF and DCAT
    RDF_NS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    DCAT_NS = Namespace("http://www.w3.org/ns/dcat#")

    # Query the RDF graph for entities of the specified type
    if entity_type == "catalog":
        entities = graph.subjects(RDF.type, DCAT_NS.Catalog)
    elif entity_type == "dataset":
        entities = graph.subjects(RDF.type, DCAT_NS.Dataset)
    elif entity_type == "distribution":
        entities = graph.subjects(RDF.type, DCAT_NS.Distribution)
    else:
        raise ValueError(f"Invalid entity type: {entity_type}")

    # Iterate through the entities and check for inconsistencies in their attribute values
    for entity in entities:
        subjects_predicates = {}  # Dictionary to store (subject, predicate) pairs and their corresponding objects

        # Iterate through the triples in the RDF graph for the entity and store (subject, predicate) pairs and their objects
        for subj, pred, obj in graph.triples((entity, None, None)):
            if (subj, pred) in subjects_predicates:
                objects = subjects_predicates[(subj, pred)]
                if obj not in objects:
                    contradictions.add((subj, pred))
                objects.append(obj)
            else:
                subjects_predicates[(subj, pred)] = [obj]

    # Calculate the percentage of inconsistencies
    total_pairs = len(subjects_predicates)
    inconsistent_pairs = len(contradictions)
    percentage = (inconsistent_pairs / total_pairs) * 100

    return percentage

"""
This program checks the consistency of a Data Catalog for a specific entity type.

Usage:
    python check_consistency.py cataglog.ttl entity_type

The function `check_consistency` takes an RDF data string and an entity type as input and returns a set of (subject, predicate) pairs that have inconsistent attribute values for the specified entity type.
"""

def main():
    try:
        # Get path to Data Catalog and entity type from command line arguments
        if len(sys.argv) < 3:
            print("Usage: python check_consistency.py filepath entity_type")
            sys.exit(1)

        rdf_data_path = sys.argv[1]
        entity_type = sys.argv[2]

        # Load RDF data from file
        with open(rdf_data_path, "r") as f:
            rdf_data = f.read()

        result = check_consistency(rdf_data, entity_type)
        print(f"The percentage of inconsistencies in {rdf_data_path} for {entity_type} is {result:.2f}%.")

    except FileNotFoundError:
        print(f"File not found: {rdf_data_path}")
        sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()