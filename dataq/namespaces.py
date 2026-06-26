# -*- coding: utf-8 -*-
"""Central RDF namespace definitions shared across all DataQ metrics.

Defining these once removes the per-script duplication that the original
standalone scripts carried, and guarantees every quality dimension reasons
about the same vocabularies (DCAT, Dublin Core Terms, PROV-O, FOAF, RDF(S)).
"""
from rdflib import Namespace

DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCT = Namespace("http://purl.org/dc/terms/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
RDF_NS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS_NS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
PROV = Namespace("http://www.w3.org/ns/prov#")

# Backwards-compatible lowercase aliases (mirrors the names used in the
# original check_*.py scripts so ported code reads identically).
dcat = DCAT
dct = DCT
dcterms = DCT
foaf = FOAF
prov = PROV
