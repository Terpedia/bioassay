# Review protocol

## Review type

This is a structured scoping review with quantitative extraction where assay
data are sufficiently comparable. A meta-analysis is not assumed: IC50, EC50,
Ki, percent effect, and endpoint-specific readouts will not be pooled without
an explicit compatibility decision.

## Eligibility

Include primary studies that:

1. test an identified terpene or terpene-rich preparation;
2. report an experimental bioassay or biochemical/cellular functional assay;
3. identify the assay system, endpoint, and concentration or dose; and
4. provide enough information to distinguish measured activity from inference.

Exclude or separately label reviews, marketing claims, docking-only studies,
sequence/structure predictions, and studies where the tested material cannot
be chemically identified.

## Required extraction fields

Each study record should preserve:

- exact compound name, stereochemistry, salt/formulation, and identity source;
- assay target/system, species, expression context, and assay format;
- endpoint, direction of effect, units, concentration range, and controls;
- replicate information, curve-fit/model, uncertainty, and cytotoxicity controls;
- source DOI/PMID/database accession and full-text location;
- evidence tier and unresolved limitations.

## Evidence tiers

`A` = direct, identity-resolved, concentration-dependent activity with an
appropriate control and assay context.

`B` = measured activity with important limitations such as incomplete
concentration-response, uncertain stereochemistry, or limited controls.

`C` = indirect or low-context evidence, including crude mixtures, phenotypic
reports without target resolution, or database annotations.

`H` = hypothesis only: prediction, docking, structural compatibility, or an
unresolved literature/database lead.

Absence of a qualifying record is reported as an evidence gap, not as proof of
inactivity.

## Planned workflow

1. Freeze the search date and database/source versions.
2. Build an identity-resolved terpene list and synonym crosswalk.
3. Search PubChem BioAssay, ChEMBL, PubMed, and the Terpedia source inventory.
4. Deduplicate studies while retaining every assay and source accession.
5. Extract assay-level observations into a machine-readable table.
6. Audit identity, controls, endpoint comparability, and evidence tier.
7. Produce compound-by-assay summaries and a narrative synthesis.

For the initial priority panel, the GCP CID-to-AID lookup is the denominator.
Underlying assay records are then retrieved from the versioned PubChem BioAssay
XML/RDF or PubChem assay service and filtered back to the exact PubChem CID.
An AID attached to a CID is not treated as a positive result until the
compound-level result row, endpoint, units, and outcome are verified.

## Interpretation boundary

An assay signal does not by itself establish therapeutic efficacy, in-vivo
exposure, receptor selectivity, mechanism, safety, or clinical relevance.
