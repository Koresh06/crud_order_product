from dataclasses import dataclass

from src.domain.value_objects.product_category import ProductCategory


@dataclass(frozen=True)
class ProductId:
    value: int


@dataclass
class ProductDTO:
    id: ProductId
    name: str
    price: float
    category: ProductCategory = ProductCategory.OTHER
    description: str | None = None

    def change_price(self, new_price: float) -> None:
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price


@dataclass(frozen=True)
class CreateProductDTO:
    name: str
    price: float
    category: ProductCategory = ProductCategory.OTHER
    description: str | None = None


@dataclass(frozen=True)
class UpdateProductDTO:
    name: str | None = None
    price: float | None = None
    category: ProductCategory | None = None
    description: str | None = None


@dataclass(frozen=True)
class ProductResponseDTO:
    id: int
    name: str
    price: float
    category: ProductCategory
    description: str | None = None