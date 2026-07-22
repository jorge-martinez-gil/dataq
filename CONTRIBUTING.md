# Contributing to DataQ and the living survey

Thank you for helping keep this project accurate and current. There are two kinds of contribution, and both are valued equally.

1. **The tool.** Code for the DataQ package: new quality dimensions, bug fixes, parsers, output formats, tests.
2. **The survey.** Entries for [`SURVEY.md`](SURVEY.md) and [`references.bib`](references.bib): a missing paper, a new tool, a corrected citation, an updated comparison row.

A survey stays useful only when the community keeps it honest. A single correction is a real contribution, and contributors are credited in the repository history.

---

## Adding or correcting a reference

Accuracy is the one hard rule. Every entry in [`references.bib`](references.bib) must resolve to a **DOI** or an **official standards-body URL**. Preprints are allowed only when no published version exists, and they must be labeled as preprints.

Steps:

1. Add the entry to [`references.bib`](references.bib) in the correct thematic section, following the existing key style (`lastnameYYYYkeyword`).
2. Confirm the author list, year, exact title, and venue at the source of record (the publisher page, the DOI, or the W3C/ISO catalog). Quote the title verbatim.
3. Add a one-line mention in the matching part of [`SURVEY.md`](SURVEY.md), and a row to the relevant table where it applies.
4. Open a pull request that states where you verified the metadata.

If a well-known work carries an online-first year that differs from its issue year, use the issue year and note the difference in a BibTeX comment, following the pattern already used for Zaveri et al. and Färber et al.

---

## Adding a tool to the comparison

The tool comparison lives in two places that must stay in sync: the table in [`SURVEY.md`](SURVEY.md), Section 5, and the machine-readable [`survey/tools.csv`](survey/tools.csv).

For each tool, record: the primary peer-reviewed reference, the unit it assesses (single dataset, whole catalog, or graph), the target model or standard, the dimensions it covers, its automation level, its output format, and whether the source is open. Keep the description fair and grounded in what the tool actually does; a comparison table earns trust when it resists promoting any single tool.

---

## Adding a quality dimension to the tool

A dimension is a small, self-contained module:

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

Then:

1. Add the `evaluate(graph)` call to `dataq/assess.py`.
2. Add a test in `tests/` that pins the expected value on at least one bundled catalog.
3. Run `pytest -q` and confirm all tests pass.
4. If your dimension answers a gap named in [`SURVEY.md`](SURVEY.md), Section 7, say so in the pull request. Those contributions are the most useful of all.

---

## Pull request checklist

- Tests pass locally (`pytest -q`).
- New references resolve to a DOI or official URL, verified at the source.
- Survey text and tables are updated together with `references.bib`.
- The change is described in one clear paragraph, with a note on where you checked any new metadata.

---

## Questions

Open an issue for anything unclear, or reach the maintainer through the [ORCID profile](https://orcid.org/0000-0002-8179-6810). Small, focused pull requests are easier to review and merge than large ones.
