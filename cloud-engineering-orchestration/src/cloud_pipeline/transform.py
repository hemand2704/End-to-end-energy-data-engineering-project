import pandas as pd

REQUIRED_COLUMNS = ["event_time", "energy_kwh", "site"]

def validate_and_transform(dataframe):
    missing = [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    result = dataframe.copy()
    result["event_time"] = pd.to_datetime(result["event_time"], utc=True, errors="coerce")
    result["energy_kwh"] = pd.to_numeric(result["energy_kwh"], errors="coerce")
    result["site"] = result["site"].astype("string").str.strip()

    result = result.dropna(subset=REQUIRED_COLUMNS)
    result = result[(result["energy_kwh"] >= 0) & (result["site"] != "")]
    result = result.sort_values(["site", "event_time"]).reset_index(drop=True)

    if result.empty:
        raise ValueError("No valid rows remain after validation")
    return result
