from abc import ABC, abstractmethod

from src.domain.dtos.product import CreateProductDTO, UpdateProductDTO, ProductDTO, ProductId


class ProductServiceInterface(ABC):
    @abstractmethod
    async def create(self, product: CreateProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    async def get(self, product_id: ProductId) -> ProductDTO | None:
        pass

    @abstractmethod
    async def list(self) -> list[ProductDTO]:
        pass

    @abstractmethod
    async def update(self, product_id: ProductId, product_dto: UpdateProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    async def delete(self, product_id: ProductId) -> None:
        pass