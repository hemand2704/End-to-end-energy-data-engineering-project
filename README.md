# Energy Consumption Data Engineering Pipeline

Portfolio project demonstrating Python ingestion, PySpark ETL, dbt analytics models, YAML configuration, Dagster orchestration, tests and CI.

**Dataset:** UCI Individual Household Electric Power Consumption. It contains household-level one-minute electricity readings. It is useful for energy time-series engineering practice, but it is not SCADA, GIS, DER or utility-network telemetry.

## Architecture
UCI dataset or generated sample → Python ingestion → raw CSV → PySpark cleaning → cleaned CSV + partitioned Parquet → dbt/DuckDB daily and monthly models. Dagster orchestrates the local ETL job; GitHub Actions runs pytest.

## Quick start
Requires Python 3.10–3.12, Java 11 or 17 (for local PySpark), and Git.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python -m energy_pipeline.pipeline --source sample
```

To download and process the public UCI data:
```bash
python -m energy_pipeline.pipeline --source uci
```
Source: https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption

## dbt
After ETL creates `data/processed/energy_clean.csv`:
```bash
cd dbt
dbt build --profiles-dir .
```
This creates `data/energy_analytics.duckdb` with `daily_energy` and `monthly_energy` models. The dbt models read the cleaned CSV through DuckDB.

## Dagster
From the project root:
```bash
dagster dev -m energy_pipeline.definitions
```
Open the local Dagster UI and materialise `energy_pipeline_job`. Set `ENERGY_SOURCE=uci` before starting Dagster to use the UCI dataset; otherwise it uses the generated sample.

## Tests
```bash
pytest
```

## Databricks deployment pathway
The PySpark transformation is suitable as a starting point for a Databricks job. For a cloud deployment, upload the raw CSV to a Unity Catalog volume or cloud object store, replace local paths with cloud URIs, write the cleaned result to Delta, configure a Databricks job, and adapt dbt to the dbt-databricks adapter. This repository does not claim that a Databricks workspace or cloud deployment has already been provisioned.

## Portfolio evidence
After running the project, add genuine screenshots of (1) successful ETL execution, (2) Parquet output, (3) dbt build, (4) Dagster run and (5) passing tests. Do not claim cloud deployment until you have completed it.

## Structure
- `config/pipeline.yaml` — YAML settings
- `src/energy_pipeline/` — ingestion, PySpark transform, CLI and Dagster definitions
- `dbt/` — dbt project, SQL models and tests
- `tests/` — pytest checks
- `.github/workflows/ci.yml` — GitHub Actions CI
- `docs/architecture.md` — architecture notes
