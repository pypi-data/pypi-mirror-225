from typing import Any, Dict, Optional
from loguru import logger

from pydantic import BaseSettings, RedisDsn, root_validator


class Settings(BaseSettings):
    # Consumer settings
    SONA_CONSUMER_SQS_SETTING: Optional[Dict] = None
    SONA_CONSUMER_KAFKA_SETTING: Optional[Dict] = None
    SONA_CONSUMER_REDIS_URL: Optional[RedisDsn] = None
    SONA_CONSUMER_REDIS_GROUP: Optional[str] = "dwave.anonymous"

    # Producer settings
    SONA_PRODUCER_SQS_SETTING: Optional[Dict] = None
    SONA_PRODUCER_KAFKA_SETTING: Optional[Dict] = None
    SONA_PRODUCER_REDIS_URL: Optional[RedisDsn] = None

    # Storage settings
    SONA_STORAGE_DIR: str = "_tmp"
    SONA_STORAGE_LOCAL_ROOT: str = "_share"

    SONA_STORAGE_SETTING: Dict = None  # TODO: Deprecate in 1.0.0
    SONA_STORAGE_S3_SETTING: Dict = None

    SONA_STORAGE_BUCKET: str = None  # TODO: Deprecate in 1.0.0
    SONA_STORAGE_S3_BUCKET: str = "sona"

    # Inferencer settings
    SONA_WORKER: str = "sona.workers.InferencerWorker"
    SONA_INFERENCER: str = None
    SONA_INFERENCER_TOPIC_PREFIX: str = "dwave.inferencer."

    @root_validator(pre=False)
    def load_settings(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values["SONA_STORAGE_SETTING"]:
            logger.warning("SONA_STORAGE_SETTING will be deprecated in version 1.0.0")
        if values["SONA_STORAGE_BUCKET"]:
            logger.warning("SONA_STORAGE_BUCKET will be deprecated in version 1.0.0")
        values["SONA_STORAGE_S3_SETTING"] = (
            values["SONA_STORAGE_SETTING"] or values["SONA_STORAGE_S3_SETTING"]
        )
        values["SONA_STORAGE_S3_BUCKET"] = (
            values["SONA_STORAGE_BUCKET"] or values["SONA_STORAGE_S3_BUCKET"]
        )
        return values

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
