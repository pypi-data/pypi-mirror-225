from __future__ import annotations

import abc
from typing import Dict, List

from sona.core.messages import Context, File, Result
from sona.core.utils.cls_utils import import_class
from sona.settings import settings

TOPIC_PREFIX = settings.SONA_INFERENCER_TOPIC_PREFIX


class InferencerBase:
    inferencer = NotImplemented

    def on_load(self) -> None:
        return

    def context_example(self) -> Context:
        return None

    @classmethod
    def get_topic(cls):
        return f"{TOPIC_PREFIX}{cls.inferencer}"

    @classmethod
    def load_class(cls, import_str):
        inferencer_cls = import_class(import_str)
        if inferencer_cls not in cls.__subclasses__():
            raise Exception(f"Unknown inferencer class: {import_str}")
        return inferencer_cls

    @abc.abstractmethod
    def inference(self, params: Dict, files: List[File]) -> Result:
        return NotImplemented
