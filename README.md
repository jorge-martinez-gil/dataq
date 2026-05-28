# Framework to Automatically Determine the Quality of Open Data Catalogs

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.eswa.2025.128379-red.svg)](https://doi.org/10.1016/j.eswa.2025.128379)
[![arXiv preprint](https://img.shields.io/badge/arXiv-2307.15464-brightgreen.svg)](https://arxiv.org/abs/2307.15464)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Citations](https://img.shields.io/badge/citations-4-blue)](https://scholar.google.com/citations?view_op=view_citation&hl=en&citation_for_view=X1pRUYcAAAAJ:pcWPcJyQGiUC)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

> **Published in**: *Expert Systems with Applications*, vol. 289, p. 128379, 2025.  
> Martinez-Gil, J. (2025). Framework to automatically determine the quality of open data catalogs. *Expert Syst. Appl.* **289**: 128379.  
> 🔗 [Journal paper](https://doi.org/10.1016/j.eswa.2025.128379) · [arXiv preprint](https://arxiv.org/abs/2307.15464) · [Cite this repository](#-citation)

---

## 🌟 Abstract

Open data catalogs are critical infrastructure for data-driven decision making, yet their quality is rarely assessed in a systematic or automated way. This repository provides a **Python framework** that automatically evaluates the quality of open data catalogs encoded in RDF/Turtle (`.ttl`) format. The framework covers **eight quality dimensions**—accuracy, completeness, consistency, scalability, timeliness, provenance, readability, and licensing—as well as **cross-catalog compatibility and similarity** assessment.

This work addresses a real need for researchers and practitioners working on **open data**, **FAIR data principles**, **linked data**, **knowledge graphs**, and **data governance**.

---

## 🎯 Key Contributions

- ✅ **Automated, reproducible quality assessment** of open data catalogs without manual intervention
- ✅ **Eight quality dimensions** covering both intrinsic (accuracy, completeness) and contextual (provenance, readability) aspects
- ✅ **Cross-catalog analysis** for compatibility and semantic similarity
- ✅ **RDF/Turtle support** — natively works with W3C-standard linked data formats
- ✅ **Lightweight Python implementation** with minimal dependencies, easy to integrate into existing pipelines
- ✅ **Extensible architecture** — new quality dimensions can be added as independent modules

---

## 📊 Quality Dimensions

### Core Dimensions

| Dimension | Description |
|---|---|
| **Accuracy** | Verifies data correctness and precision |
| **Completeness** | Measures the availability and coverage of expected data fields |
| **Consistency** | Detects incoherence and contradictions across data sources |
| **Scalability** | Assesses catalog performance as data volume grows |
| **Timeliness** | Checks currency and freshness of data |

### Contextual Dimensions

| Dimension | Description |
|---|---|
| **Provenance** | Traces the origin, lineage, and history of data assets |
| **Readability** | Evaluates clarity of descriptions (Flesch-Kincaid Grade Level) |
| **Licensing** | Confirms usage rights and license compliance |

### Cross-Catalog Analysis

| Capability | Description |
|---|---|
| **Compatibility** | Identifies structurally or semantically compatible catalogs |
| **Similarity** | Quantifies semantic overlap between two catalogs |

---

## 🛠️ Installation

```bash
pip install -r requirements.txt
```

**Dependencies:** `nltk`, `rdflib`, `requests`, `textstat` — all lightweight, no GPU required.

---

## ⚙️ Usage

Each quality dimension has its own dedicated script:

```bash
# Core quality checks
python check_accuracy.py example001.ttl
python check_completeness.py example001.ttl
python check_consistency.py example001.ttl entity_type
python check_scalability.py example001.ttl
python check_timeliness.py example001.ttl

# Contextual quality checks
python check_licensing.py example001.ttl
python check_lineage_provenance.py example001.ttl
python check_readability.py example001.ttl        # Flesch-Kincaid Grade Level

# Cross-catalog analysis (requires two catalogs)
python check_compatibility.py example001.ttl example002.ttl
python check_similarity.py example001.ttl example002.ttl
```

Example RDF/Turtle catalogs (`example001.ttl` – `example004.ttl`) are included in the repository.

---

## 📚 Citation

If you use this framework in your research, please cite the following paper.  
GitHub also provides a **"Cite this repository"** button (top-right of the repo page) powered by the included [`CITATION.cff`](CITATION.cff) file.

### BibTeX

```bibtex
@article{martinez2025datacatalogs,
  title   = {Framework to Automatically Determine the Quality of Open Data Catalogs},
  author  = {Jorge Martinez-Gil},
  journal = {Expert Systems with Applications},
  volume  = {289},
  pages   = {128379},
  year    = {2025},
  issn    = {0957-4174},
  doi     = {10.1016/j.eswa.2025.128379},
  url     = {https://www.sciencedirect.com/science/article/pii/S0957417425019980},
}
```

### APA

> Martinez-Gil, J. (2025). Framework to automatically determine the quality of open data catalogs. *Expert Systems with Applications*, *289*, 128379. https://doi.org/10.1016/j.eswa.2025.128379

### Chicago

> Martinez-Gil, Jorge. "Framework to Automatically Determine the Quality of Open Data Catalogs." *Expert Systems with Applications* 289 (2025): 128379. https://doi.org/10.1016/j.eswa.2025.128379

---

## 🔑 Keywords

`open data` · `data catalog` · `data quality` · `linked data` · `RDF` · `knowledge graph` · `FAIR data` · `data governance` · `data management` · `semantic web` · `automated assessment`

---

## 📑 Research That Has Cited This Work

1. **[Assessing the Readability of Open Data Portals: A Case Study of Open Data Pakistan](http://jice.um.edu.my/index.php/MJLIS/article/view/48035)**
   - **Authors:** N.F. Warraich, T. Rasool
   - **Venue:** *Malaysian Journal of Library & Information Science*, 2023
   - **Relevance:** Applies the readability dimension of this framework to evaluate Open Data Pakistan portals.

2. **[Automated Quality Indicators for Machine-Actionable Data Management Plans](https://repositum.tuwien.at/handle/20.500.12708/200466)**
   - **Author:** L. Arnhold
   - **Venue:** *TU Wien Repository*, 2024
   - **Relevance:** Extends the automated quality indicator approach to machine-actionable Data Management Plans (DMPs).

3. **[An Overview of Approaches to Quantify Open Data Catalog Similarity](http://publicationslist.org/data/jorge-martinez-gil/ref-204/Data-Catalogs.pdf)**
   - **Author:** J. Martinez-Gil
   - **Venue:** *Preprint*, 2023
   - **Relevance:** Surveys and extends the similarity assessment methodology introduced in this framework.

---

## 📄 License

This project is available under the [MIT License](LICENSE).
