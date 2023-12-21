# Framework to Automatically Determine the Quality of Open Data Catalogs

> **Repository Overview**: This repository offers an innovative solution for assessing the quality of open data catalogs, based on the paper by Jorge Martinez-Gil.

[![arXiv preprint](https://img.shields.io/badge/arXiv-2307.15464-brightgreen.svg)](https://arxiv.org/abs/2307.15464)

## 🌟 Introduction

In the era of data-driven decision making, data catalogs are indispensable. They streamline the discovery, understanding, and utilization of diverse data assets. This framework introduces an automated approach to evaluate the quality of open data catalogs. It's designed to bolster confidence in the data used by organizations, ensuring decisions are based on accurate, complete, and timely information.

## 📊 Core Quality Dimensions

The framework evaluates data catalogs across multiple dimensions:

- **Accuracy**: Ensures data correctness and precision.
- **Completeness**: Measures data availability comprehensively.
- **Consistency**: Maintains coherence across various data sources.
- **Scalability**: Assesses the catalog's ability to manage growing data volumes.
- **Timeliness**: Keeps data relevant and up-to-date.

## 📈 Non-Core Quality Dimensions

Beyond the core dimensions, we assess:

- **Provenance**: Traces the origin and history of data.
- **Readability**: Guarantees clear and understandable data descriptions.
- **Licensing**: Confirms data usage rights and restrictions.

## 🔄 Compatibility and Similarity Assessment

Identify and leverage complementary data assets through our advanced assessment tools for compatibility and similarity among various data catalogs.

## 🛠️ Installation
``` pip install -r requirements.txt```

## ⚙️ Usage

A suite of commands to evaluate different aspects of a data catalog:

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

``` python check_timeliness.py example001.ttl```
Check the timeliness of a DCAT data catalog.


## 📚 Citation

Please cite our work if you find it useful:

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

## 📄 License

This project is available under the MIT License - see the [LICENSE](https://chat.openai.com/c/LICENSE) file for details.