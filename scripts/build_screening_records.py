"""Turn PubMed candidates into an explicit, initially unreviewed screening file."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main() -> None:
    source = DATA / "pubmed-priority-panel-candidates.csv"
    output = DATA / "pubmed-screening-records.csv"
    with source.open(newline="") as handle:
        candidates = list(csv.DictReader(handle))
    fields = ["record_id", "source", "source_record_id", "title_or_assay_name",
              "compound_identity", "stereochemistry_resolved", "assay_system", "endpoint",
              "full_text_status", "include_status", "exclusion_reason", "reviewer",
              "decision_date", "notes"]
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in candidates:
            writer.writerow({"record_id": f"PMID:{row['pmid']}", "source": "PubMed",
                             "source_record_id": row["pmid"], "title_or_assay_name": row["title"],
                             "compound_identity": row["compound_query"],
                             "stereochemistry_resolved": "unknown", "assay_system": "unknown",
                             "endpoint": "unknown", "full_text_status": "not_checked",
                             "include_status": "unreviewed", "exclusion_reason": "",
                             "reviewer": "", "decision_date": "", "notes": row["doi"]})
    print(f"Wrote {len(candidates)} unreviewed screening records")


if __name__ == "__main__":
    main()
