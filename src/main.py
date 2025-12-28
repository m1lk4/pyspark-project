import logging
import os
from pyspark.sql import SparkSession
from utils.transformations import clean_data, load_to_bq
from utils.data_io import load_raw_csv, save_clean_dataset
from utils.config_loader import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

env = os.getenv("ENV", "dev")


def main():
    spark = SparkSession.builder.appName("us-insurance-etl").getOrCreate()

    config_bucket = spark.conf.get("spark.executorEnv.CONFIG_BUCKET")

    config = load_config(env=env, config_bucket=config_bucket)

    raw_path = config["raw_path"]
    clean_path = config["clean_path"]
    project_id = config["project_id"]
    dataset = config["bq_dataset"]
    table = config["bq_table"]

    try:
        df_raw = load_raw_csv(spark, raw_path)
        df_clean = clean_data(df_raw)
        save_clean_dataset(df_clean, clean_path)
        load_to_bq(
            project_id=project_id,
            dataset=dataset,
            table=table,
            clean_path=clean_path,
        )

        logger.info("Proceso completado exitosamente.")

    except Exception as e:
        logger.exception(f"Ocurrió un error durante el proceso: {e}")
        raise

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
