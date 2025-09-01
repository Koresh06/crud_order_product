from src.utils.exceptions import ProductNotFoundError
from src.domain.services.product import ProductServiceInterface
from src.domain.dtos.product import CreateProductDTO, ProductDTO, ProductId, UpdateProductDTO
from src.domain.repositories.product_intarface import ProductAbstractRepository


class ProductService(ProductServiceInterface):
    def __init__(self, repository: ProductAbstractRepository):
        self.repository = repository

    async def create(self, product_dto: CreateProductDTO) -> ProductDTO:
        product = await self.repository.add(product_dto)
        return product

    async def get(self, product_id: ProductId) -> ProductDTO:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError()
        return product

    async def list(self) -> list[ProductDTO]:
        return await self.repository.list_all()

    async def update(self, product_id: ProductId, update_dto: UpdateProductDTO) -> ProductDTO:
        existing = await self.repository.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError()
        updated_product = await self.repository.update(product_id, update_dto)
        return updated_product

    async def delete(self, product_id: ProductId) -> None:
        existing = await self.repository.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError()
        await self.repository.remove(product_id)