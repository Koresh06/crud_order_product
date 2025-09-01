from abc import ABC, abstractmethod

from src.domain.dtos.order import CreateOrderDTO, UpdateOrderDTO, OrderDTO, OrderId


class OrderServiceInterface(ABC):
    @abstractmethod
    async def add(self, order: CreateOrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    async def get(self, order_id: OrderId) -> OrderDTO | None:
        pass

    @abstractmethod
    async def list(self) -> list[OrderDTO]:
        pass

    @abstractmethod
    async def update(self, order_id: OrderId, order_dto: UpdateOrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    async def delete(self, order_id: OrderId) -> None:
        pass