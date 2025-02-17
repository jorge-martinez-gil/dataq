# Framework to Automatically Determine the Quality of Open Data Catalogs

> **Repository Overview**: This repository offers an innovative solution for assessing the quality of open data catalogs, based on the paper by Jorge Martinez-Gil.

[![arXiv preprint](https://img.shields.io/badge/arXiv-2307.15464-brightgreen.svg)](https://arxiv.org/abs/2307.15464) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Citations](https://img.shields.io/badge/citations-3-blue)](https://scholar.google.com/citations?view_op=view_citation&hl=en&citation_for_view=X1pRUYcAAAAJ:XUAslYVNQLQC)

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

```bash
python check_accuracy.py example001.ttl    # Check data accuracy
python check_completeness.py example001.ttl    # Assess completeness
python check_consistency.py example001.ttl entity_type    # Ensure consistency
python check_scalability.py example001.ttl    # Evaluate scalability
python check_timeliness.py example001.ttl    # Verify timeliness
python check_compatibility.py example001.ttl example002.ttl    # Compare compatibility
python check_similarity.py example001.ttl example002.ttl    # Analyze similarity
python check_licensing.py example001.ttl    # Check licensing compliance
python check_lineage_provenance.py example001.ttl    # Assess data provenance
python check_readability.py example001.ttl    # Measure readability (Flesch-Kincaid Grade Level)
```


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
## 📑 Research that has cited this work

1. **[Assessing the Readability of Open Data Portals: A Case Study of Open Data Pakistan](http://jice.um.edu.my/index.php/MJLIS/article/view/48035)**
   - **Authors:** N.F. Warraich, T. Rasool
   - **Journal:** *Journal of Library and Information Science*, 2023
   - **Abstract:** Open data portals provide accessible and reproducible data. This study evaluates the readability of datasets from Open Data Pakistan.

2. **[Automated Quality Indicators for Machine-Actionable Data Management Plans](https://repositum.tuwien.at/handle/20.500.12708/200466)**
   - **Author:** L. Arnhold
   - **Journal:** *Repositum*, TU Wien, 2024
   - **Abstract:** Discusses the role of machine-actionable Data Management Plans (DMPs) in research, focusing on automated quality indicators for improving data management.

3. **[An Overview of Approaches to Quantify Open Data Catalog Similarity](http://publicationslist.org/data/jorge-martinez-gil/ref-204/Data-Catalogs.pdf)**
   - **Author:** J. Martinez-Gil
   - **Journal:** *Preprint*, 2023
   - **Abstract:** As open data initiatives grow, this paper explores various methods to measure the similarity between different open data catalogs.

## 📄 License
This project is available under the MIT License.
