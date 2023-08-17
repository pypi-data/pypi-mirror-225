from __future__ import annotations

from pydantic import BaseModel


class MessageBase(BaseModel):
    def mutate(self, **kwargs) -> MessageBase:
        kwargs = {**self.dict(), **kwargs}
        return self.__class__(**kwargs)

    def to_message(self) -> str:
        return self.json()

    class Config:
        allow_mutation = False
