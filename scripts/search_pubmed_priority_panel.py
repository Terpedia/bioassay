"""Run and archive the reproducible PubMed priority-panel search.

This script stores candidate records only. It does not make inclusion decisions.
"""

import csv
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "notes"
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

COMPOUNDS = [
    "beta-caryophyllene", "beta-myrcene", "nerolidol", "linalool", "alpha-pinene",
    "borneol", "alpha-bisabolol", "d-limonene", "l-limonene", "terpinolene", "fenchol",
]


def request_xml(endpoint: str, params: dict[str, str]) -> ET.Element:
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{BASE}/{endpoint}?{query}", timeout=60) as response:
        return ET.fromstring(response.read())


def search(term: str) -> list[str]:
    first = request_xml("esearch.fcgi", {"db": "pubmed", "term": term, "retstart": "0",
                                         "retmax": "1000", "retmode": "xml"})
    total = int(first.findtext(".//Count", default="0"))
    ids = [node.text for node in first.findall(".//Id") if node.text]
    for start in range(1000, total, 1000):
        root = request_xml("esearch.fcgi", {"db": "pubmed", "term": term,
                                             "retstart": str(start), "retmax": "1000", "retmode": "xml"})
        ids.extend(node.text for node in root.findall(".//Id") if node.text)
        time.sleep(0.35)
    return ids


def fetch(pmids: list[str]) -> list[dict[str, str]]:
    if not pmids:
        return []
    root = request_xml("efetch.fcgi", {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"})
    records = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID", default="")
        title = " ".join(article.findtext(".//ArticleTitle", default="").split())
        abstract = " ".join(" ".join(" ".join(node.itertext()).split())
                            for node in article.findall(".//AbstractText"))
        journal = article.findtext(".//Journal/Title", default="")
        year = article.findtext(".//PubDate/Year", default="") or article.findtext(".//PubDate/MedlineDate", default="")[:4]
        doi = ""
        for aid in article.findall(".//ArticleId"):
            if aid.attrib.get("IdType") == "doi":
                doi = aid.text or ""
        records.append({"pmid": pmid, "title": title, "abstract": abstract, "journal": journal,
                        "year": year, "doi": doi})
    return records


def main() -> None:
    retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    query_rows = []
    all_records: dict[str, dict[str, str]] = {}
    for compound in COMPOUNDS:
        term = f'"{compound}"[Title/Abstract] AND (bioassay OR bioactivity OR pharmacology OR receptor OR antimicrobial)'
        ids = search(term)
        query_rows.append({"compound": compound, "query": term, "candidate_count": len(ids),
                           "retrieved_at_utc": retrieved_at})
        for offset in range(0, len(ids), 200):
            for record in fetch(ids[offset:offset + 200]):
                record["compound_query"] = compound
                record["retrieved_at_utc"] = retrieved_at
                all_records.setdefault(record["pmid"], record)
            time.sleep(0.35)
        time.sleep(0.35)

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "pubmed-priority-panel-queries-2026-09-04.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(query_rows[0]))
        writer.writeheader()
        writer.writerows(query_rows)
    fields = ["pmid", "compound_query", "title", "abstract", "journal", "year", "doi", "retrieved_at_utc"]
    with (DATA / "pubmed-priority-panel-candidates.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_records.values())
    (OUT / "pubmed-priority-panel-search.json").write_text(json.dumps({"retrieved_at_utc": retrieved_at,
        "database": "PubMed", "candidate_record_count": len(all_records), "queries": query_rows}, indent=2) + "\n")
    print(f"Archived {len(all_records)} unique PubMed candidates from {len(COMPOUNDS)} compound queries")


if __name__ == "__main__":
    main()
