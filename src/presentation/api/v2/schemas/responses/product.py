from pydantic import BaseModel

from src.domain.dtos.product import ProductDTO


class ProductData(BaseModel):
    id: int
    name: str
    price: float
    category: str
    description: str | None


class ProductResponse(BaseModel):
    product: ProductData

    @classmethod
    def from_dto(cls, dto: ProductDTO) -> "ProductResponse":
        return cls(
            product=ProductData(
                id=dto.id.value,
                name=dto.name,
                price=dto.price,
                category=dto.category.name,
                description=dto.description,
            )
        )


class ProductsListResponse(BaseModel):
    products: list[ProductData]

    @classmethod
    def from_dto_list(cls, dtos: list[ProductDTO]) -> "ProductsListResponse":
        return cls(products=[ProductResponse.from_dto(dto).product for dto in dtos])