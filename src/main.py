import logging
from src.cleaning import clean_data, load_raw_csv, save_clean_dataset
from utils.session import create_spark_session
from src.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    logger.info(f"Iniciando proceso en entorno: {settings.ENV}")
    logger.info(f"Usando bucket: {settings.BUCKET_NAME}")

    spark = create_spark_session()

    try:
        df_raw = load_raw_csv(spark, settings.input_file)
        df_clean = clean_data(df_raw)
        save_clean_dataset(df_clean, settings.clean_output_file)

        logger.info("Proceso completado exitosamente.")

    except Exception as e:
        logger.exception(f"Ocurrió un error durante el proceso: {e}")
        raise

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
