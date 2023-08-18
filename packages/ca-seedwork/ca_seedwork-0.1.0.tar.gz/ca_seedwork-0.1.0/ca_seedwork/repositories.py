import uuid
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from .entities import Entity

TEntity = TypeVar("TEntity", bound=Entity)


class IRepository(Generic[TEntity], metaclass=ABCMeta):
    @abstractmethod
    def get_by_id(self, entity_id: uuid.UUID) -> TEntity | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: TEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_by_id(self, entity_id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def next_id(self) -> uuid.UUID:
        raise NotImplementedError
