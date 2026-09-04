# Terpene Bioassay Activity Review

A manuscript workspace and small, evidence-aware toolkit for reviewing terpene
bioassay activity.

The working article is [`manuscript/article.md`](manuscript/article.md). The
review protocol and extraction schema are in [`protocol.md`](protocol.md).

The first GCP-backed coverage snapshot is recorded in
[`data/gcp-bioassay-coverage-2026-09-04.csv`](data/gcp-bioassay-coverage-2026-09-04.csv),
with the reproducible query in [`queries/00_gcp_coverage.sql`](queries/00_gcp_coverage.sql).
Claim and hypothesis registers are maintained in the sibling Terpedia
[`claims/data/`](../claims/data/) directory.

The initial project focuses on a safe, reproducible first pass:

- load tidy CSV assay observations;
- calculate percent activity from sample, positive-control, and negative-control wells;
- summarize replicate measurements without hiding missing values;
- preserve the distinction between an assay signal and a biological claim.

## Input format

CSV files should contain these columns:

```text
compound,assay,concentration,unit,replicate,sample_signal,positive_control,negative_control
```

`sample_signal`, `positive_control`, and `negative_control` are numeric readouts
on the same scale. The normalized activity is calculated as:

```text
100 * (sample - negative_control) / (positive_control - negative_control)
```

## Quick start

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'

bioassay summarize examples/results.csv
pytest
```

The summary output is tab-separated so it can be redirected into a file or
opened in a spreadsheet.

## Review question

Which terpene compounds have reproducible, identity-resolved activity in
defined bioassay systems, against which targets or phenotypes, and with what
limitations in potency, selectivity, assay format, and biological relevance?

The review will separate direct experimental activity from database
annotations, docking/model predictions, ethnobotanical reports, and claims
that are only inferred from chemical class or target association.

## Scope and interpretation

This package reports assay measurements and normalization only. It does not
infer potency, receptor binding, efficacy, selectivity, toxicity, or human
relevance. Those conclusions require assay-specific validation and evidence
review.

## License

To be selected before publication.
