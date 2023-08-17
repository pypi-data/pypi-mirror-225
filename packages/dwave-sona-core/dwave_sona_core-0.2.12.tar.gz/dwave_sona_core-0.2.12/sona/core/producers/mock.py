from loguru import logger

from .base import ProducerBase


class MockProducer(ProducerBase):
    def emit(self, topic, message) -> None:
        logger.info(f"emit [{topic}] {message}")
