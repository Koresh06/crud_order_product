import itertools
from datetime import datetime

from src.utils.exceptions import OrderNotFoundError
from src.domain.dtos.order import CreateOrderDTO, UpdateOrderDTO, OrderDTO, OrderId
from src.domain.dtos.order_item import OrderItemDTO
from src.domain.dtos.product import ProductId
from src.domain.repositories.order_intarface import OrderAbstractRepository
from src.domain.value_objects.order_status import OrderStatus


class InMemoryOrderRepository(OrderAbstractRepository):
    def __init__(self):
        self._orders: dict[int, OrderDTO] = {}
        self._id_counter = itertools.count(1)

    async def add(self, order: CreateOrderDTO) -> OrderDTO:
        order_id = OrderId(next(self._id_counter))
        order_dto = OrderDTO(
            id=order_id,
            items=[
                OrderItemDTO(
                    product_id=ProductId(item.product_id),
                    quantity=item.quantity,
                    price=item.price
                )
                for item in order.items
            ],
            status=OrderStatus.PENDING,
            currency=order.currency,
        )
        self._orders[order_id.value] = order_dto
        return order_dto

    async def get_by_id(self, order_id: OrderId) -> OrderDTO | None:
        return self._orders.get(order_id.value)

    async def list_all(self) -> list[OrderDTO]:
        return list(self._orders.values())

    async def update(self, order_id: OrderId, update_dto: UpdateOrderDTO) -> OrderDTO:
        order = self._orders.get(order_id.value)
        if not order:
            raise OrderNotFoundError()
    
        if update_dto.status is not None:
            order.change_status(update_dto.status)
    
        if update_dto.currency is not None:
            setattr(order, "currency", update_dto.currency)
            order.updated_at = datetime.now()
    
        self._orders[order_id.value] = order
        return order


    async def remove(self, order_id: OrderId) -> None:
        if order_id.value in self._orders:
            del self._orders[order_id.value]
        else:
            raise OrderNotFoundError()

    async def list_by_status(self, status: OrderStatus) -> list[OrderDTO]:
        return [order for order in self._orders.values() if order.status == status]
