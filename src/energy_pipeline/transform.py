from pathlib import Path
from pyspark.sql import SparkSession, functions as F, types as T
from energy_pipeline.config import load_config

NUMERIC = ["Global_active_power","Global_reactive_power","Voltage","Global_intensity","Sub_metering_1","Sub_metering_2","Sub_metering_3"]

def transform_file(input_path, output_csv, output_parquet):
    cfg = load_config()
    output_csv, output_parquet = Path(output_csv), Path(output_parquet)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_parquet.parent.mkdir(parents=True, exist_ok=True)
    spark = (SparkSession.builder.appName(cfg["spark"]["app_name"])
             .master(cfg["spark"]["master"])
             .config("spark.sql.shuffle.partitions", str(cfg["spark"]["shuffle_partitions"]))
             .getOrCreate())
    try:
        df = (spark.read.option("header", True).option("sep", ";")
              .option("inferSchema", False).csv(str(input_path)))
        missing = [c for c in cfg["quality"]["required_columns"] if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        df = df.withColumn("event_timestamp", F.to_timestamp(
            F.concat_ws(" ", "Date", "Time"), "d/M/yyyy H:mm:ss"))
        for col in NUMERIC:
            df = df.withColumn(col, F.regexp_replace(F.col(col), ",", ".").cast(T.DoubleType()))
        df = (df.filter(F.col("event_timestamp").isNotNull())
              .drop("Date", "Time").dropna(subset=NUMERIC)
              .filter((F.col("Global_active_power") >= 0) & (F.col("Voltage") >= 0))
              .withColumn("event_date", F.to_date("event_timestamp"))
              .withColumn("year", F.year("event_timestamp"))
              .withColumn("month", F.month("event_timestamp"))
              .withColumn("estimated_energy_wh", F.col("Global_active_power") * 1000.0 / 60.0))
        count = df.count()
        if count == 0:
            raise ValueError("No valid records remain after cleaning")
        tmp = output_csv.parent / (output_csv.stem + "_tmp")
        df.coalesce(1).write.mode("overwrite").option("header", True).csv(str(tmp))
        part = next(tmp.glob("part-*.csv"))
        part.replace(output_csv)
        for item in tmp.iterdir():
            item.unlink()
        tmp.rmdir()
        df.write.mode("overwrite").partitionBy("year", "month").parquet(str(output_parquet))
        return count
    finally:
        spark.stop()
