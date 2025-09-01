from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Path, status, Depends

from src.application.containers.container import Container
from src.application.use_cases.intarface import UseCaseOneEntity
from src.application.use_cases.intarface import UseCaseMultipleEntities, UseCaseNoReturn, UseCaseOneEntity
from src.domain.dtos.product import ProductId
from src.presentation.api.v2.schemas.requests.product import CreateProductRequest, UpdateProductRequest
from src.presentation.api.v2.schemas.responses.product import ProductResponse, ProductsListResponse


router = APIRouter(
    prefix="/product",
    tags=["Product v2"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый продукт",
)
@inject
async def create_product(
    payload: Annotated[
        CreateProductRequest,
        Body(..., description="Данные для создания продукта"),
    ],
    user_case: Annotated[
        UseCaseOneEntity,
        Depends(Provide[Container.create_product_uc]),
    ],
) -> ProductResponse:
    """
    Создание нового продукта.

    Принимает объект `CreateProductRequest` и возвращает созданный продукт `ProductResponse`.
    """
    product_dto = await user_case.execute(payload.to_dto())
    return ProductResponse.from_dto(dto=product_dto)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить продукт по ID",
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
    Получение существующего продукта по его ID.
    """
    product_dto = await user_case.execute(ProductId(product_id))
    return ProductResponse.from_dto(dto=product_dto)


@router.get(
    "/",
    response_model=ProductsListResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить список всех продуктов",
)
@inject
async def list_products(
    user_case: Annotated[
        UseCaseMultipleEntities,
        Depends(Provide[Container.list_products_uc]),
    ]
) -> ProductsListResponse:
    """
    Получение списка всех продуктов.

    Возвращает массив объектов `ProductResponse`.
    """
    products_dto = await user_case.execute()
    return ProductsListResponse.from_dto_list(products_dto)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить продукт по ID",
)
@inject
async def update_product(
    product_id: Annotated[
        int,
        Path(..., description="Уникальный идентификатор продукта", example=123),
    ],
    payload: Annotated[
        UpdateProductRequest,
        Body(..., description="Данные для обновления продукта"),
    ],
    user_case: Annotated[
        UseCaseOneEntity,
        Depends(Provide[Container.update_product_uc]),
    ],
) -> ProductResponse:
    """
    Обновление существующего продукта по его ID.

    Принимает объект `UpdateProductRequest` и возвращает обновлённый продукт.
    """
    product_dto = await user_case.execute(ProductId(product_id), payload.to_dto())
    return ProductResponse.from_dto(dto=product_dto)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить продукт по ID",
)
@inject
async def delete_product(
    product_id: Annotated[
        int,
        Path(..., description="Уникальный идентификатор продукта", example=123),
    ],
    user_case: Annotated[
        UseCaseNoReturn,
        Depends(Provide[Container.delete_product_uc]),
    ],
) -> None:
    """
    Удаление существующего продукта по его ID.
    """
    await user_case.execute(ProductId(product_id))