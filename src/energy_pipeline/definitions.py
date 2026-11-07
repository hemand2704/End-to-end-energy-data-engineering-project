import os
from dagster import Definitions, job, op
from energy_pipeline.pipeline import run_pipeline

@op
def run_energy_etl():
    return run_pipeline(os.getenv("ENERGY_SOURCE", "sample"))

@job
def energy_pipeline_job():
    run_energy_etl()

defs = Definitions(jobs=[energy_pipeline_job])
