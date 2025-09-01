from dataclasses import dataclass
from src.domain.dtos.product import ProductId


@dataclass(frozen=True)
class OrderItemDTO:
    product_id: ProductId
    quantity: int
    price: float

    @property
    def total(self) -> float:
        return self.quantity * self.price
    

@dataclass(frozen=True)
class OrderItemResponseDTO:
    product_id: int
    quantity: int
    price: float
    total: float