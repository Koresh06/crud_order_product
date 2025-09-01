from abc import ABC, abstractmethod

from src.domain.dtos.order import CreateOrderDTO, UpdateOrderDTO, OrderDTO, OrderId
from src.domain.value_objects.order_status import OrderStatus


class OrderAbstractRepository(ABC):
    @abstractmethod
    async def add(self, order: CreateOrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: OrderId) -> OrderDTO | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[OrderDTO]:
        pass

    @abstractmethod
    async def update(self, order_id: OrderId, update_dto: UpdateOrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    async def remove(self, order_id: OrderId) -> None:
        pass

    @abstractmethod
    async def list_by_status(self, status: OrderStatus) -> list[OrderDTO]:
        pass
