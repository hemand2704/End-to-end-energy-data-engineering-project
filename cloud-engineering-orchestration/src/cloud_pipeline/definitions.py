import os
from dagster import Definitions, EnvVar, asset, define_asset_job

from cloud_pipeline.config import PROJECT_ROOT, load_config
from cloud_pipeline.ingestion import create_sample_data, read_input_csv
from cloud_pipeline.transform import validate_and_transform
from cloud_pipeline.storage import upload_file_to_s3

@asset
def source_data():
    cfg = load_config()
    path = PROJECT_ROOT / cfg["pipeline"]["input_file"]
    if not path.exists():
        create_sample_data(path)
    return str(path)

@asset
def processed_data(source_data):
    cfg = load_config()
    output = PROJECT_ROOT / cfg["pipeline"]["output_file"]
    output.parent.mkdir(parents=True, exist_ok=True)
    clean = validate_and_transform(read_input_csv(source_data))
    clean.to_csv(output, index=False)
    return str(output)

@asset
def s3_upload(processed_data):
    cfg = load_config()
    return upload_file_to_s3(
        processed_data,
        region=cfg["aws"]["region"]
    )

cloud_data_pipeline = define_asset_job("cloud_data_pipeline")
defs = Definitions(
    assets=[source_data, processed_data, s3_upload],
    jobs=[cloud_data_pipeline],
)
