from __future__ import annotations

import abc

from loguru import logger

from sona.core.consumers import ConsumerBase
from sona.core.messages import Context
from sona.core.producers import ProducerBase
from sona.core.storages.base import ShareStorageBase
from sona.core.utils.cls_utils import import_class
from sona.settings import settings

TOPIC_PREFIX = settings.SONA_INFERENCER_TOPIC_PREFIX


class WorkerBase:
    name: str = None
    topic: str = "dummy"

    def set_consumer(self, consumer: ConsumerBase):
        self.consumer = consumer

    def set_producer(self, producer: ProducerBase):
        self.producer = producer

    def set_storage(self, storage: ShareStorageBase):
        self.storage = storage

    async def start(self):
        await self.on_load()
        self.topic = self.get_topic()
        logger.info(f"Susbcribe on {self.topic}({self.consumer.__class__.__name__})")
        self.consumer.subscribe(self.topic)
        async for message in self.consumer.consume():
            try:
                self.storage = self.storage.create_storage()
                context = Context.parse_raw(message)
                await self.on_context(context)
            except Exception as e:
                logger.warning(f"[{self.topic}] error: {e}, msg: {message}")
            finally:
                self.storage.clean()

    async def test(self, context: Context):
        await self.on_load()
        await self.on_context(context)

    @classmethod
    def get_topic(cls) -> str:
        return f"{TOPIC_PREFIX}{cls.name}" if cls.name else cls.topic

    @classmethod
    def load_class(cls, import_str):
        worker_cls = import_class(import_str)
        if worker_cls not in cls.__subclasses__():
            raise Exception(f"Unknown worker class: {import_str}")
        return worker_cls

    # Callbacks
    @abc.abstractmethod
    async def on_load(self) -> None:
        return NotImplemented

    @abc.abstractmethod
    async def on_context(self, message: Context) -> Context:
        return NotImplemented

    def context_example(self) -> Context:
        return None
