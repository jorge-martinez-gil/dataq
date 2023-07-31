# Framework to Automatically Determine the Quality of Open Data Catalogs
This repository contains code for reproducing the paper
- Jorge Martinez-Gil, "Framework to Automatically Determine the Quality of Open Data Catalogs", [[arXiv preprint]](https://arxiv.org/abs/2307.15464), July 2023

## Introduction

Data catalogs play a crucial role in modern data-driven organizations by facilitating the discovery, understanding, and utilization of diverse data assets. However, ensuring their quality and reliability is complex, especially in open and large-scale data environments. This framework proposes to automatically determine the quality of open data catalogs, addressing the need for efficient and reliable quality assessment mechanisms. The goal is to empower data-driven organizations to make informed decisions based on trustworthy and well-curated data assets.

## Core Quality Dimensions

Our framework can analyze various core quality dimensions, including:

1. Accuracy: Assessing the correctness and precision of data in the catalog.
2. Completeness: Measuring the extent to which all required data is available.
3. Consistency: Checking for coherence and agreement between different data sources in the catalog.
4. Scalability: Evaluating the capability of the catalog to handle growing data volumes.
5. Timeliness: Determining how up-to-date the data in the catalog is.

## Non-Core Quality Dimensions

In addition to core quality dimensions, the framework implements a set of non-core quality dimensions, such as:

1. Provenance: Assessing the origin and history of data to establish its reliability.
2. Readability: Evaluating the clarity and understandability of the catalog's data descriptions.
3. Licensing: Verifying the usage rights and restrictions associated with the data.

## Compatibility and Similarity Assessment

Our framework offers several alternatives for the assessment of compatibility and similarity across different data catalogs. This allows organizations to identify and leverage complementary data assets effectively.

## Install
``` pip install -r requirements.txt```

## Usage

``` python check_accuracy.py example001.ttl```
Check the accuracy of a DCAT data catalog.

``` python check_compatibility.py example001.ttl example002.ttl```
Check the compatibility of two DCAT data catalogs.

``` python check_completeness.py example001.ttl```
Check the completeness of a DCAT data catalog.

``` python check_consistency.py example001.ttl entity_type```
Check the consistency of a DCAT data catalog for the kind of entity (catalog, dataset, distribution).

``` python check_licensing.py example001.ttl```
Check the licensing of a DCAT data catalog.

``` python check_lineage_provenance.py example001.ttl```
Check the lineage and provenance of a DCAT data catalog.

``` python check_readability.py example001.ttl```
Check the readability of a DCAT data catalog according the Flesch-Kincaid Grade Level.

``` python check_scalability.py example001.ttl```
Check the scalability of a DCAT data catalog.

``` python check_similarity.py example001.ttl example002.ttl```
Check the similarity of two DCAT data catalogs.

``` python check_timeliness.pyexample001.ttl ```
Check the timeliness of a DCAT data catalog.

## Citation
If you use this work, please cite:

```
@inproceedings{martinez2023d,
  author    = {Jorge Martinez-Gil},
  title     = {Framework to Automatically Determine the Quality of Open Data Catalogs},
  journal   = {CoRR},
  volume    = {abs/2307.15464},
  year      = {2023},
  url       = {https://arxiv.org/abs/2307.15464},
  doi       = {https://doi.org/10.48550/arXiv.2307.15464},
  eprinttype = {arXiv},
  eprint    = {2307.15464}
}

```

# License
This code is released under the MIT License. See the LICENSE file for more information.