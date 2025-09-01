from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.mapper import IModelMapper
from src.utils.exceptions import ProductNotFoundError
from src.domain.dtos.product import CreateProductDTO, ProductDTO, ProductId, UpdateProductDTO
from src.domain.repositories.product_intarface import ProductAbstractRepository
from src.infrastructure.database.models.product import Product


class SQLAlchemyProductRepository(ProductAbstractRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], product_mapper: IModelMapper[Product, ProductDTO]):
        self._session_factory = session_factory
        self._product_mapper = product_mapper

    async def add(self, product: CreateProductDTO) -> ProductDTO:
        async with self._session_factory() as session:
            product_model = Product(
                name=product.name,
                price=product.price,
                category=product.category,
                description=product.description
            )
            session.add(product_model)
            await session.commit()
            await session.refresh(product_model)
            return self._product_mapper.to_dto(product_model)

    async def get_by_id(self, product_id: ProductId) -> ProductDTO | None:
        async with self._session_factory() as session:
            model = await session.get(Product, product_id.value)
            if not model:
                return None
            return self._product_mapper.to_dto(model)

    async def list_all(self) -> list[ProductDTO]:
        async with self._session_factory() as session:
            result = await session.execute(select(Product))
            models = result.scalars().all()
            return [self._product_mapper.to_dto(m) for m in models]

    async def update(self, product_id: ProductId, update_dto: UpdateProductDTO) -> ProductDTO:
        async with self._session_factory() as session:
            model = await session.get(Product, product_id.value)
            if not model:
                raise ProductNotFoundError()
            self._product_mapper.apply_update(model, update_dto)
            await session.commit()
            await session.refresh(model)
            return self._product_mapper.to_dto(model)

    async def remove(self, product_id: ProductId) -> None:
        async with self._session_factory() as session:
            model = await session.get(Product, product_id.value)
            if not model:
                raise ProductNotFoundError()
            await session.delete(model)
            await session.commit()
