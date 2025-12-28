import yaml
from google.cloud import storage
import logging

logger = logging.getLogger(__name__)


def load_config(env: str = None, config_bucket: str = None) -> dict:

    if not config_bucket:
        raise ValueError(f"CONFIG_BUCKET no está definido en el entorno {env}")

    logger.info(
        f"Iniciando carga de configuración para el entorno: {env} desde el bucket: {config_bucket}"
    )

    name, prefix = config_bucket.split("/", 1)

    logger.info(f"Bucket: {name}, Prefijo: {prefix}")

    client = storage.Client()
    bucket = client.bucket(name)
    blob = bucket.blob(f"{prefix}{env}.yaml")

    config = yaml.safe_load(blob.download_as_string())

    logger.info(f"Configuración cargada exitosamente para el entorno: {env}")
    return config
