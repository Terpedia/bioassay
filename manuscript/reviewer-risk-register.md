# Reviewer-risk register

| Likely reviewer concern | Manuscript response / required evidence |
|---|---|
| PubChem assay counts are mistaken for positive activity | Separate coverage denominator from verified compound-level result rows in Figure 1 and Table 1 |
| Compound names hide stereochemistry | Retain CID, InChIKey, structure title, and tested form in the identity crosswalk |
| MIC, percent activity, and receptor potency are pooled | Keep endpoints in separate evidence domains; no universal activity score |
| Database absence is interpreted as inactivity | Report absent exact rows as coverage gaps |
| Extracted assay records are not independent studies | Preserve AID, SID, source accession, and publication identifiers; deduplicate at study level |
| Single-concentration or flag-only results are overinterpreted | Use `context-limited` status and explicit interpretation boundaries |
| Evidence map is not a systematic review | Complete screening log, exclusion reasons, PRISMA-ScR counts, and search reproducibility before submission |
| GCP snapshot may change | Freeze table names, retrieval timestamps, query text, and manifest/source version |
| In-vitro activity is translated into human efficacy | Separate assay signal, organism-level phenotype, exposure, and clinical relevance throughout |
| Review is too broad for a coherent synthesis | Limit the priority panel and organize the paper by assay domain, identity quality, and endpoint comparability |
