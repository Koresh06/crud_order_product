from datetime import datetime
from pydantic import BaseModel
from typing import List
from src.domain.dtos.order import CreateOrderItemDTO, CreateOrderDTO
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
