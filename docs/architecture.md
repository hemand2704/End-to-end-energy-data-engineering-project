# Architecture

```mermaid
flowchart TD
 A[UCI electricity time series] --> B[Python ingestion]
 B --> C[Raw CSV]
 C --> D[PySpark cleaning and validation]
 D --> E[Clean CSV and partitioned Parquet]
 E --> F[dbt and DuckDB]
 F --> G[Daily energy model]
 G --> H[Monthly energy model]
 I[Dagster] -. orchestrates .-> B
 I -. orchestrates .-> D
 J[GitHub Actions] --> K[pytest]
```

The pipeline separates ingestion, transformation and analytics modelling. Parquet is retained
for columnar processing; CSV provides a simple local hand-off to dbt-duckdb. A generated sample
allows a quick smoke test before downloading the full dataset.
