"""Create the first manuscript figure with a dependency-free SVG renderer."""

import csv
import html
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "manuscript" / "figures"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def label(x: float, y: float, value: str, size: int = 13, weight: str = "400",
          anchor: str = "start", fill: str = "#23323b") -> str:
    return (f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" '
            f'font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}" '
            f'fill="{fill}">{esc(value)}</text>')


def main() -> None:
    identity = load_rows(DATA / "priority-compound-identity-crosswalk.csv")
    observations = load_rows(DATA / "priority-assay-observations.csv")
    observed = {row["compound"] for row in observations if row["endpoint"] != "unknown"}
    flagged = {row["compound"] for row in observations if row["endpoint"] == "unknown"}
    matched = sorted((row for row in identity if row["GCP_lookup_status"] == "matched"),
                    key=lambda row: int(row["GCP_bioassay_count"]))
    display = sorted(identity, key=lambda row: row["compound"].lower())
    colors = {"verified": "#1b4965", "flag": "#ca6702", "pending": "#8d99ae", "absent": "#bfc0c0"}

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="580" viewBox="0 0 1050 580">',
             '<rect width="1050" height="580" fill="white"/>',
             label(525, 30, "Terpene priority panel: coverage is broader than interpretable assay evidence", 17, "700", "middle"),
             label(28, 66, "A  GCP-linked assay coverage", 14, "700"),
             label(545, 66, "B  Assay-context verification", 14, "700")]

    x0, x1, y0 = 205, 480, 105
    for tick in (0, 100, 200, 300, 400, 500):
        x = x0 + tick / 580 * (x1 - x0)
        parts.append(f'<line x1="{x}" y1="{y0 - 12}" x2="{x}" y2="430" stroke="#d9e2e8" stroke-width="1"/>')
        parts.append(label(x, 450, str(tick), 11, anchor="middle", fill="#53636d"))
    for i, row in enumerate(matched):
        y = y0 + i * 48
        value = int(row["GCP_bioassay_count"])
        width = value / 580 * (x1 - x0)
        parts += [label(x0 - 10, y + 18, row["compound"], 12, anchor="end"),
                  f'<rect x="{x0}" y="{y}" width="{width:.1f}" height="26" fill="#1b4965"/>',
                  label(x0 + width + 8, y + 18, f"{value:,}", 11)]
    parts.append(label((x0 + x1) / 2, 475, "Linked PubChem BioAssay records (count)", 12, anchor="middle"))

    for i, row in enumerate(display):
        y = 105 + i * 30
        compound = row["compound"]
        status = ("verified" if compound in observed else "flag" if compound in flagged
                  else "pending" if row["GCP_lookup_status"] == "matched" else "absent")
        parts += [label(715, y + 18, compound, 12, anchor="end"),
                  f'<circle cx="760" cy="{y + 13}" r="8" fill="{colors[status]}" stroke="white" stroke-width="1"/>']
    legend = [("verified", "Verified result row"), ("flag", "Flag; context incomplete"),
              ("pending", "GCP-linked; extraction pending"), ("absent", "No exact GCP row")]
    for i, (key, description) in enumerate(legend):
        x, y = 545 + (i % 2) * 235, 475 + (i // 2) * 25
        parts += [f'<circle cx="{x}" cy="{y - 4}" r="7" fill="{colors[key]}"/>', label(x + 14, y, description, 11)]
    parts += [label(28, 555, "GCP snapshot: 2026-09-04. A linked AID is not itself a positive activity result.", 10, fill="#53636d"), '</svg>']

    OUT.mkdir(parents=True, exist_ok=True)
    svg = OUT / "figure1-priority-panel.svg"
    svg.write_text("\n".join(parts), encoding="utf-8")
    subprocess.run(["rsvg-convert", "-o", str(OUT / "figure1-priority-panel.png"), str(svg)], check=True)
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(OUT / "figure1-priority-panel.pdf"), str(svg)], check=True)


if __name__ == "__main__":
    main()
