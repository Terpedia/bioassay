from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    compound: str
    assay: str
    concentration: float
    unit: str
    replicate: int
    sample_signal: float
    positive_control: float
    negative_control: float


@dataclass(frozen=True)
class Summary:
    compound: str
    assay: str
    concentration: float
    unit: str
    n: int
    mean_activity: float
    sd_activity: float | None
