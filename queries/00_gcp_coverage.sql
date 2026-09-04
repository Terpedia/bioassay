-- Read-only coverage query for the Terpedia GCP PubChem BioAssay snapshot.
-- Coverage and assay counts are not measurements of terpene activity.
WITH ids AS (
  SELECT DISTINCT terpene_id, TRIM(cid) AS pubchem_cid
  FROM `terpedia-489015.terpedia_core.terpene_pubchem_lookup_20260904`,
    UNNEST(SPLIT(pubchem_cids, ";")) AS cid
  WHERE terpene_id IS NOT NULL AND pubchem_cids IS NOT NULL
), assays AS (
  SELECT pubchem_cid, bioassay_count
  FROM `terpedia-489015.terpedia_core.terpene_pubchem_bioassay_lookup_20260904`
)
SELECT
  COUNT(DISTINCT ids.terpene_id) AS terpene_ids_with_pubchem,
  COUNT(DISTINCT IF(assays.bioassay_count > 0, ids.terpene_id, NULL))
    AS terpene_ids_with_any_assay,
  COUNT(DISTINCT IF(assays.bioassay_count = 0, ids.terpene_id, NULL))
    AS terpene_ids_with_zero_assay,
  COUNT(*) AS cid_links
FROM ids
LEFT JOIN assays USING (pubchem_cid);
