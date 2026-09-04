import csv
import math
from collections import defaultdict
from pathlib import Path

from .models import Observation, Summary
from .normalize import normalize_activity


def read_csv(path: str | Path) -> list[Observation]:
    with Path(path).open(newline="") as handle:
        rows = csv.DictReader(handle)
        required = {
            "compound", "assay", "concentration", "unit", "replicate",
            "sample_signal", "positive_control", "negative_control",
        }
        missing = required - set(rows.fieldnames or [])
        if missing:
            raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
        return [Observation(
            compound=row["compound"], assay=row["assay"],
            concentration=float(row["concentration"]), unit=row["unit"],
            replicate=int(row["replicate"]), sample_signal=float(row["sample_signal"]),
            positive_control=float(row["positive_control"]),
            negative_control=float(row["negative_control"]),
        ) for row in rows]


def summarize(observations: list[Observation]) -> list[Summary]:
    grouped: dict[tuple[str, str, float, str], list[float]] = defaultdict(list)
    for obs in observations:
        key = (obs.compound, obs.assay, obs.concentration, obs.unit)
        grouped[key].append(normalize_activity(obs.sample_signal, obs.positive_control,
                                               obs.negative_control))
    results = []
    for (compound, assay, concentration, unit), values in sorted(grouped.items()):
        mean = sum(values) / len(values)
        sd = None if len(values) < 2 else math.sqrt(sum((x - mean) ** 2 for x in values) / (len(values) - 1))
        results.append(Summary(compound, assay, concentration, unit, len(values), mean, sd))
    return results
