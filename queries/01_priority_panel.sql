-- Identity-safe priority panel. Names are resolved outside BigQuery through
-- PubChem PUG and retained in data/priority-compound-identity-crosswalk.csv.
WITH priority_cids AS (
  SELECT cid
  FROM UNNEST([
    '5281515', '31253', '5284507', '6549', '6654', '64685',
    '1549992', '440917', '439250', '11463', '15406'
  ]) AS cid
)
SELECT
  p.pubchem_cid,
  p.bioassay_count,
  p.pubchem_aids,
  p.retrieved_at
FROM `terpedia-489015.terpedia_core.terpene_pubchem_bioassay_lookup_20260904` AS p
JOIN priority_cids ON p.pubchem_cid = priority_cids.cid
ORDER BY SAFE_CAST(pubchem_cid AS INT64);
