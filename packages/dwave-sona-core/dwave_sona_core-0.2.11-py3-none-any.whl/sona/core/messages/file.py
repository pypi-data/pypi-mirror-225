from typing import Dict

from .base import MessageBase


class File(MessageBase):
    label: str
    path: str
    metadata: Dict = {}
