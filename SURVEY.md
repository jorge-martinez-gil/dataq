# A Living Survey of Automated Quality Assessment for Open Data Catalogs, Linked Data, and FAIR Resources

*Maintained alongside [DataQ](README.md), the open-source reference implementation.*
*Maintainer: Jorge Martinez-Gil ([ORCID 0000-0002-8179-6810](https://orcid.org/0000-0002-8179-6810)). Corrections and additions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).*

> **Short cite.** If this survey or its comparison tables help your work, please cite
> Martinez-Gil, J. (2025), *Framework to Automatically Determine the Quality of Open Data
> Catalogs*, Expert Systems with Applications, 289, 128379,
> [doi:10.1016/j.eswa.2025.128379](https://doi.org/10.1016/j.eswa.2025.128379). The full
> entry and a machine-readable [`references.bib`](references.bib) are at the end.

---

## Abstract

Open data catalogs, research-data repositories, and knowledge graphs are public infrastructure, yet the quality of their metadata is measured with a patchwork of methods that rarely agree and are seldom reproducible. This document maps that research area. It gathers more than forty peer-reviewed studies together with the principal standards (DCAT, the Data Quality Vocabulary, PROV-O, Dublin Core Terms, SHACL, and ISO/IEC 25012), organizes them into a single taxonomy of quality dimensions, and compares the tools that automate assessment across three communities that have mostly worked apart: open-government-data portal quality, linked-data and knowledge-graph quality, and FAIR data assessment. A recurring finding runs through the tools: most operate at the level of a single dataset, few evaluate a whole catalog as one object, and independent studies show that tools disagree on identical inputs. The survey closes with open problems and a research agenda, and positions DataQ as a small, tested, standards-native tool that others can extend.

**Keywords:** open data quality, metadata quality, data catalog quality, DCAT, FAIR assessment, linked data quality, knowledge graph quality, provenance, data governance, reproducible evaluation.

---

## 1. Why map this area

A dataset that no one can find, that carries no license, or whose origin is unknown, cannot be reused however good the underlying records are. Quality at the catalog level is where findability and reuse are won or lost, and it is exactly the level where measurement is weakest.

Three research communities have each built their own answer. Open-government-data researchers score portal metadata for completeness and retrievability. The semantic-web community assesses linked data and knowledge graphs for accuracy and consistency. The research-data community scores FAIRness against maturity indicators. These lines cite each other rarely, use different vocabularies for the same idea, and ship tools that are hard to compare. A researcher entering the area has no single map. This document is that map, and it is meant to stay current as a living resource rather than a one-time snapshot.

The practical payoff is threefold. A newcomer gets a taxonomy and a reading list with resolvable identifiers. A tool builder gets an honest feature comparison and a list of gaps worth solving. A portal operator gets a menu of what can be measured today and with which software.

---

## 2. Method

This review follows a lightweight systematic protocol so that its coverage can be checked and reproduced.

**Sources searched.** Google Scholar, DBLP, Crossref, and Semantic Scholar, together with the W3C and ISO catalogs for normative specifications.

**Query terms.** Combinations of *data quality*, *metadata quality*, *open data*, *data catalog*, *DCAT*, *linked data quality*, *knowledge graph quality*, *FAIR assessment*, *quality dimensions*, and *provenance*.

**Time span.** 1996 to 2026, from the foundational data-quality taxonomies to the most recent tool comparisons.

**Inclusion criteria.** A work was included when it (i) appeared in a peer-reviewed venue or is an official standard, and (ii) proposes, operationalizes, or evaluates an automated or semi-automated method for assessing the quality of data catalogs, metadata, linked data, or FAIRness.

**Exclusion criteria.** Opinion pieces without a method, and secondary web pages without a stable identifier, were left out. Two categories are kept but flagged: peer-reviewed workshop papers in CEUR-WS (no DOI, stable URL given), and one preprint retained only where no published version exists.

**Verification.** Every entry in the reference list was checked against a resolvable DOI or an official standards-body URL. Author lists, years, titles, and venues were confirmed at the source of record. Where a well-known work carries an online-first year that differs from its issue year (Zaveri et al.; Färber et al.), the issue year is used and the discrepancy is noted in [`references.bib`](references.bib).

**Result.** More than forty scholarly works and the core specifications listed in Section 5 form the corpus discussed below.

---

## 3. A unified taxonomy of catalog quality dimensions

Different communities name the same idea differently. The table below reconciles the dimensions DataQ computes with the sources that define them, so a reader can trace any single measure back to its origin.

| Dimension | Plain meaning | Grounded in |
|---|---|---|
| Completeness | Core descriptive properties are present on catalog, dataset, and distribution records | Wang & Strong 1996; Pipino et al. 2002; Neumaier et al. 2016; Vetrò et al. 2016 |
| Accuracy | Descriptions are correct: no missing core fields, no duplicates, no broken links | Wang & Strong 1996; Zaveri et al. 2016; Färber et al. 2018 |
| Consistency | The same subject and predicate do not carry conflicting values | Batini et al. 2009; Zaveri et al. 2016; Kontokostas et al. 2014 |
| Licensing / openness | Datasets declare a usable license | Neumaier et al. 2016; Wentzel et al. 2023 (reusability) |
| Provenance / lineage | Origin and processing history are recorded | PROV-O (W3C 2013); Zaveri et al. 2016 |
| Readability | Titles and descriptions are understandable to a human reader | Kincaid et al. 1975; Wang & Strong 1996 (representational) |
| Timeliness / currency | Metadata has been updated recently enough to be trusted | Wang & Strong 1996; Pipino et al. 2002; Batini et al. 2009 |
| Scalability | Assessment stays tractable as a catalog grows | An engineering concern; less standardized in the literature |
| Compatibility / interoperability | Two catalogs share structure and terms | Wentzel et al. 2023; DCAT (W3C 2024) |
| Similarity | Two catalogs overlap in what they describe | Jaccard 1912; Assaf et al. 2015 (deduplication) |
| Findability / accessibility | A resource can be located and retrieved | Wilkinson et al. 2016; Wentzel et al. 2023 |

The foundational taxonomies of Wang and Strong, Wand and Wang, and Batini and colleagues supply the parent categories (intrinsic, contextual, representational, accessibility) into which every one of these measures falls. ISO/IEC 25012 offers a normative alternative set of characteristics that a portal operator may prefer to adopt wholesale.

---

## 4. Research strands

### 4.1 Data quality foundations

Modern quality measurement rests on a small set of canonical papers. Wang and Strong gave the field its consumer-centered taxonomy of dimensions, sorted into intrinsic, contextual, representational, and accessibility groups (Wang & Strong 1996). Wand and Wang grounded those dimensions in ontological theory, giving a principled reason to measure completeness or accuracy rather than an ad hoc one (Wand & Wang 1996). Pipino, Lee, and Wang separated subjective judgment from objective measurement and offered reusable metric forms, including the simple ratio that many automated checks still use (Pipino et al. 2002). Batini and colleagues then surveyed the assessment and improvement methods themselves, the reference point any new method should locate itself against (Batini et al. 2009). Book-length treatments from Redman, Naumann, and the Sadiq handbook round out the definitions and the economics of poor quality (Redman 1996; Naumann 2002; Sadiq 2013). ISO/IEC 25012 turns the ideas into a de jure model of fifteen characteristics (ISO/IEC 2008).

### 4.2 Open data portal and metadata quality

This strand sits closest to a DCAT catalog tool. Reiche and Höfig were among the first to run metadata-quality metrics against a real government portal (Reiche & Höfig 2013). Vetrò and colleagues defined a measurement method covering completeness, accuracy, consistency, and traceability, then applied it to Italian open-government data (Vetrò et al. 2016). The most influential work here is the Open Data Portal Watch line from Neumaier, Umbrich, and Polleres, which defines objective, automatable metrics and runs them at scale across hundreds of CKAN, Socrata, and OpenDataSoft portals, tracking their evolution over time (Umbrich et al. 2015; Neumaier et al. 2016). Kubler and colleagues added a way to weight and aggregate those metrics into comparable per-portal scores using the Analytic Hierarchy Process, a direct answer to the question of how to combine dimensions fairly (Kubler et al. 2016; Kubler et al. 2018). Assaf, Troncy, and Senart built Roomba to validate, correct, and generate dataset profiles from portal metadata (Assaf et al. 2015). Máchová and Lněnička scored national portals on functionality and dataset quality together (Máchová & Lněnička 2017), and Nikiforova evaluated open data with a data-object-driven method (Nikiforova 2018).

The single closest published peer to a DCAT catalog quality tool is the work of Wentzel and colleagues at Fraunhofer FOKUS, who document the DCAT-AP quality method behind the European data portal's Metadata Quality Assessment service, mapping its dimensions to the FAIR principles and adding a SHACL validator for DCAT-AP conformance (Wentzel et al. 2023). Related work on open urban platforms shows the same harvest-then-assess pattern applied to smart-city catalogs (Lämmel et al. 2020). A recent review from Žnideršič and colleagues surveys these methods and is a useful companion to this document (Žnideršič et al. 2025).

### 4.3 Linked data and knowledge graph quality

The semantic-web community produced the field's most cited quality survey. Zaveri and colleagues consolidated thirty approaches into eighteen dimensions and sixty-nine metrics, and it remains the conceptual backbone for linked-data quality (Zaveri et al. 2016). Its methodology companion sets out a step-wise assessment process (Rula & Zaveri 2014). On the tooling side, Kontokostas and colleagues introduced RDFUnit, which auto-generates SPARQL test cases from schema constraints for test-driven quality evaluation (Kontokostas et al. 2014), and Debattista, Auer, and Lange built Luzzu, a pluggable assessment system with a declarative metric language and RDF-native result reporting (Debattista et al. 2016). The two W3C validation languages, SHACL and ShEx, turn constraint checking into a declarative, automatable operation over RDF graphs (Knublauch & Kontokostas 2017; Prud'hommeaux et al. 2014).

Applying these ideas to real knowledge graphs, Färber and colleagues assessed DBpedia, Freebase, OpenCyc, Wikidata, and YAGO against an operationalized criteria set (Färber et al. 2018). Broader surveys of knowledge-graph quality control (Wang et al. 2021), linked-data quality assessment (Nayak et al. 2022), and a 2026 analysis of assessment methods (Kropshofer & Wöß 2026) show that the area remains active, with validation-through-external-sources adding an accuracy angle that constraint checking alone misses (Huaman et al. 2021).

### 4.4 FAIR assessment tools

FAIR gave metadata quality a policy mandate. The Wilkinson principles named the goals of findability, accessibility, interoperability, and reusability (Wilkinson et al. 2016), and the follow-up metrics program turned them into fourteen measurable indicators (Wilkinson et al. 2018). The FAIR Evaluator implemented community-governed maturity indicators as automated compliance tests against a resource identifier (Wilkinson et al. 2019). The RDA maturity model then harmonized these heterogeneous checks into a shared indicator set with priorities (Bahim et al. 2020; RDA FAIR Data Maturity Model WG 2020). Operational tools followed: F-UJI scores a dataset automatically from its persistent identifier and harvested metadata (Devaraju & Huber 2021; Devaraju et al. 2021), FAIRshake offers configurable rubrics for research digital resources (Clarke et al. 2019), and FAIR-Checker evaluates FAIR metrics through SPARQL queries and SHACL over embedded RDF (Gaignard et al. 2023).

A caution belongs here, and it shapes the gaps in Section 6. Independent studies find that these tools disagree. Sun, Emonet, and Dumontier ran several automated evaluators on the same resources and recorded divergent scores (Sun et al. 2022). Krans and colleagues evaluated tool use and performance on real datasets (Krans et al. 2022). Candela, Mangione, and Pavone analyzed twenty tools and more than a thousand metrics and found widespread misalignment between what a metric claims to measure and what it actually measures (Candela et al. 2024). A further structural point: each of these tools targets an individual dataset or research object identified with a PID, not a whole DCAT catalog. Catalog-level properties like record-to-record duplication, distribution-level conformance, and cross-record consistency sit outside their design.

### 4.5 Standards and vocabularies

Automated assessment is only as portable as the vocabularies it speaks. DCAT is the W3C model for describing datasets and catalogs on the web, now at version 3 with version 2 still widely deployed through the DCAT-AP profile (Albertoni et al. 2024; Albertoni et al. 2020). The Data Quality Vocabulary gives a standard way to express quality measurements and annotations, which makes it the natural interchange format for scores produced anywhere (Albertoni & Isaac 2016). PROV-O standardizes how provenance is recorded and therefore how lineage completeness is checked (Lebo et al. 2013). Dublin Core Terms supply the descriptive properties most catalogs embed (DCMI 2020). Two measurement primitives complete the set: the Flesch-Kincaid grade level for readability (Kincaid et al. 1975) and the Jaccard index for set overlap and deduplication (Jaccard 1912).

---

## 5. Tool and method comparison

The table compares the software and operational methods that automate quality assessment. It is meant to be fair rather than promotional: DataQ is one option among several, with a distinct position rather than a universal advantage. Columns record the unit assessed (a single dataset, a whole catalog, or a graph), the target model, the dimensions covered, how automated the tool is, its output, and whether the source is open.

| Tool / method | Reference | Unit assessed | Target model | Dimensions covered | Automation | Output | Open source |
|---|---|---|---|---|---|---|---|
| **DataQ** | Martinez-Gil 2025 | Whole catalog (DCAT graph) | DCAT, DCT, PROV-O (RDF/Turtle) | completeness, accuracy, consistency, licensing, provenance, readability, timeliness, scalability; cross-catalog compatibility and similarity | Automated, one command, offline-deterministic | text / JSON / Markdown; DQV-mappable | MIT |
| data.europa.eu MQA | Wentzel et al. 2023 | Whole catalog (DCAT-AP) | DCAT-AP (RDF) + SHACL | findability, accessibility, interoperability, reusability, contextuality (FAIR-aligned) | Automated web service | dashboards, PDF | Partly open service |
| Open Data Portal Watch | Neumaier et al. 2016 | Many portals, per record | CKAN / Socrata mapped to DCAT | existence, conformance, retrievability, accuracy, openness | Automated crawler | reports, API | Research service |
| Roomba | Assaf et al. 2015 | Dataset profile | CKAN metadata | completeness, correctness (license, access, provenance) | Automated validate and correct | dataset profiles | Open (research) |
| Luzzu | Debattista et al. 2016 | Dataset / graph | RDF / linked data | pluggable: accessibility, intrinsic, representational, contextual | Semi-automated, metric language | daQ / DQV RDF | Open |
| RDFUnit | Kontokostas et al. 2014 | Dataset / graph | RDF, RDFS, OWL | consistency, accuracy, conformance, completeness | Automated SPARQL tests | RDF report | Open |
| SHACL | Knublauch & Kontokostas 2017 | Graph | RDF shapes | conformance, consistency, completeness | Declarative, automatable | RDF validation report | W3C standard |
| ShEx | Prud'hommeaux et al. 2014 | Graph | RDF shapes | structural conformance, completeness | Declarative | validation report | Open |
| F-UJI | Devaraju & Huber 2021 | Single dataset | DataCite, schema.org, DC | FAIR facets (F, A, I, R) | Automated web / API | per-metric score | Open |
| FAIRshake | Clarke et al. 2019 | Digital resource | configurable rubrics | FAIR (rubric-dependent) | Hybrid manual and automated | rubric scores | Open |
| FAIR Evaluator | Wilkinson et al. 2019 | Digital resource (GUID) | maturity indicators | FAIR facets | Automated tests | pass/fail per test | Open |
| FAIR-Checker | Gaignard et al. 2023 | Resource / metadata doc | embedded RDF (JSON-LD, RDFa) | FAIR metrics via SPARQL / SHACL | Automated | metric report | Open |

Reading across the rows, three positions stand out. The FAIR tools cluster at the single-dataset level and consume research-data metadata standards. The validation languages and RDFUnit check graph conformance but leave dimension scoring to the user. Only the European MQA and DataQ score a whole catalog across many dimensions at once, and they occupy different niches: MQA is an operational service tuned to DCAT-AP and the European portal, while DataQ is a small open-source library with transparent metric code, a test suite, and offline determinism, meant for research reuse and extension. The two are complements, not substitutes.

---

## 6. Open problems

**No shared benchmark or gold standard.** There is no agreed, openly published test set of catalogs with reference quality scores. Without one, methods cannot be ranked and claims cannot be replicated. This is the single largest gap, and it is the one a community resource can close fastest.

**Tools disagree on the same input.** Independent comparisons record divergent scores from different automated evaluators run on identical resources (Sun et al. 2022; Candela et al. 2024). Until metric definitions are pinned down and shared, a score is only meaningful relative to the tool that produced it.

**Dataset-level tools miss catalog-level faults.** FAIR evaluators score one dataset at a time. Duplication across records, uneven distribution-level conformance, and cross-record inconsistency are invisible at that granularity, yet they are precisely the faults that degrade a catalog.

**Aggregation and weighting are contested.** Combining several dimensions into one number requires a weighting choice. The AHP method of Kubler and colleagues is one principled option, but most tools either hide their weighting or avoid aggregation. Transparency about how a single score is formed matters more than the score itself.

**Scores are not interchangeable.** Most tools emit bespoke reports. Expressing results in the Data Quality Vocabulary would let scores from different tools be compared and tracked, but adoption is thin.

**Reproducibility is uneven.** Many published results cannot be re-run because the code, the data, or the exact tool version is unavailable. A quality method that cannot be reproduced is hard to trust.

**Human validation is scarce.** Few studies check automated scores against human judgment of the same catalogs, so the construct validity of most metrics is largely untested.

---

## 7. A research agenda

The gaps above suggest concrete, citable next steps.

1. **A public catalog-quality benchmark and leaderboard.** An openly licensed set of real catalogs with agreed reference scores, plus a leaderboard that any new method reports against. A benchmark becomes a reference point that later work cites as a matter of routine.
2. **Machine-actionable metric definitions in DQV.** Publishing each metric as a shared, executable definition expressed in the Data Quality Vocabulary would make scores portable and tool disagreement measurable rather than anecdotal.
3. **Catalog-level FAIR indicators.** A mapping from the RDA maturity indicators to catalog-level checks over DCAT would bridge the dataset-level FAIR tools and the catalog-level portal tools that currently ignore each other.
4. **Validation against human judgment.** Studies that correlate automated scores with expert ratings of the same catalogs would establish which metrics actually track perceived quality.
5. **Continuous assessment in portal pipelines.** Moving quality checks into the publication pipeline, so a portal is scored on every update rather than in one-off studies, would turn assessment from a research exercise into routine practice.

DataQ is offered as a starting point for items 1, 2, and 3: its metric code is short and readable, its outputs already map onto DQV, and adding a dimension is a small self-contained module.

---

## 8. Where DataQ fits

DataQ is the open-source reference implementation of the method in Martinez-Gil (2025). It reads a DCAT/RDF catalog and returns per-dimension scores plus a machine-readable report in one command. Its design choices answer several of the gaps above directly. Every metric is a small module with the arithmetic in plain sight, so a reviewer can audit exactly what a number means. Assessment is offline-deterministic, so the same catalog yields the same result on any machine. A test suite of 213 checks includes parity tests that assert the packaged metrics return values identical to the original reference scripts, which keeps the software honest as it changes. The bundled catalogs and a one-command benchmark make published numbers reproducible.

DataQ does not try to replace the FAIR evaluators or the European MQA service. It occupies the open, reproducible, research-friendly niche: a place to prototype a new dimension, to run a fair cross-portal comparison, or to teach how catalog quality is measured. Researchers who want to build on it, disagree with it, or extend its dimension set are the intended audience, and every such use is a citation the method earns on merit.

---

## 9. Contributing to this survey

This is a living document. The fastest way to keep it accurate is community correction. If a reference is wrong, a tool is missing, or a new method has appeared, open a pull request against [`references.bib`](references.bib) and the tables here. The process, and the small format each entry follows, are described in [CONTRIBUTING.md](CONTRIBUTING.md). Contributors are credited in the repository history.

---

## References

Full, verified entries with resolvable identifiers are in [`references.bib`](references.bib). Grouped here for reading.

**Foundations.** Wang & Strong 1996, [doi:10.1080/07421222.1996.11518099](https://doi.org/10.1080/07421222.1996.11518099) · Wand & Wang 1996, [doi:10.1145/240455.240479](https://doi.org/10.1145/240455.240479) · Pipino, Lee & Wang 2002, [doi:10.1145/505248.506010](https://doi.org/10.1145/505248.506010) · Batini, Cappiello, Francalanci & Maurino 2009, [doi:10.1145/1541880.1541883](https://doi.org/10.1145/1541880.1541883) · Redman 1996 (Artech House) · Naumann 2002, [doi:10.1007/3-540-45921-9](https://doi.org/10.1007/3-540-45921-9) · Sadiq (ed.) 2013, [doi:10.1007/978-3-642-36257-6](https://doi.org/10.1007/978-3-642-36257-6) · ISO/IEC 25012:2008, [iso.org/standard/35736](https://www.iso.org/standard/35736.html).

**Open data portal and metadata quality.** Reiche & Höfig 2013, [doi:10.1109/COMPSACW.2013.32](https://doi.org/10.1109/COMPSACW.2013.32) · Umbrich, Neumaier & Polleres 2015, [doi:10.1109/FiCloud.2015.82](https://doi.org/10.1109/FiCloud.2015.82) · Vetrò et al. 2016, [doi:10.1016/j.giq.2016.02.001](https://doi.org/10.1016/j.giq.2016.02.001) · Neumaier, Umbrich & Polleres 2016, [doi:10.1145/2964909](https://doi.org/10.1145/2964909) · Kubler et al. 2016, [doi:10.1145/2912160.2912167](https://doi.org/10.1145/2912160.2912167) · Kubler et al. 2018, [doi:10.1016/j.giq.2017.11.003](https://doi.org/10.1016/j.giq.2017.11.003) · Assaf, Troncy & Senart 2015, [doi:10.1007/978-3-319-25639-9_46](https://doi.org/10.1007/978-3-319-25639-9_46) · Máchová & Lněnička 2017, [doi:10.4067/S0718-18762017000100003](https://doi.org/10.4067/S0718-18762017000100003) · Nikiforova 2018, [doi:10.22364/bjmc.2018.6.4.04](https://doi.org/10.22364/bjmc.2018.6.4.04) · Lämmel et al. 2020, [doi:10.1145/3409795](https://doi.org/10.1145/3409795) · Wentzel et al. 2023, [doi:10.1007/978-3-031-41138-0_17](https://doi.org/10.1007/978-3-031-41138-0_17) · Žnideršič, Marolt & Pesek 2025, [doi:10.15388/25-INFOR614](https://doi.org/10.15388/25-INFOR614).

**Linked data and knowledge graph quality.** Prud'hommeaux, Labra Gayo & Solbrig 2014 (ShEx), [doi:10.1145/2660517.2660523](https://doi.org/10.1145/2660517.2660523) · Kontokostas et al. 2014 (RDFUnit), [doi:10.1145/2566486.2568002](https://doi.org/10.1145/2566486.2568002) · Rula & Zaveri 2014, [ceur-ws.org/Vol-1215](https://ceur-ws.org/Vol-1215/) · Zaveri et al. 2016, [doi:10.3233/SW-150175](https://doi.org/10.3233/SW-150175) · Debattista, Auer & Lange 2016 (Luzzu), [doi:10.1145/2992786](https://doi.org/10.1145/2992786) · Färber et al. 2018, [doi:10.3233/SW-170275](https://doi.org/10.3233/SW-170275) · Huaman, Tauqeer & Fensel 2021, [doi:10.1007/978-3-030-91305-2_4](https://doi.org/10.1007/978-3-030-91305-2_4) · Wang et al. 2021, [doi:10.1016/j.fmre.2021.09.003](https://doi.org/10.1016/j.fmre.2021.09.003) · Nayak, Božić & Longo 2022, [doi:10.1007/978-3-030-96140-4_5](https://doi.org/10.1007/978-3-030-96140-4_5) · Kropshofer & Wöß 2026, [doi:10.1145/3748522.3779741](https://doi.org/10.1145/3748522.3779741).

**FAIR principles and assessment.** Wilkinson et al. 2016, [doi:10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18) · Wilkinson et al. 2018, [doi:10.1038/sdata.2018.118](https://doi.org/10.1038/sdata.2018.118) · Clarke et al. 2019 (FAIRshake), [doi:10.1016/j.cels.2019.09.011](https://doi.org/10.1016/j.cels.2019.09.011) · Wilkinson et al. 2019 (FAIR Evaluator), [doi:10.1038/s41597-019-0184-5](https://doi.org/10.1038/s41597-019-0184-5) · Bahim et al. 2020, [doi:10.5334/dsj-2020-041](https://doi.org/10.5334/dsj-2020-041) · RDA FAIR Data Maturity Model WG 2020, [doi:10.15497/rda00050](https://doi.org/10.15497/rda00050) · Devaraju & Huber 2021 (F-UJI), [doi:10.1016/j.patter.2021.100370](https://doi.org/10.1016/j.patter.2021.100370) · Devaraju et al. 2021, [doi:10.5334/dsj-2021-004](https://doi.org/10.5334/dsj-2021-004) · Sun, Emonet & Dumontier 2022, [ceur-ws.org/Vol-3127](https://ceur-ws.org/Vol-3127/paper-6.pdf) · Krans et al. 2022, [doi:10.1016/j.impact.2022.100402](https://doi.org/10.1016/j.impact.2022.100402) · Gaignard et al. 2023 (FAIR-Checker), [doi:10.1186/s13326-023-00289-5](https://doi.org/10.1186/s13326-023-00289-5) · Candela, Mangione & Pavone 2024, [doi:10.5334/dsj-2024-033](https://doi.org/10.5334/dsj-2024-033).

**Standards and vocabularies.** DCAT v3 (W3C 2024), [w3.org/TR/vocab-dcat-3](https://www.w3.org/TR/vocab-dcat-3/) · DCAT v2 (W3C 2020), [w3.org/TR/vocab-dcat-2](https://www.w3.org/TR/vocab-dcat-2/) · DQV (W3C 2016), [w3.org/TR/vocab-dqv](https://www.w3.org/TR/vocab-dqv/) · PROV-O (W3C 2013), [w3.org/TR/prov-o](https://www.w3.org/TR/prov-o/) · SHACL (W3C 2017), [w3.org/TR/shacl](https://www.w3.org/TR/shacl/) · DCMI Metadata Terms, [dublincore.org](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) · Kincaid et al. 1975, [eric.ed.gov/?id=ED108134](https://eric.ed.gov/?id=ED108134) · Jaccard 1912, [doi:10.1111/j.1469-8137.1912.tb05611.x](https://doi.org/10.1111/j.1469-8137.1912.tb05611.x).

---

## How to cite this survey

The survey travels with the DataQ software and its reference paper. Please cite the paper:

```bibtex
@article{martinezgil2025dataq,
  author  = {Martinez-Gil, Jorge},
  title   = {Framework to Automatically Determine the Quality of Open Data Catalogs},
  journal = {Expert Systems with Applications},
  volume  = {289},
  pages   = {128379},
  year    = {2025},
  doi     = {10.1016/j.eswa.2025.128379},
}
```

Martinez-Gil, J. (2025). Framework to automatically determine the quality of open data catalogs. *Expert Systems with Applications*, *289*, 128379. [https://doi.org/10.1016/j.eswa.2025.128379](https://doi.org/10.1016/j.eswa.2025.128379)
