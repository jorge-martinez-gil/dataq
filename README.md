# DataQ — Automated Quality Assessment of Open Data Catalogs

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.eswa.2025.128379-red.svg)](https://doi.org/10.1016/j.eswa.2025.128379)
[![arXiv preprint](https://img.shields.io/badge/arXiv-2307.15464-brightgreen.svg)](https://arxiv.org/abs/2307.15464)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-213%20passing-brightgreen.svg)](#tests--reproducibility)

> **DataQ** automatically measures the quality of an open data catalog encoded in
> RDF/Turtle (DCAT) across **eight FAIR-aligned quality dimensions** and produces a
> structured, machine-readable quality report — in **one command**.
>
> Reference implementation for: Martinez-Gil, J. (2025). *Framework to automatically
> determine the quality of open data catalogs.* **Expert Systems with Applications**,
> 289, 128379. [[journal]](https://doi.org/10.1016/j.eswa.2025.128379) ·
> [[preprint]](https://arxiv.org/abs/2307.15464) · [[how to cite]](#-how-to-cite)

```bash
pip install -e .             # from this repository
dataq assess my_catalog.ttl  # full quality report in your terminal
```

---

## What problem does this solve?

Open data catalogs (data.gov, the EU Open Data Portal, regional and institutional
portals) are critical public infrastructure, yet **their metadata quality is rarely
assessed in a systematic, automated, comparable way.** Poor catalog quality — missing
fields, broken links, no license, stale or unreadable metadata, absent provenance —
silently undermines discoverability, reuse, and trust.

**DataQ turns "is this catalog any good?" into a reproducible number.** Point it at a
DCAT/RDF catalog and it returns per-dimension scores plus a machine-readable report you
can track over time, compare across portals, and cite in a paper.

## Why does catalog quality matter?

Data quality is a precondition for the **FAIR principles** (Findable, Accessible,
Interoperable, Reusable). A dataset nobody can find, that has no license, or whose
provenance is unknown, is not reusable regardless of how good the underlying data is.
Catalog-level quality is where findability and reusability are won or lost.

## Why is DataQ different?

- **Catalog-level, not dataset-level** — it evaluates the whole DCAT graph
  (Catalog → Dataset → Distribution), not a single file.
- **Eight dimensions in one pass** — accuracy, completeness, consistency, scalability,
  timeliness, provenance, readability, licensing — plus cross-catalog compatibility and
  similarity.
- **Machine-readable & reproducible** — JSON / Markdown / text reports, a stable Python
  API, and a test suite that proves every number matches the published reference.
- **Standards-native** — works directly on W3C **DCAT**, **Dublin Core Terms (DCT)**,
  and **PROV-O** vocabularies in RDF/Turtle.
- **Peer-reviewed method** — backed by a paper in *Expert Systems with Applications*.

---

## Quality dimensions

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

## Installation

```bash
pip install -e .                  # core
pip install -e ".[similarity]"    # + NLTK tokenizer for the similarity dimension
```

**Dependencies:** `rdflib`, `requests`, `textstat`, `pytz` (lightweight, no GPU).
`textstat` is pinned to `0.7.3` to compute Flesch-Kincaid grades **offline**; on
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
> accuracy when computed). It is a convenience indicator for ranking catalogs — it is
> **not** a weighted index defined in the source paper. Every dimension is always reported
> separately so you can apply your own weighting.

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

Stable `key`s make it easy to track a catalog over time or compare many portals.

---

## How do I reproduce the experiments?

The repository ships example catalogs (`example001.ttl`–`example004.ttl`) and real
**"Official catalogs"** (Canada, Europeana, EASA, EuroMap, HADEA, Pacific Data …).
Reproduce the full comparison table with one command:

```bash
python examples/run_benchmark.py    # writes benchmark/results.csv and results.md
```

Every value is computed live from the bundled data — nothing is hard-coded — so the
table is fully reproducible on any machine.

## Tests & reproducibility

```bash
pip install -e ".[dev]"
pytest -q          # 213 tests
```

The suite includes **parity tests** asserting the packaged metrics return values
**numerically identical** to the original standalone `check_*.py` scripts across every
bundled catalog — the scientific-integrity guardrail that the refactor is a faithful
reimplementation, not a re-derivation.

---

## How do I extend the framework?

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
export, and benchmark automatically.

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
```

The original `check_*.py` scripts are kept for backward compatibility and as cited
artifacts; they still run exactly as before (`python check_completeness.py file.ttl`).

---

## Keywords

`open data quality` · `data catalog quality` · `metadata quality` · `FAIR assessment` ·
`FAIR evaluation tool` · `DCAT validation` · `linked data quality` · `repository quality` ·
`metadata benchmarking` · `open government data quality` · `RDF` · `knowledge graph` ·
`data governance` · `provenance` · `semantic web`

---

## 📚 How to cite

If you use DataQ in your research, please cite the paper. GitHub's **"Cite this
repository"** button (powered by [`CITATION.cff`](CITATION.cff)) also exports this.

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
