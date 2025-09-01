import itertools
from dataclasses import asdict

from src.utils.exceptions import ProductNotFoundError
from src.domain.dtos.product import  CreateProductDTO, ProductDTO, ProductId, UpdateProductDTO
from src.domain.repositories.product_intarface import ProductAbstractRepository

class InMemoryProductRepository(ProductAbstractRepository):
    def __init__(self):
        self._products: dict[int, ProductDTO] = {}
        self._id_counter = itertools.count(1)

    async def add(self, product: CreateProductDTO) -> ProductDTO:
        product_id = ProductId(next(self._id_counter))
        product_dto = ProductDTO(
            id=product_id,
            name=product.name,
            price=product.price,
            category=product.category,
            description=product.description
        )
        self._products[product_id.value] = product_dto
        return product_dto

    async def get_by_id(self, product_id: ProductId) -> ProductDTO | None:
        return self._products.get(product_id.value)

    async def list_all(self) -> list[ProductDTO]:
        return list(self._products.values())

    async def update(self, product_id: ProductId, update_dto: UpdateProductDTO) -> ProductDTO:
        product = self._products.get(product_id.value)
        if not product:
            raise ProductNotFoundError()

        update_data = asdict(update_dto)
        for key, value in update_data.items():
            if value is not None:
                setattr(product, key, value)

        self._products[product_id.value] = product
        return product

    async def remove(self, product_id: ProductId) -> None:
        if product_id.value in self._products:
            del self._products[product_id.value]
        else:
            raise ProductNotFoundError()