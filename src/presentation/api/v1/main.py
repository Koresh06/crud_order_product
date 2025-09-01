from fastapi import FastAPI

from src.application.containers.modules import MODULES
from src.utils.exceptions import add_exception_handlers
from src.utils.logging import setup_logging
from src.application.containers.container import Container
from src.presentation.api.v1.routers.product import router as product_router
from src.presentation.api.v1.routers.order import router as order_router
from src.presentation.api.middlewares import RateLimitingMiddleware


def create_app() -> FastAPI:

    container = Container()
    container.wire(modules=MODULES)
    
    app = FastAPI(title="CRUD v1")

    app.add_middleware(RateLimitingMiddleware)

    app.include_router(product_router, prefix="/api/v1")
    app.include_router(order_router, prefix="/api/v1")

    add_exception_handlers(app=app)
    setup_logging()

    return app