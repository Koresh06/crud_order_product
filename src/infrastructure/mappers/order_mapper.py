from datetime import datetime

from src.domain.dtos.order import OrderDTO, OrderId, UpdateOrderDTO
from src.domain.dtos.order_item import OrderItemDTO
from src.domain.dtos.product import ProductId
from src.infrastructure.database.models.order import Order
from src.infrastructure.database.models.order_item import OrderItem

class OrderModelMapper:

    @staticmethod
    def to_dto(model: Order) -> OrderDTO:
        return OrderDTO(
            id=OrderId(model.id),
            items=[
                OrderItemDTO(
                    product_id=ProductId(item.product_id),
                    quantity=item.quantity,
                    price=item.price
                ) for item in model.items
            ],
            status=model.status,
            currency=model.currency,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def from_dto(dto: OrderDTO) -> Order:
        return Order(
            id=dto.id.value,
            items=[
                OrderItem(
                    product_id=item.product_id.value,
                    quantity=item.quantity,
                    price=item.price
                ) for item in dto.items
            ],
            status=dto.status,
            currency=dto.currency,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
    
    @staticmethod
    def apply_update(model: Order, update_dto: UpdateOrderDTO) -> None:
        if update_dto.status is not None:
            model.status = update_dto.status
        if update_dto.currency is not None:
            model.currency = update_dto.currency
        
        model.updated_at = datetime.now()
