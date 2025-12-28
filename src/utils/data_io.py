import logging
from pyspark.sql import DataFrame

logger = logging.getLogger(__name__)


def load_raw_csv(spark, input_path: str) -> DataFrame:
    logger.info(f"Cargando CSV desde: {input_path}")
    return spark.read.option("header", True).option("inferSchema", True).csv(input_path)


def save_clean_dataset(df: DataFrame, output_path: str):
    logger.info(f"Guardando dataset limpio en: {output_path}")
    (df.write.mode("overwrite").partitionBy("smoker").parquet(output_path))
