from dataclasses import dataclass, field
from datetime import datetime

from src.domain.dtos.order_item import OrderItemDTO, OrderItemResponseDTO
from src.domain.value_objects.currency import Currency
from src.domain.value_objects.order_status import OrderStatus

from dataclasses import dataclass, field
from datetime import datetime



@dataclass(frozen=True)
class OrderId:
    value: int


@dataclass
class OrderDTO:
    id: OrderId
    items: list[OrderItemDTO] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    currency: Currency = Currency.USD
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def total_amount(self) -> float:
        return sum(item.total for item in self.items)

    def add_item(self, item: OrderItemDTO) -> None:
        self.items.append(item)
        self.updated_at = datetime.now()

    def change_status(self, new_status: OrderStatus) -> None:
        self.status = new_status
        self.updated_at = datetime.now()


@dataclass(frozen=True)
class CreateOrderItemDTO:
    product_id: int
    quantity: int


@dataclass(frozen=True)
class CreateOrderDTO:
    items: list[CreateOrderItemDTO]
    currency: Currency = Currency.USD


@dataclass(frozen=True)
class UpdateOrderDTO:
    status: OrderStatus | None = None
    currency: Currency | None = None


@dataclass(frozen=True)
class OrderResponseDTO:
    id: int
    items: list[OrderItemResponseDTO]
    total_amount: float
    status: OrderStatus
    currency: Currency
    created_at: datetime
    updated_at: datetime