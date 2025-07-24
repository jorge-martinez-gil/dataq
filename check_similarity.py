# -*- coding: utf-8 -*-
"""
[Martinez-Gil2025] Jorge Martinez-Gil: Framework to automatically determine the quality of open data catalogs. Expert Syst. Appl. 289: 128379 (2025).

This script calculates the similarity between two DCAT catalogs in Turtle format based on their titles 
and descriptions. Similarity is computed using the Jaccard similarity between preprocessed texts.
The RDF data for each catalog can be loaded from a local file or a URL.

Usage:
    python check_similarity.py <source1> <source2>

Example:
    python check_similarity.py catalog1.ttl catalog2.ttl
    python check_similarity.py http://example.com/catalog1.ttl http://example.com/catalog2.ttl

@author: Jorge Martinez-Gil
"""

import sys
import requests
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from rdflib import Graph, Namespace
from typing import Set

# Download required NLTK resources quietly
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

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
        except UnicodeDecodeError as e:
            print(f"Unicode decode error for file '{source}': {e}")
            sys.exit(1)

def preprocess_text(text: str) -> Set[str]:
    """
    Preprocesses a text by tokenizing it into sentences and words, converting to lowercase, 
    and removing stopwords.

    Args:
        text (str): The text to preprocess.

    Returns:
        Set[str]: A set of preprocessed words.
    """
    # Tokenize the sentences and convert to lowercase
    sentences = sent_tokenize(text.lower())

    # Tokenize words in each sentence and remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        filtered_words = [word for word in words if word not in stop_words]
        tokens.extend(filtered_words)
    
    return set(tokens)

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """
    Calculates the Jaccard similarity between two sets.

    Args:
        set1 (Set[str]): The first set.
        set2 (Set[str]): The second set.

    Returns:
        float: The Jaccard similarity between the two sets.
    """
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0

def are_graphs_identical(g1: Graph, g2: Graph) -> bool:
    """
    Checks if two RDF graphs are identical.

    Args:
        g1 (Graph): The first RDF graph.
        g2 (Graph): The second RDF graph.

    Returns:
        bool: True if the graphs are identical, False otherwise.
    """
    return len(g1) == len(g2) and all(t in g2 for t in g1) and all(t in g1 for t in g2)

def check_similarity(source1: str, source2: str) -> float:
    """
    Calculates the similarity between two DCAT catalogs in Turtle format based on their titles 
    and descriptions. Similarity is computed using the Jaccard similarity between preprocessed texts.

    Args:
        source1 (str): The file path or URL for the first catalog.
        source2 (str): The file path or URL for the second catalog.

    Returns:
        float: The similarity between the two catalogs as a percentage.
    """
    # Load RDF data for both catalogs
    data1 = load_rdf_data(source1)
    data2 = load_rdf_data(source2)

    # Parse Turtle data into RDF graphs with error handling
    g1 = Graph()
    g2 = Graph()
    try:
        g1.parse(data=data1, format='ttl')
    except Exception as e:
        print(f"Error parsing {source1}: {e}")
        sys.exit(1)
    try:
        g2.parse(data=data2, format='ttl')
    except Exception as e:
        print(f"Error parsing {source2}: {e}")
        sys.exit(1)
    
    # If graphs are identical, return 100%
    if are_graphs_identical(g1, g2):
        return 100.0

    # Define DCAT namespace
    dcat = Namespace('http://www.w3.org/ns/dcat#')
    
    # Extract titles and descriptions from both catalogs
    titles1 = [str(title) for title in g1.objects(predicate=dcat.title)]
    titles2 = [str(title) for title in g2.objects(predicate=dcat.title)]
    
    descriptions1 = [str(desc) for desc in g1.objects(predicate=dcat.description)]
    descriptions2 = [str(desc) for desc in g2.objects(predicate=dcat.description)]
    
    # Preprocess titles and descriptions
    pre_titles1 = [preprocess_text(title) for title in titles1]
    pre_titles2 = [preprocess_text(title) for title in titles2]
    pre_desc1 = [preprocess_text(desc) for desc in descriptions1]
    pre_desc2 = [preprocess_text(desc) for desc in descriptions2]
    
    # Calculate Jaccard similarity for titles
    if pre_titles1 and pre_titles2:
        title_similarity = sum(
            jaccard_similarity(t1, t2) for t1 in pre_titles1 for t2 in pre_titles2
        ) / (len(pre_titles1) * len(pre_titles2))
    else:
        title_similarity = 0.0

    # Calculate Jaccard similarity for descriptions
    if pre_desc1 and pre_desc2:
        description_similarity = sum(
            jaccard_similarity(d1, d2) for d1 in pre_desc1 for d2 in pre_desc2
        ) / (len(pre_desc1) * len(pre_desc2))
    else:
        description_similarity = 0.0
    
    # Overall similarity is the average of title and description similarity
    overall_similarity = (title_similarity + description_similarity) / 2
    return overall_similarity * 100

def main() -> None:
    """
    Main function that calculates the similarity between two DCAT catalogs in Turtle format
    and prints the result.

    Usage:
        python check_similarity.py <source1> <source2>
    """
    if len(sys.argv) < 3:
        print("Usage: python check_similarity.py <source1> <source2>")
        sys.exit(1)

    source1 = sys.argv[1]
    source2 = sys.argv[2]

    similarity = check_similarity(source1, source2)
    print(f"The similarity of '{source1}' and '{source2}' is {similarity:.2f}%.")

if __name__ == "__main__":
    main()
