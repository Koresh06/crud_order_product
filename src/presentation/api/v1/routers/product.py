from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Path, status, Depends

from src.application.containers.container import Container
from src.application.use_cases.intarface import UseCaseOneEntity
from src.application.use_cases.intarface import UseCaseMultipleEntities, UseCaseOneEntity
from src.domain.dtos.product import ProductId
from src.presentation.api.v1.schemas.requests.product import CreateProductRequest
from src.presentation.api.v1.schemas.responses.product import ProductResponse, ProductsListResponse


router = APIRouter(
    prefix="/product",
    tags=["Product v1"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать продукт",
    responses={
        201: {"description": "Продукт успешно создан"},
        400: {"description": "Неверные данные запроса"},
        422: {"description": "Ошибка валидации"},
    },
)
@inject
async def create_product(
    payload: Annotated[
        CreateProductRequest,
        Body(..., description="Данные для создания нового продукта"),
    ],
    user_case: Annotated[
        UseCaseOneEntity,
        Depends(Provide[Container.create_product_uc]),
    ],
) -> ProductResponse:
    """
    Создание нового продукта.

    Принимает объект `CreateProductRequest` с данными продукта и возвращает созданный продукт.
    """
    product_dto = await user_case.execute(payload.to_dto())
    return ProductResponse.from_dto(dto=product_dto)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить продукт по ID",
    responses={
        200: {"description": "Продукт найден"},
        404: {"description": "Продукт не найден"},
    },
)
@inject
async def get_product(
    product_id: Annotated[
        int,
        Path(..., description="Уникальный идентификатор продукта", example=123),
    ],
    user_case: Annotated[
        UseCaseOneEntity,
        Depends(Provide[Container.get_product_uc]),
    ],
) -> ProductResponse:
    """
    Получение информации о продукте по его уникальному идентификатору.
    """
    product_dto = await user_case.execute(ProductId(product_id))
    return ProductResponse.from_dto(dto=product_dto)


@router.get(
    "/",
    response_model=ProductsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Список продуктов",
    responses={
        200: {"description": "Список продуктов успешно получен"},
    },
)
@inject
async def list_products(
    user_case: Annotated[
        UseCaseMultipleEntities,
        Depends(Provide[Container.list_products_uc]),
    ],
) -> ProductsListResponse:
    """
    Получение списка всех продуктов.

    Возвращает массив объектов `ProductResponse`.
    """
    products_dto = await user_case.execute()
    return ProductsListResponse.from_dto_list(products_dto)