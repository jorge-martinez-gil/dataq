# DataQ: Automated Quality Assessment of Open Data Catalogs

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.eswa.2025.128379-red.svg)](https://doi.org/10.1016/j.eswa.2025.128379)
[![arXiv preprint](https://img.shields.io/badge/arXiv-2307.15464-brightgreen.svg)](https://arxiv.org/abs/2307.15464)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-213%20passing-brightgreen.svg)](#tests--reproducibility)
[![Survey](https://img.shields.io/badge/living%20survey-SURVEY.md-blueviolet.svg)](SURVEY.md)

> **DataQ** measures the quality of an open data catalog encoded in RDF/Turtle (DCAT)
> across **eight FAIR-aligned quality dimensions** and produces a structured,
> machine-readable quality report in **one command**.
>
> This repository holds two things that reinforce each other: the open-source
> **reference implementation** of the method, and a **living survey** of the whole
> research area, [`SURVEY.md`](SURVEY.md), that maps the tools and papers on open data,
> linked data, and FAIR quality assessment and shows where DataQ fits.
>
> Reference paper: Martinez-Gil, J. (2025). *Framework to automatically determine the
> quality of open data catalogs.* **Expert Systems with Applications**, 289, 128379.
> [[journal]](https://doi.org/10.1016/j.eswa.2025.128379) ·
> [[preprint]](https://arxiv.org/abs/2307.15464) · [[how to cite]](#how-to-cite)

```bash
pip install -e .             # from this repository
dataq assess my_catalog.ttl  # full quality report in your terminal
```

---

## Two resources in one repository

**1. The tool.** Point DataQ at a DCAT/RDF catalog and it returns per-dimension scores plus a machine-readable report you can track over time, compare across portals, and cite in a paper.

**2. The living survey.** [`SURVEY.md`](SURVEY.md) is a maintained systematic review of automated quality assessment for open data catalogs, linked data, and FAIR resources. It gathers more than forty verified references into one taxonomy, compares every major tool in an honest feature table, and lists the open problems worth solving. If you are entering this area, start there. Corrections and additions are welcome ([CONTRIBUTING.md](CONTRIBUTING.md)).

---

## What problem does this solve?

Open data catalogs (data.gov, the EU Open Data Portal, regional and institutional portals) are public infrastructure, yet their metadata quality is rarely assessed in a systematic, automated, comparable way. Poor catalog quality, meaning missing fields, broken links, no license, stale or unreadable metadata, absent provenance, silently undermines discoverability, reuse, and trust.

DataQ turns "is this catalog any good?" into a reproducible number. Every metric is a short, readable module, so a reviewer can see exactly what a score means, and assessment is offline-deterministic, so the same catalog yields the same result on any machine.

## Why catalog quality matters

Data quality is a precondition for the **FAIR principles** (Findable, Accessible, Interoperable, Reusable). A dataset nobody can find, that has no license, or whose provenance is unknown, is not reusable however good the underlying data is. Catalog-level quality is where findability and reuse are won or lost.

---

## Quality dimensions

Each dimension traces to the data-quality literature. The mapping to source references is in [`SURVEY.md`](SURVEY.md), Section 3.

| Dimension | What it measures | Output |
|---|---|---|
| **Completeness** | Presence of core DCAT / DCT properties on Catalog, Dataset, Distribution | % |
| **Accuracy** | 100 − mean(missing core props, duplicates, broken links) | % |
| **Consistency** | Share of (subject, predicate) pairs with a single, non-conflicting value | % |
| **Licensing** | Datasets that declare a `dcterms:license` | % |
| **Provenance** | Lineage + PROV-O coverage (six criteria) | % |
| **Readability** | Flesch-Kincaid grade level of titles & descriptions | grade |
| **Timeliness** | Catalog modified within the last 365 days | yes/no |
| **Scalability** | Timing heuristic for catalog-scale operations | category |
| **Compatibility** *(pairwise)* | Triples of catalog A also present in catalog B | % |
| **Similarity** *(pairwise)* | Jaccard overlap of titles & descriptions | % |

---

## How DataQ compares to other tools

The field has three communities that mostly work apart: open-data portal quality, linked-data and knowledge-graph quality, and FAIR assessment. Most tools score a single dataset; few score a whole catalog. The short table below places DataQ among representative tools. The full twelve-tool comparison, with references, is in [`SURVEY.md`](SURVEY.md), Section 5.

| Tool | Unit assessed | Target model | Automation | Open source |
|---|---|---|---|---|
| **DataQ** | Whole catalog (DCAT graph) | DCAT, DCT, PROV-O | one command, offline-deterministic | MIT |
| data.europa.eu MQA | Whole catalog (DCAT-AP) | DCAT-AP + SHACL | web service | partly open |
| F-UJI | Single dataset | DataCite, schema.org | web / API | open |
| Luzzu | Dataset / RDF graph | linked data | metric language | open |
| RDFUnit | Dataset / RDF graph | RDF, RDFS, OWL | SPARQL tests | open |

DataQ occupies the open, reproducible, research-friendly niche: a place to prototype a new dimension, run a fair cross-portal comparison, or teach how catalog quality is measured. It complements the European MQA service and the dataset-level FAIR tools rather than replacing them.

---

## Benchmark over the bundled catalogs

Real numbers, recomputed live from the bundled data with `python examples/run_benchmark.py`. Nothing is hard-coded, so the table reproduces on any machine.

| catalog | triples | aggregate% | Completeness(DCAT)% | Completeness(DCT)% | Consistency% | Licensing% | Provenance% | Readability(FK) | Timely |
|---|---|---|---|---|---|---|---|---|---|
| example001.ttl | 27 | 50.42 | 40.0 | 13.33 | 95.0 | 50.0 | 16.7 | 0.25 | False |
| example002.ttl | 37 | 25.8 | 6.67 | 66.67 | 96.55 | 0.0 | 0.0 | 5.25 | False |
| example003.ttl | 26 | 50.42 | 40.0 | 13.33 | 95.0 | 50.0 | 16.7 | 1.65 | False |
| example004.ttl | 56 | 29.17 | 23.81 | 14.29 | 92.86 | 0.0 | 0.0 | 8.8 | False |
| canada.ttl | 15 | 48.08 | 0.0 | 50.0 | 92.31 | 100.0 | 0.0 | 14.2 | False |
| canada2.ttl | 45 | 19.0 | 0.0 | 55.56 | 76.0 | 0.0 | 0.0 | 10.7 | False |
| easa.ttl | 356 | 21.91 | 8.33 | 75.0 | 79.31 | 0.0 | 0.0 | 7.9 | False |
| euromap.ttl | 786 | 18.21 | 0.0 | 81.48 | 72.84 | 0.0 | 0.0 | 15.12 | False |
| europeana.ttl | 223 | 19.74 | 0.0 | 77.78 | 78.95 | 0.0 | 0.0 | 10.6 | False |
| hadea.ttl | 97 | 27.04 | 11.11 | 77.78 | 97.06 | 0.0 | 0.0 | 17.7 | False |
| pacific.ttl | 16 | 48.08 | 0.0 | 50.0 | 92.31 | 100.0 | 0.0 | 14.2 | False |
| pacific2.ttl | 59 | 48.28 | 0.0 | 66.67 | 93.1 | 100.0 | 0.0 | 22.1 | False |

---

## Installation

```bash
pip install -e .                  # core
pip install -e ".[similarity]"    # + NLTK tokenizer for the similarity dimension
```

**Dependencies:** `rdflib`, `requests`, `textstat`, `pytz` (lightweight, no GPU).
`textstat` is pinned to `0.7.3` to compute Flesch-Kincaid grades offline; on
`setuptools >= 81` also run `pip install "setuptools<81"` (it provides `pkg_resources`).

---

## How do I evaluate my own catalog?

**One command:**

```bash
dataq assess my_catalog.ttl                          # human-readable report
dataq assess my_catalog.ttl -f json -o report.json   # machine-readable
dataq assess https://example.org/catalog.ttl --check-links   # include live link checks
```

**From Python:**

```python
from dataq import assess_catalog

report = assess_catalog("my_catalog.ttl")
print(report.to_text())          # pretty report
print(report.aggregate_score)    # convenience aggregate (see note below)
data = report.to_dict()          # full machine-readable result
for m in report.metrics:
    print(m.key, m.display_value())
```

**Use one dimension at a time:**

```python
from dataq.io import load_graph
from dataq.metrics import completeness, provenance

g = load_graph("my_catalog.ttl")
print(completeness.completeness(g, "dcat"))   # -> 40.0
print(provenance.provenance(g))               # -> 16.7
```

**Cross-catalog tools:**

```bash
dataq similarity     a.ttl b.ttl
dataq compatibility  a.ttl b.ttl
dataq show           a.ttl
```

> **Note on the aggregate score.** `aggregate_score` is a transparent, unweighted mean of
> the percentage-based dimensions (completeness, consistency, licensing, provenance, and
> accuracy when computed). It is a convenience indicator for ranking catalogs. It is
> **not** a weighted index defined in the source paper. Every dimension is always reported
> separately so you can apply your own weighting. How to weight and aggregate dimensions
> fairly is itself an open problem; see [`SURVEY.md`](SURVEY.md), Section 6, and the AHP
> approach of Kubler et al. (2018).

---

## The JSON report

```jsonc
{
  "source": "my_catalog.ttl",
  "dataq_version": "1.0.0",
  "n_triples": 97,
  "entities": { "Catalog": 1, "Dataset": 1, "Distribution": 1 },
  "aggregate_score": 27.04,
  "aggregated_dimensions": ["completeness_dcat", "consistency", "licensing", "provenance"],
  "metrics": [
    { "key": "completeness_dcat", "name": "Completeness (DCAT)", "value": 11.11,
      "unit": "percent", "higher_is_better": true, "skipped": false, "note": "" }
  ]
}
```

Stable `key`s make it easy to track a catalog over time or compare many portals. The
schema maps cleanly onto the W3C Data Quality Vocabulary (DQV), the standard interchange
format for quality scores; see [`SURVEY.md`](SURVEY.md), Section 4.5.

---

## How do I reproduce the experiments?

The repository ships example catalogs (`example001.ttl`–`example004.ttl`) and real
**"Official catalogs"** (Canada, Europeana, EASA, EuroMap, HADEA, Pacific Data). Reproduce
the full comparison table with one command:

```bash
python examples/run_benchmark.py    # writes benchmark/results.csv and results.md
```

Every value is computed live from the bundled data, so the table is fully reproducible on
any machine.

## Tests & reproducibility

```bash
pip install -e ".[dev]"
pytest -q          # 213 tests
```

The suite includes **parity tests** asserting the packaged metrics return values
**numerically identical** to the original standalone `check_*.py` scripts across every
bundled catalog. This is the scientific-integrity guardrail that the refactor is a
faithful reimplementation, not a re-derivation.

---

## How do I extend DataQ?

A new quality dimension is a small, self-contained module:

```python
# dataq/metrics/my_dimension.py
from rdflib import Graph
from dataq.report import MetricResult

def my_dimension(graph: Graph) -> float:
    ...                      # compute a score from the RDF graph
    return score

def evaluate(graph: Graph) -> MetricResult:
    return MetricResult(key="my_dimension", name="My dimension",
                        value=my_dimension(graph), unit="percent",
                        higher_is_better=True)
```

Add its `evaluate(graph)` call to `dataq/assess.py` and it appears in every report, JSON
export, and benchmark automatically. New dimensions that fill a gap named in
[`SURVEY.md`](SURVEY.md), Section 7, are especially welcome as contributions.

---

## Repository layout

```
dataq/                 importable package
  io.py                unified RDF loading (file / URL)
  namespaces.py        shared DCAT / DCT / PROV namespaces
  report.py            MetricResult + QualityReport (JSON / Markdown / text)
  assess.py            one-call orchestrator -> QualityReport
  cli.py               `dataq` command-line interface
  metrics/             one module per quality dimension
examples/run_benchmark.py   reproducible benchmark over bundled catalogs
tests/                 pytest suite incl. parity tests
check_*.py             original standalone scripts (preserved, still runnable)
Official catalogs/     real-world DCAT catalogs for benchmarking
SURVEY.md              living survey of the research area
references.bib         curated, verified bibliography (40+ entries)
CONTRIBUTING.md        how to extend the tool and the survey
```

The original `check_*.py` scripts are kept for backward compatibility and as cited
artifacts; they still run exactly as before (`python check_completeness.py file.ttl`).

---

## The living survey

[`SURVEY.md`](SURVEY.md) is the part of this repository meant for the wider community to
read, cite, and extend. It contains:

- a lightweight systematic-review method (search strategy, inclusion criteria, verification);
- a unified taxonomy that reconciles quality dimensions across three research communities;
- a twelve-tool comparison table covering DataQ, the European MQA, F-UJI, FAIRshake, the
  FAIR Evaluator, FAIR-Checker, Luzzu, RDFUnit, SHACL, ShEx, Roomba, and Open Data Portal Watch;
- open problems and a research agenda, including the missing shared benchmark;
- a curated [`references.bib`](references.bib) where every entry resolves to a DOI or an
  official standards URL.

If it helps your work, please cite the reference paper below, and open a pull request to
keep it current.

---

## Keywords

`open data quality` · `data catalog quality` · `metadata quality` · `FAIR assessment` ·
`FAIR evaluation tool` · `DCAT validation` · `linked data quality` · `knowledge graph quality` ·
`metadata benchmarking` · `open government data quality` · `RDF` · `data governance` ·
`provenance` · `semantic web` · `survey`

---

## How to cite

If you use DataQ or the survey in your research, please cite the paper. The
[`CITATION.cff`](CITATION.cff) file also exports this through GitHub's "Cite this
repository" button.

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

> Martinez-Gil, J. (2025). Framework to automatically determine the quality of open data
> catalogs. *Expert Systems with Applications*, *289*, 128379.
> https://doi.org/10.1016/j.eswa.2025.128379

---

## License

[MIT](LICENSE) © Jorge Martinez-Gil.
