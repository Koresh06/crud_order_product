from datetime import datetime
from pydantic import BaseModel

from src.domain.dtos.order import OrderDTO


class OrderItemData(BaseModel):
    product_id: int
    quantity: int
    price: float
    total: float


class OrderData(BaseModel):
    id: int
    items: list[OrderItemData]
    total_amount: float
    status: str
    currency: str
    created_at: datetime
    updated_at: datetime


class OrderResponse(BaseModel):
    order: OrderData

    @classmethod
    def from_dto(cls, dto: OrderDTO) -> "OrderResponse":
        return cls(
            order=OrderData(
                id=dto.id.value,
                items=[
                    OrderItemData(
                        product_id=item.product_id.value,
                        quantity=item.quantity,
                        price=item.price,
                        total=item.total,
                    )
                    for item in dto.items
                ],
                total_amount=dto.total_amount,
                status=dto.status.name,
                currency=dto.currency.name,
                created_at=dto.created_at,
                updated_at=dto.updated_at,
            )
        )


class OrdersListResponse(BaseModel):
    orders: list[OrderData]
    orders_count: int

    @classmethod
    def from_dto_list(cls, dtos: list[OrderDTO]) -> "OrdersListResponse":
        return cls(
            orders=[OrderResponse.from_dto(dto).order for dto in dtos],
            orders_count=len(dtos),
        )