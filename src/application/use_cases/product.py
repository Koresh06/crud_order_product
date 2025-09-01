from src.domain.dtos.product import CreateProductDTO, ProductDTO, ProductId
from src.application.use_cases.intarface import UseCaseMultipleEntities, UseCaseOneEntity, UseCaseNoReturn
from src.application.services.product import ProductServiceInterface


class CreateProductUseCase(UseCaseOneEntity[ProductDTO]):
    def __init__(self, product_service: ProductServiceInterface):
        self.product_service = product_service

    async def execute(self, create_dto: CreateProductDTO) -> ProductDTO:
        return await self.product_service.create(create_dto)


class ListProductsUseCase(UseCaseMultipleEntities[ProductDTO]):
    def __init__(self, product_service: ProductServiceInterface):
        self.product_service = product_service

    async def execute(self) -> list[ProductDTO]:
        return await self.product_service.list()


class GetProductUseCase(UseCaseOneEntity[ProductDTO]):
    def __init__(self, product_service: ProductServiceInterface):
        self.product_service = product_service

    async def execute(self, product_id: ProductId) -> ProductDTO | None:
        return await self.product_service.get(product_id)


class UpdateProductUseCase(UseCaseOneEntity[ProductDTO]):
    def __init__(self, product_service: ProductServiceInterface):
        self.product_service = product_service

    async def execute(self, product_id: ProductId, update_dto) -> ProductDTO:
        return await self.product_service.update(product_id, update_dto)


class DeleteProductUseCase(UseCaseNoReturn):
    def __init__(self, product_service: ProductServiceInterface):
        self.product_service = product_service

    async def execute(self, product_id: ProductId) -> None:
        await self.product_service.delete(product_id)