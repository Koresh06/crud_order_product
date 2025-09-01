from pydantic import BaseModel, Field
from src.domain.dtos.product import CreateProductDTO, UpdateProductDTO
from src.domain.value_objects.product_category import ProductCategory

class CreateProductData(BaseModel):
    name: str
    price: float
    category: ProductCategory
    description: str | None = None


class UpdateProductData(BaseModel):
    name: str | None = Field(None)
    price: float | None = Field(None)
    category: ProductCategory | None = Field(None)
    description: str | None = Field(None)


class CreateProductRequest(BaseModel):
    product: CreateProductData

    def to_dto(self) -> CreateProductDTO:
        return CreateProductDTO(
            name=self.product.name,
            price=self.product.price,
            category=self.product.category,
            description=self.product.description
        )
    
class UpdateProductRequest(BaseModel):
    product: UpdateProductData

    def to_dto(self) -> UpdateProductDTO:
        return UpdateProductDTO(
            name=self.product.name,
            price=self.product.price,
            category=self.product.category,
            description=self.product.description
        )