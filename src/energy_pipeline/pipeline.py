import argparse
import logging
from pathlib import Path
from energy_pipeline.config import load_config, PROJECT_ROOT
from energy_pipeline.ingestion import create_sample_csv, download_uci_dataset
from energy_pipeline.transform import transform_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def run_pipeline(source="sample"):
    cfg = load_config()
    raw = PROJECT_ROOT / cfg["paths"]["raw_dir"]
    processed = PROJECT_ROOT / cfg["paths"]["processed_dir"]
    raw.mkdir(parents=True, exist_ok=True)
    processed.mkdir(parents=True, exist_ok=True)
    if source == "sample":
        input_file = create_sample_csv(raw / "sample_energy.csv")
    elif source == "uci":
        input_file = download_uci_dataset(raw, cfg["source"]["uci_zip_url"])
    else:
        raise ValueError("source must be 'sample' or 'uci'")
    rows = transform_file(input_file, processed / cfg["paths"]["cleaned_csv"],
                          processed / cfg["paths"]["cleaned_parquet_dir"])
    log.info("ETL complete: %s valid rows", rows)
    return rows

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["sample", "uci"], default="sample")
    run_pipeline(parser.parse_args().source)
