from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lower
import logging

logger = logging.getLogger(__name__)


def load_raw_csv(spark, input_path: str) -> DataFrame:
    logger.info(f"Cargando CSV desde: {input_path}")
    return spark.read.option("header", True).option("inferSchema", True).csv(input_path)


def clean_data(df: DataFrame) -> DataFrame:
    """
    Realiza limpieza y casteo de columnas del dataset de seguros.
    - Convierte tipos correctos
    - Normaliza cadenas de texto a minúsculas
    """
    logger.info("Iniciando limpieza del dataset...")

    df_clean = (
        df.withColumn("age", col("age").cast("int"))
        .withColumn("bmi", col("bmi").cast("float"))
        .withColumn("children", col("children").cast("int"))
        .withColumn("charges", col("charges").cast("float"))
        .withColumn("sex", lower(col("sex")))
        .withColumn("smoker", lower(col("smoker")))
        .withColumn("region", lower(col("region")))
    )
    return df_clean


def save_clean_dataset(df: DataFrame, output_path: str):
    logger.info(f"Guardando dataset limpio en: {output_path}")
    (df.write.mode("overwrite").parquet(output_path))
