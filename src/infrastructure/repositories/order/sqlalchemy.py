from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.database.models.product import Product
from src.utils.exceptions import OrderNotFoundError, ProductNotFoundError
from src.domain.dtos.order import CreateOrderDTO, OrderDTO, OrderId, UpdateOrderDTO
from src.domain.repositories.order_intarface import OrderAbstractRepository
from src.domain.value_objects.order_status import OrderStatus
from src.infrastructure.database.models.order import Order
from src.infrastructure.database.models.order_item import OrderItem
from src.domain.mapper import IModelMapper


class SQLAlchemyOrderRepository(OrderAbstractRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], order_mapper: IModelMapper[Order, OrderDTO]):
        self._session_factory = session_factory
        self._order_mapper = order_mapper

    async def add(self, order: CreateOrderDTO) -> OrderDTO:
        async with self._session_factory() as session:
            order_model = Order(currency=order.currency, status=OrderStatus.PENDING)
            session.add(order_model)
            await session.flush()

            for item in order.items:
                product = await session.get(Product, item.product_id)
                if not product:
                    raise ProductNotFoundError()

                session.add(OrderItem(
                    order_id=order_model.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    price=product.price,
                ))

            await session.commit()

            result = await session.execute(
                select(Order).options(selectinload(Order.items)).where(Order.id == order_model.id)
            )
            order_model = result.scalar_one()

            return self._order_mapper.to_dto(order_model)

    async def get_by_id(self, order_id: OrderId) -> OrderDTO | None:
        async with self._session_factory() as session:
            order_model = await session.get(Order, order_id.value)
            if not order_model:
                return None
            return self._order_mapper.to_dto(order_model)

    async def list_all(self) -> list[OrderDTO]:
        async with self._session_factory() as session:
            result = await session.scalars(select(Order))
            models = result.all()
            return [self._order_mapper.to_dto(o) for o in models]

    async def update(self, order_id: OrderId, update_dto: UpdateOrderDTO) -> OrderDTO:
        async with self._session_factory() as session:
            order_model = await session.get(Order, order_id.value)
            if not order_model:
                raise OrderNotFoundError()

            self._order_mapper.apply_update(order_model, update_dto)

            await session.commit()
            await session.refresh(order_model)
            return self._order_mapper.to_dto(order_model)

    async def remove(self, order_id: OrderId) -> None:
        async with self._session_factory() as session:
            order_model = await session.get(Order, order_id.value)
            if not order_model:
                raise OrderNotFoundError()
            await session.delete(order_model)
            await session.commit()

    async def list_by_status(self, status: OrderStatus) -> list[OrderDTO]:
        async with self._session_factory() as session:
            result = await session.scalars(select(Order).where(Order.status == status))
            models = result.all()
            return [self._order_mapper.to_dto(o) for o in models]
