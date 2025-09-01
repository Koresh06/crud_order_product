from src.domain.dtos.product import ProductDTO, ProductId, UpdateProductDTO
from src.infrastructure.database.models.product import Product


class ProductModelMapper:

    @staticmethod
    def to_dto(model: Product) -> ProductDTO:
        return ProductDTO(
            id=ProductId(model.id),
            name=model.name,
            price=model.price,
            category=model.category,
            description=model.description
        )

    @staticmethod
    def from_dto(dto: ProductDTO) -> Product:
        return Product(
            id=dto.id.value,
            name=dto.name,
            price=dto.price,
            category=dto.category,
            description=dto.description
        )

    @staticmethod
    def apply_update(model: Product, update_dto: UpdateProductDTO) -> None:
        if update_dto.name is not None:
            model.name = update_dto.name
        if update_dto.price is not None:
            model.price = update_dto.price
        if update_dto.category is not None:
            model.category = update_dto.category
        if update_dto.description is not None:
            model.description = update_dto.description
