from src.utils.exceptions import OrderNotFoundError
from src.domain.services.order import OrderServiceInterface
from src.domain.dtos.order import CreateOrderDTO, OrderDTO, OrderId, UpdateOrderDTO
from src.domain.repositories.order_intarface import OrderAbstractRepository


class OrderService(OrderServiceInterface):
    def __init__(self, repository: OrderAbstractRepository):
        self.repository = repository

    async def add(self, order_dto: CreateOrderDTO) -> OrderDTO:
        order = await self.repository.add(order_dto)
        return order

    async def get(self, order_id: OrderId) -> OrderDTO:
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError()
        return order

    async def list(self) -> list[OrderDTO]:
        return await self.repository.list_all()

    async def update(self, order_id: OrderId, update_dto: UpdateOrderDTO) -> OrderDTO:
        existing = await self.repository.get_by_id(order_id)
        if not existing:
            raise OrderNotFoundError()
        updated_order = await self.repository.update(order_id, update_dto)
        return updated_order

    async def delete(self, order_id: OrderId) -> None:
        existing = await self.repository.get_by_id(order_id)
        if not existing:
            raise OrderNotFoundError()
        await self.repository.remove(order_id)
