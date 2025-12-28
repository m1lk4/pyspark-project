from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lower
from google.cloud import bigquery
import logging

logger = logging.getLogger(__name__)


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


def load_to_bq(project_id: str, dataset: str, table: str, clean_path: str):
    """
    Carga el DataFrame limpio a una tabla de BigQuery.
    """
    client = bigquery.Client(project=project_id)

    table_name = f"{project_id}.{dataset}.{table}"
    logger.info(f"Cargando datos a BigQuery en la tabla: {table_name}")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET, write_disposition="WRITE_TRUNCATE"
    )

    uri = clean_path + "/*"

    load_job = client.load_table_from_uri(uri, table_name, job_config=job_config)

    load_job.result()

    logger.info(f"Carga a BigQuery completada: {table_name}")
