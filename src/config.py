import os
import logging

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Error para configuración faltante o inválida."""

    pass


def get_env_variable(name: str, default: str = None, required: bool = False):
    """
    Obtiene una variable de entorno.
    - Si required=True y no existe → lanza error.
    - Si default está presente → usa valor por defecto.
    """
    value = os.getenv(name, default)

    if required and value is None:
        raise ConfigError(
            f"La variable de entorno {name} es obligatoria y no fue encontrada."
        )

    logger.debug(f"Variable cargada: {name} = {value}")
    return value


class Settings:
    """Carga toda la configuración de entorno del proyecto."""

    # Entorno
    ENV = get_env_variable("ENV", default="local")  # local, dev, staging, prod

    # Buckets solo para no-local
    BUCKET_NAME = get_env_variable("BUCKET_NAME", "")

    # Rutas dentro del bucket
    RAW_PATH = get_env_variable("RAW_PATH", default="raw/")
    CLEAN_PATH = get_env_variable("CLEAN_PATH", default="clean/")
    OUTPUT_PATH = get_env_variable("OUTPUT_PATH", default="output/")

    RAW_FILENAME = get_env_variable("RAW_FILENAME", required=True)
    CLEAN_FILENAME = get_env_variable("CLEAN_FILENAME", required=True)
    OUTPUT_FILENAME = get_env_variable("OUTPUT_FILENAME", required=True)

    # BigQuery
    BQ_PROJECT = get_env_variable("BQ_PROJECT", default="practicas-cubifort")
    BQ_DATASET = get_env_variable("BQ_DATASET", default="spark_insurance")
    BQ_TABLE = get_env_variable("BQ_TABLE", default="insurance_clean")

    @property
    def input_file(self):
        """
        Si es local, carga desde disco local.
        Si no es local, carga desde GCS.
        """
        if self.ENV == "local":
            return f"./data/{self.RAW_FILENAME}"
        return f"gs://{self.BUCKET_NAME}/{self.RAW_PATH}{self.RAW_FILENAME}"

    @property
    def clean_output_file(self):
        if self.ENV == "local":
            return f"./data/{self.CLEAN_FILENAME}"
        return f"gs://{self.BUCKET_NAME}/{self.CLEAN_PATH}{self.CLEAN_FILENAME}"

    @property
    def output_file(self):
        if self.ENV == "local":
            return f"./data/{self.OUTPUT_FILENAME}"
        return f"gs://{self.BUCKET_NAME}/{self.OUTPUT_PATH}{self.OUTPUT_FILENAME}"


# Instancia global
settings = Settings()
