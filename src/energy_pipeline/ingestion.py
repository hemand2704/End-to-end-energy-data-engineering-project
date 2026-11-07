from pathlib import Path
from zipfile import ZipFile
import io
import requests
import pandas as pd

UCI_URL = "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"
COLUMNS = ["Date", "Time", "Global_active_power", "Global_reactive_power", "Voltage", "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]

def create_sample_csv(output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ["01/01/2007","00:00:00","2.580","0.136","241.97","10.6","0.0","0.0","0.0"],
        ["01/01/2007","00:01:00","2.552","0.130","241.75","10.4","0.0","0.0","0.0"],
        ["01/01/2007","00:02:00","2.550","0.128","241.60","10.4","0.0","0.0","0.0"],
        ["02/01/2007","00:00:00","1.120","0.090","240.20","4.8","0.0","1.0","0.0"],
        ["02/01/2007","00:01:00","1.100","0.088","240.10","4.7","0.0","1.0","0.0"],
    ]
    pd.DataFrame(rows, columns=COLUMNS).to_csv(output_path, index=False, sep=";")
    return output_path

def download_uci_dataset(output_dir, url=UCI_URL):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    with ZipFile(io.BytesIO(response.content)) as archive:
        match = next((n for n in archive.namelist() if n.lower().endswith("household_power_consumption.txt")), None)
        if not match:
            raise FileNotFoundError("Expected household_power_consumption.txt in UCI archive")
        target = output_dir / "household_power_consumption.txt"
        target.write_bytes(archive.read(match))
    return target
