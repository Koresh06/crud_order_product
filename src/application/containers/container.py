from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.application.use_cases.order import CreateOrderUseCase, DeleteOrderUseCase, GetOrderUseCase, ListOrdersUseCase, UpdateOrderUseCase
from src.application.use_cases.product import CreateProductUseCase, DeleteProductUseCase, GetProductUseCase, ListProductsUseCase, UpdateProductUseCase
from src.utils.config import settings
from src.infrastructure.database.connect.sqlite import SQLiteDatabaseHelper
from src.infrastructure.repositories.product.in_memory import InMemoryProductRepository
from src.infrastructure.repositories.product.sqlalchemy import SQLAlchemyProductRepository
from src.infrastructure.repositories.order.in_memory import InMemoryOrderRepository
from src.infrastructure.repositories.order.sqlalchemy import SQLAlchemyOrderRepository
from src.application.services.product import ProductService
from src.application.services.order import OrderService
from src.infrastructure.mappers.order_mapper import OrderModelMapper
from src.infrastructure.mappers.product_mapper import ProductModelMapper


def get_sqlite_sessionmaker(helper: SQLiteDatabaseHelper) -> async_sessionmaker[AsyncSession]:
    return helper.get_sessionmaker()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    db_type = providers.Object(settings.db.type)

    sqlite_helper = providers.Singleton(SQLiteDatabaseHelper)

    sqlite_sessionmaker = providers.Callable(
        get_sqlite_sessionmaker,
        sqlite_helper,
    )

    # --- Repositories ---
    product_repo = providers.Selector(
        db_type,
        memory=providers.Singleton(InMemoryProductRepository),
        sqlite=providers.Factory(
            SQLAlchemyProductRepository,
            session_factory=sqlite_sessionmaker,
            product_mapper=ProductModelMapper,
        ),
    )
    order_repo = providers.Selector(
        db_type,
        memory=providers.Singleton(InMemoryOrderRepository),
        sqlite=providers.Factory(
            SQLAlchemyOrderRepository,
            session_factory=sqlite_sessionmaker,
            order_mapper=OrderModelMapper,
        ),
    )

    # --- Services ---
    product_service = providers.Singleton(
        ProductService,
        repository=product_repo,
    )
    order_service = providers.Singleton(
        OrderService,
        repository=order_repo,
    )

    # --- Product use cases ---
    create_product_uc = providers.Factory(
        CreateProductUseCase,
        product_service=product_service,
    )
    list_products_uc = providers.Factory(
        ListProductsUseCase,
        product_service=product_service,
    )
    get_product_uc = providers.Factory(
        GetProductUseCase,
        product_service=product_service,
    )
    update_product_uc = providers.Factory(
        UpdateProductUseCase,
        product_service=product_service,
    )
    delete_product_uc = providers.Factory(
        DeleteProductUseCase,
        product_service=product_service,
    )

    # --- Order use cases ---
    create_order_uc = providers.Factory(
        CreateOrderUseCase,
        order_service=order_service,
    )
    list_order_uc = providers.Factory(
        ListOrdersUseCase,
        order_service=order_service,
    )
    get_order_uc = providers.Factory(
        GetOrderUseCase,
        order_service=order_service,
    )
    update_order_uc = providers.Factory(
        UpdateOrderUseCase,
        order_service=order_service,
    )
    delete_order_uc = providers.Factory(
        DeleteOrderUseCase,
        order_service=order_service,
    )


container = Container()