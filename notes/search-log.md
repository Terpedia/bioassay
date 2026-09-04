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

## Current verified sample

The first extraction pass verified AIDs 332912, 338300, and 1189 for exact
compound-level rows. The resulting observations and limitations are recorded
in `data/priority-assay-observations.csv` and are not a substitute for the
complete review search.

## Reproducibility rules

- Save the exact query and snapshot identifier with every aggregate.
- Filter assay results by exact PubChem CID, not by name alone.
- Preserve AID, SID, source accession, endpoint, relation, value, units, and
  outcome.
- Treat AID linkage as coverage until the compound-level result row is checked.
- Record endpoint/context failures rather than excluding them silently.
