from abc import ABC, abstractmethod

from src.domain.dtos.product import CreateProductDTO, UpdateProductDTO, ProductDTO, ProductId


class ProductAbstractRepository(ABC):
    @abstractmethod
    async def add(self, product: CreateProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: ProductId) -> ProductDTO | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[ProductDTO]:
        pass

    @abstractmethod
    async def update(self, product_id: ProductId, product_dto: UpdateProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    async def remove(self, product_id: ProductId) -> None:
        pass