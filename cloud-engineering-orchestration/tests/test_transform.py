import pandas as pd
import pytest
from cloud_pipeline.transform import validate_and_transform

def test_transform_removes_invalid_rows_and_sorts():
    frame = pd.DataFrame([
        {"event_time":"2026-01-01T01:00:00Z","energy_kwh":2.0,"site":" b "},
        {"event_time":"bad-date","energy_kwh":3.0,"site":"a"},
        {"event_time":"2026-01-01T00:00:00Z","energy_kwh":1.0,"site":"a"},
        {"event_time":"2026-01-01T02:00:00Z","energy_kwh":-1.0,"site":"a"},
    ])
    result = validate_and_transform(frame)
    assert len(result) == 2
    assert result.iloc[0]["site"] == "a"
    assert result.iloc[1]["site"] == "b"

def test_transform_rejects_missing_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_and_transform(pd.DataFrame({"event_time": []}))
