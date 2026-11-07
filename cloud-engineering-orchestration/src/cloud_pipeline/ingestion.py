from pathlib import Path
import pandas as pd

SAMPLE_ROWS = [
    {"event_time": "2026-01-01T00:00:00Z", "energy_kwh": 12.4, "site": "site_a"},
    {"event_time": "2026-01-01T01:00:00Z", "energy_kwh": 10.8, "site": "site_a"},
    {"event_time": "2026-01-01T00:00:00Z", "energy_kwh": 8.2, "site": "site_b"},
    {"event_time": "2026-01-01T01:00:00Z", "energy_kwh": 9.1, "site": "site_b"},
]

def create_sample_data(output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(SAMPLE_ROWS).to_csv(path, index=False)
    return path

def read_input_csv(input_path):
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Input CSV does not exist: {path}")
    return pd.read_csv(path)
