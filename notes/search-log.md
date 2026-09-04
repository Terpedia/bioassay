# Search and extraction log

## Snapshot and access date

- Access date: 2026-09-04 (UTC)
- GCP project: `terpedia-489015`
- GCP region: `us-central1`
- GCP coverage table: `terpedia_core.terpene_pubchem_bioassay_lookup_20260904`
- Terpedia-to-PubChem table: `terpedia_core.terpene_pubchem_lookup_20260904`
- PubChem BioAssay raw archive: `gs://terpedia-knowledge-raw/raw/pubchem-bioassay-xml/`

## Queries and resources used

1. `queries/00_gcp_coverage.sql` — corpus coverage counts.
2. `queries/01_priority_panel.sql` — exact-CID priority-panel lookup.
3. PubChem PUG REST compound properties — identity crosswalk.
4. PubChem PUG REST assay description and CSV endpoints — assay-level verification.

The PubMed query runner paginates E-utilities results in 1,000-record pages;
the saved query CSV records the final candidate count for each compound query.
The first run before pagination was discarded as a denominator because four
queries reached the page cap.

## Current verified sample

The first extraction pass verified AIDs 332912, 338300, and 1189 for exact
compound-level rows. The resulting observations and limitations are recorded
in `data/priority-assay-observations.csv` and are not a substitute for the
complete review search.

The current PubMed candidate export is `data/pubmed-priority-panel-candidates.csv`.
Every row is copied into `data/pubmed-screening-records.csv` with
`include_status=unreviewed`; no candidate is treated as included until title,
abstract, identity, and full-text eligibility are reviewed.

The 11 query counts sum to 9,386 hits. PMID-level deduplication yields 7,861
unique candidates. The `retmax` pagination limit is handled in
`scripts/search_pubmed_priority_panel.py`.

## Reproducibility rules

- Save the exact query and snapshot identifier with every aggregate.
- Filter assay results by exact PubChem CID, not by name alone.
- Preserve AID, SID, source accession, endpoint, relation, value, units, and
  outcome.
- Treat AID linkage as coverage until the compound-level result row is checked.
- Record endpoint/context failures rather than excluding them silently.
