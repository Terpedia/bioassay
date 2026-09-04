import pytest

from bioassay import Observation, normalize_activity, summarize


def test_normalize_activity():
    assert normalize_activity(50, 80, 20) == pytest.approx(50)


def test_zero_control_span_is_rejected():
    with pytest.raises(ValueError, match="controls must differ"):
        normalize_activity(10, 10, 10)


def test_summary_keeps_out_of_range_signal_and_computes_sample_sd():
    observations = [
        Observation("x", "a", 1, "uM", 1, 20, 80, 20),
        Observation("x", "a", 1, "uM", 2, 80, 80, 20),
    ]
    result = summarize(observations)[0]
    assert result.n == 2
    assert result.mean_activity == pytest.approx(50)
    assert result.sd_activity == pytest.approx(70.710678)
