import sys
from rdflib import Graph, RDF, Namespace

# Define some RDF prefixes
dcat = Namespace("http://www.w3.org/ns/dcat#")
dct = Namespace("http://purl.org/dc/terms/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# DCAT properties
dcat_properties = [
    dcat.title,
    dcat.downloadURL,
    dcat.size
]

# DCT properties
dct_properties = [
    dct.title,
    dct.identifier,
    dct.description
]

def calculate_completeness(graph, subject, required_properties):
    """
    Calculates the completeness of a catalog.
    """
    present_properties = set()
    for predicate, obj in graph.predicate_objects(subject):
        if predicate in required_properties:
            present_properties.add(predicate)
    return len(present_properties) / len(required_properties) * 100

def check_completeness(rdf_data: str, property_set: str) -> float:
    """
    Checks the completeness of RDF data.
    """
    required_properties = dct_properties if property_set == 'dct' else dcat_properties
    graph = Graph()
    graph.parse(data=rdf_data, format="turtle")
    completeness_scores = []
    for subject_type in [dcat.Catalog, dcat.Dataset, dcat.Distribution]:
        for subject in graph.subjects(RDF.type, subject_type):
            score = calculate_completeness(graph, subject, required_properties)
            completeness_scores.append(score)
    return sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0

def main():
    try:
        if len(sys.argv) < 3:
            print("Usage: python check_completeness.py filepath [dcat|dct]")
            sys.exit(1)

        rdf_data_path = sys.argv[1]
        property_set = sys.argv[2]

        if property_set not in ['dcat', 'dct']:
            print("Invalid property set. Choose 'dcat' or 'dct'.")
            sys.exit(1)

        with open(rdf_data_path, "r", encoding="utf-8") as f:
            rdf_data = f.read()

        result = check_completeness(rdf_data, property_set)
        print(f"The completeness of {rdf_data_path} using {property_set.upper()} properties is {result}%.")

    except FileNotFoundError:
        print(f"File not found: {rdf_data_path}")
        sys.exit(1)

    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
