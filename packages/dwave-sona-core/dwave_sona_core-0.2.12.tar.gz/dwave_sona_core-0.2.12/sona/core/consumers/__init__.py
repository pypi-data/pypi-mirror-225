from sona.settings import settings

from .base import ConsumerBase
from .kafka import KafkaConsumer
from .redis import RedisConsumer
from .sqs import SQSConsumer

__all__ = ["ConsumerBase", "KafkaConsumer", "RedisConsumer", "SQSConsumer"]


def create_consumer():
    if settings.SONA_CONSUMER_SQS_SETTING:
        return SQSConsumer()
    if settings.SONA_CONSUMER_REDIS_URL:
        return RedisConsumer()
    if settings.SONA_CONSUMER_KAFKA_SETTING:
        return KafkaConsumer()
    raise Exception(
        "Consumer settings not found, please set SONA_CONSUMER_KAFKA_SETTING or SONA_CONSUMER_REDIS_URL"
    )
