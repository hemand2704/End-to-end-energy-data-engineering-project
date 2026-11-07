import os
from pathlib import Path
import boto3

def upload_file_to_s3(local_path, bucket=None, key=None, region="ap-southeast-2", s3_client=None):
    """Upload a local file to S3. Credentials are resolved by the standard boto3 credential chain."""
    bucket = bucket or os.getenv("AWS_S3_BUCKET")
    if not bucket:
        return {"uploaded": False, "reason": "AWS_S3_BUCKET is not configured"}

    prefix = os.getenv("AWS_S3_PREFIX", "portfolio/energy").strip("/")
    key = key or f"{prefix}/{Path(local_path).name}"
    client = s3_client or boto3.client("s3", region_name=region)
    client.upload_file(str(local_path), bucket, key)
    return {"uploaded": True, "bucket": bucket, "key": key}
