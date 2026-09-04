# PRISMA-ScR flow specification

The final manuscript will report the study-selection flow from the screening
file rather than from database row counts. The current GCP BioAssay counts are
coverage denominators and must not be used as the number of included studies.

The PubMed candidate export is an identification-stage artifact. Its rows are
all `unreviewed` until eligibility and full-text checks are completed; the
current export must not be described as the number of included studies.

## Required flow counts

| Stage | Count source |
|---|---|
| Records identified from PubMed | Screening log, `source=PubMed` |
| Records identified from PubChem BioAssay/ChEMBL | Screening log, source fields |
| Records identified from Terpedia | Screening log, source fields |
| Duplicate records removed | Deduplication audit |
| Title/abstract records screened | Screening log |
| Records excluded at title/abstract | Screening log plus reason |
| Full-text reports sought | Screening log |
| Full-text reports unavailable | Screening log |
| Full-text reports excluded | Screening log plus reason |
| Studies included in evidence map | `include_status=included` |
| Assay records included | Extracted assay table |

## Minimum exclusion vocabulary

Use one primary reason per excluded record: `not_terpene`, `no_experimental_assay`,
`identity_unresolved`, `no_assay_context`, `review_or_secondary`,
`duplicate_report`, `full_text_unavailable`, or `out_of_scope`.

## Reporting rule

Any post hoc change to eligibility or deduplication rules must be logged with a
date, reason, and affected record count before the Results section is updated.
