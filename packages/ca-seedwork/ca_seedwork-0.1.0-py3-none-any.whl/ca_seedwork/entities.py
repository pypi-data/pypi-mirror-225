import uuid
from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class Entity(metaclass=ABCMeta):
    id: uuid.UUID

    @staticmethod
    def next_id() -> uuid.UUID:
        return uuid.uuid4()
