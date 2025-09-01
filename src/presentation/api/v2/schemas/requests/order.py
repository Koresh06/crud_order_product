from datetime import datetime
from pydantic import BaseModel
from typing import List
from src.domain.dtos.order import CreateOrderItemDTO, OrderDTO, OrderStatus, CreateOrderDTO, UpdateOrderDTO
from src.domain.value_objects.currency import Currency


class CreateOrderItemData(BaseModel):
    product_id: int
    quantity: int

    def to_dto(self) -> CreateOrderItemDTO: 
        return CreateOrderItemDTO(
            product_id=self.product_id,
            quantity=self.quantity,
        )


class CreateOrderRequest(BaseModel):
    items: List[CreateOrderItemData]
    currency: Currency

    def to_dto(self) -> CreateOrderDTO:
        return CreateOrderDTO(
            items=[item.to_dto() for item in self.items],
            currency=Currency[self.currency.upper()]
        )



class UpdateOrderRequest(BaseModel):
    status: OrderStatus | None = None
    currency: Currency | None = None

    def to_dto(self) -> UpdateOrderDTO:
        return UpdateOrderDTO(
            status=self.status,
            currency=Currency[self.currency.upper()] if self.currency else None
        )


class OrderItemResponseData(BaseModel):
    product_id: int
    quantity: int
    price: float
    total: float


class OrderResponseData(BaseModel):
    id: int
    items: List[OrderItemResponseData]
    total_amount: float
    status: OrderStatus
    currency: Currency
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: OrderDTO) -> "OrderResponseData":
        return cls(
            id=dto.id.value,
            items=[
                OrderItemResponseData(
                    product_id=item.product_id.value,
                    quantity=item.quantity,
                    price=item.price,
                    total=item.total
                )
                for item in dto.items
            ],
            total_amount=dto.total_amount,
            status=dto.status,
            currency=dto.currency,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )