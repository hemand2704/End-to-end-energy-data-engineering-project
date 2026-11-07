# AWS S3 setup guide

## 1. Create an S3 bucket
Create a globally unique S3 bucket in the AWS region configured in `config/pipeline.yaml` (default: `ap-southeast-2`). Keep Block Public Access enabled. The pipeline only needs private object storage.

## 2. Configure least-privilege access
Use an IAM role or user dedicated to this project. Restrict permissions to the specific bucket and prefix. Typical upload permissions include `s3:PutObject` on `arn:aws:s3:::YOUR_BUCKET/portfolio/energy/*`. Add `s3:ListBucket` only if your workflow needs to list objects. Avoid broad administrator permissions.

## 3. Configure credentials locally
Prefer AWS IAM Identity Center / an AWS profile where available. Alternatively configure environment variables in your shell; never put secrets in source files or commit them.

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="ap-southeast-2"
export AWS_S3_BUCKET="your-bucket-name"
export AWS_S3_PREFIX="portfolio/energy"
```

Do not paste real credentials into GitHub issues, commits, screenshots, or chat.

## 4. Upload
Run:

```bash
python -m cloud_pipeline.pipeline --upload
```

Or materialise the Dagster `cloud_data_pipeline` job. The final `s3_upload` asset uploads the processed CSV if `AWS_S3_BUCKET` is set.

## 5. Optional GitHub Actions deployment
The included workflow is CI only: it runs tests and does not access AWS. For secure automated AWS deployment, configure GitHub Actions OIDC federation to assume a narrowly scoped IAM role. Prefer OIDC over long-lived access keys. Add a separate deployment workflow only after creating and testing the IAM trust policy and role.

## Verification checklist
- [ ] Bucket is private and Block Public Access is enabled
- [ ] IAM permissions are restricted to the required bucket prefix
- [ ] Credentials are provided through a secure credential provider
- [ ] Local upload succeeds
- [ ] Object appears under the expected S3 prefix
- [ ] Dagster asset run reports success
- [ ] CI workflow passes
