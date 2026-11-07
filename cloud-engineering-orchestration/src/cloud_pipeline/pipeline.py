import argparse
import os
from pathlib import Path
from cloud_pipeline.config import PROJECT_ROOT, load_config
from cloud_pipeline.ingestion import create_sample_data, read_input_csv
from cloud_pipeline.transform import validate_and_transform
from cloud_pipeline.storage import upload_file_to_s3

def run_pipeline(input_file=None, upload=False):
    config = load_config()
    input_path = Path(input_file) if input_file else PROJECT_ROOT / config["pipeline"]["input_file"]
    output_path = PROJECT_ROOT / config["pipeline"]["output_file"]

    if not input_path.exists() and input_file is None:
        create_sample_data(input_path)

    raw = read_input_csv(input_path)
    clean = validate_and_transform(raw)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_path, index=False)

    result = {"rows_processed": len(clean), "output_file": str(output_path)}
    if upload:
        result["s3"] = upload_file_to_s3(
            output_path,
            region=config["aws"]["region"]
        )
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the cloud-ready data pipeline")
    parser.add_argument("--input", help="Optional input CSV path")
    parser.add_argument("--upload", action="store_true", help="Upload output to S3")
    args = parser.parse_args()
    print(run_pipeline(args.input, upload=args.upload))
