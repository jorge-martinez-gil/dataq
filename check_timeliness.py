# -*- coding: utf-8 -*-
"""
[Martinez-Gil2025] Jorge Martinez-Gil: Framework to automatically determine the quality of open data catalogs. Expert Syst. Appl. 289: 128379 (2025).

This script checks the timeliness of a DCAT catalog in RDF data. A catalog is considered 
timely if its modification date (dcterms:modified) is within the last 365 days.
The RDF data can be loaded from a local file or a URL.

Usage:
    python check_timeliness.py <file_or_url>

Example:
    python check_timeliness.py data.ttl
    python check_timeliness.py http://example.com/data.ttl

@author: Jorge Martinez-Gil
"""

import sys
from datetime import datetime, timedelta
from rdflib import Graph, RDF, Namespace
import pytz
from typing import Optional
import requests

# Define RDF namespaces
dcat = Namespace("http://www.w3.org/ns/dcat#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf_ns = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
dcterms = Namespace("http://purl.org/dc/terms/")

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
            print(f"Error fetching RDF data from URL '{source}': {e}")
            sys.exit(1)
    else:
        try:
            with open(source, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"File not found: {source}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{source}': {e}")
            sys.exit(1)

def check_timeliness(rdf_data: str, rdf_format: str = "turtle") -> bool:
    """
    Checks the timeliness of an RDF data file containing a DCAT catalog.
    
    A catalog is considered timely if its modification date (dcterms:modified)
    is within the last 365 days.

    Args:
        rdf_data (str): The RDF data as a string.
        rdf_format (str): The RDF serialization format (default is "turtle").

    Returns:
        bool: True if the catalog is timely, False otherwise.
    """
    graph = Graph()
    try:
        graph.parse(data=rdf_data, format=rdf_format)
    except Exception as e:
        print(f"Error parsing RDF data: {e}")
        return False

    modified_date: Optional[str] = None

    # Retrieve the first modification date for a DCAT catalog in the graph
    for s, p, o in graph.triples((None, RDF.type, dcat.Catalog)):
        for s2, p2, o2 in graph.triples((s, dcterms.modified, None)):
            modified_date = str(o2)
            break
        if modified_date:
            break

    if not modified_date:
        print("No modification date found in the catalog.")
        return False

    try:
        # Parse the modification date (expects ISO 8601 format with timezone)
        parsed_date = datetime.strptime(modified_date, '%Y-%m-%dT%H:%M:%S%z')
    except Exception as e:
        print(f"Error parsing modified date '{modified_date}': {e}")
        return False

    one_year_ago = datetime.now(pytz.UTC) - timedelta(days=365)
    return parsed_date > one_year_ago

def main() -> None:
    """
    Main function that checks the timeliness of a DCAT catalog and prints the result.
    
    Usage:
        python check_timeliness.py <file_or_url>
    """
    if len(sys.argv) < 2:
        print("Usage: python check_timeliness.py <file_or_url>")
        sys.exit(1)

    rdf_data_source = sys.argv[1]
    rdf_data = load_rdf_data(rdf_data_source)
    timely = check_timeliness(rdf_data)
    print(f"The timeliness of '{rdf_data_source}' is {timely}.")

if __name__ == "__main__":
    main()

