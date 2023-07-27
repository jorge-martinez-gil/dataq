# -*- coding: utf-8 -*-
"""
[Martinez-Gil2023d]  Framework to Automatically Determine the Quality of Open Data Catalogs, arXiv preprint arXiv:2305.035xx, 2023

@author: Jorge Martinez-Gil
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from rdflib import Graph, Namespace
import sys

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


def preprocess_text(text):
    """
    Preprocesses a text by tokenizing it into sentences and words, converting to lowercase, and removing stopwords.

    Args:
        text (str): The text to preprocess.

    Returns:
        set: A set of preprocessed words.
    """
    # Tokenize the sentences and convert to lowercase
    sentences = sent_tokenize(text.lower())

    # Tokenize words in each sentence and remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [word for word in words if word not in stop_words]
        tokens.extend(words)
    
    return set(tokens)


def jaccard_similarity(set1, set2):
    """
    Calculates the Jaccard similarity between two sets.

    Args:
        set1 (set): The first set.
        set2 (set): The second set.

    Returns:
        float: The Jaccard similarity between the two sets.
    """
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


def are_graphs_identical(g1, g2):
    """
    Checks if two RDF graphs are identical.

    Args:
        g1 (rdflib.Graph): The first RDF graph.
        g2 (rdflib.Graph): The second RDF graph.

    Returns:
        bool: True if the graphs are identical, False otherwise.
    """
    return len(g1) == len(g2) and all(t in g2 for t in g1) and all(t in g1 for t in g2)


def check_similarity(catalog1_file, catalog2_file):
    """
    Calculates the similarity between two DCAT catalogs in Turtle format.

    Args:
        catalog1_file (str): The path to the first catalog file.
        catalog2_file (str): The path to the second catalog file.

    Returns:
        float: The similarity between the two catalogs as a percentage.
    """
    # Parse Turtle files into RDF graph
    g1 = Graph()
    g1.parse(catalog1_file, format='ttl')
    
    g2 = Graph()
    g2.parse(catalog2_file, format='ttl')
    
    # Check if the graphs are identical
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
    titles1 = [preprocess_text(title) for title in titles1]
    titles2 = [preprocess_text(title) for title in titles2]
    descriptions1 = [preprocess_text(desc) for desc in descriptions1]
    descriptions2 = [preprocess_text(desc) for desc in descriptions2]
    
    # Calculate Jaccard similarity for titles and descriptions
    if titles1 and titles2:
        title_similarity = sum(jaccard_similarity(title1, title2) for title1 in titles1 for title2 in titles2) / (len(titles1) * len(titles2))
    else:
        title_similarity = 0.0

    if descriptions1 and descriptions2:
        description_similarity = sum(jaccard_similarity(desc1, desc2) for desc1 in descriptions1 for desc2 in descriptions2) / (len(descriptions1) * len(descriptions2))
    else:
        description_similarity = 0.0
    
    # Overall similarity as the average of title and description similarity
    overall_similarity = (title_similarity + description_similarity) / 2
    
    return overall_similarity * 100
    
"""
Main function that calculates the similarity between two DCAT catalogs in Turtle format and prints the result.

Usage: python check_similarity.py filepath filepath2
"""
def main():

    # Get paths to RDF data files from command line arguments
    if len(sys.argv) < 3:
        print("Usage: python check_similarity.py filepath filepath2")
        sys.exit(1)

    rdf_data_path = sys.argv[1]
    rdf_data_path2 = sys.argv[2]

    # Calculate similarity
    result = check_similarity(rdf_data_path, rdf_data_path2)
    print(f"The similarity of {rdf_data_path} and {rdf_data_path2} is {result}%.")
   

if __name__ == "__main__":
    main()