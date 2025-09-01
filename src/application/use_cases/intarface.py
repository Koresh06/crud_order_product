from typing import Any, Iterable, TypeVar, Generic, Optional
from abc import ABC, abstractmethod


Entity = TypeVar("Entity")


class GenericUseCase(ABC, Generic[Entity]):

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Entity:
        pass


class UseCaseNoReturn(ABC):

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> None:
        pass


class UseCaseOneEntity(GenericUseCase[Optional[Entity]], ABC):

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Optional[Entity]:
        pass


class UseCaseMultipleEntities(GenericUseCase[Iterable[Entity]], ABC):

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Iterable[Entity]:
        pass