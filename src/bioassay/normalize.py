def normalize_activity(
    sample_signal: float,
    positive_control: float,
    negative_control: float,
) -> float:
    """Return signal normalized to negative=0 and positive=100.

    A zero control span is rejected because normalization would be undefined.
    Values outside 0--100 are retained: they can indicate assay behavior that
    deserves review and should not be silently clipped.
    """
    span = positive_control - negative_control
    if span == 0:
        raise ValueError("positive and negative controls must differ")
    return 100.0 * (sample_signal - negative_control) / span
