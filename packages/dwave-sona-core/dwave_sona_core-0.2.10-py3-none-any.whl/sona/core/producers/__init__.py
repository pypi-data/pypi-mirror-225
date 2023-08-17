from sona.settings import settings

from .base import ProducerBase
from .kafka import KafkaProducer
from .mock import MockProducer
from .redis import RedisProducer
from .sqs import SQSProducer

__all__ = [
    "ProducerBase",
    "KafkaProducer",
    "RedisProducer",
    "SQSProducer",
    "MockProducer",
]


def create_producer():
    if settings.SONA_PRODUCER_SQS_SETTING:
        return SQSProducer()
    if settings.SONA_PRODUCER_REDIS_URL:
        return RedisProducer()
    if settings.SONA_PRODUCER_KAFKA_SETTING:
        return KafkaProducer()
    raise Exception(
        "Producer settings not found, please set SONA_PRODUCER_KAFKA_SETTING or SONA_PRODUCER_REDIS_URL"
    )
