from pyspark.sql import SparkSession
from src.config import settings
import logging

logger = logging.getLogger(__name__)


def create_spark_session():
    """Crea una SparkSession según el entorno configurado."""
    if settings.ENV == "local":
        logger.info("Creando SparkSession en LOCAL")
        return (
            SparkSession.builder.master("local[*]")
            .appName("insurance-cleaning-local")
            .getOrCreate()
        )

    else:
        logger.info("Creando SparkSession para DATAPROC")
        return SparkSession.builder.appName("insurance-cleaning-dataproc").getOrCreate()
