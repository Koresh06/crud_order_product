from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Path, status, Depends

from src.application.containers.container import Container
from src.application.use_cases.intarface import UseCaseOneEntity
from src.application.use_cases.intarface import UseCaseMultipleEntities, UseCaseOneEntity
from src.domain.dtos.order import OrderId
from src.presentation.api.v1.schemas.requests.order import CreateOrderRequest
from src.presentation.api.v1.schemas.responses.order import OrderResponse, OrdersListResponse


router = APIRouter(
    prefix="/order",
    tags=["Order v1"]
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать заказ",
    responses={
        201: {"description": "Заказ успешно создан"},
        400: {"description": "Неверные данные запроса"},
        422: {"description": "Ошибка валидации"},
    },
)
@inject
async def create_order(
    payload: Annotated[
        CreateOrderRequest,
        Body(..., description="Данные для создания нового заказа"),
    ],
    user_case: Annotated[
        UseCaseOneEntity,
        Depends(Provide[Container.create_order_uc]),
    ],
) -> OrderResponse:
    """
    Создание нового заказа.

    Принимает объект `CreateOrderRequest` с данными заказа и возвращает созданный заказ.
    """
    order_dto = await user_case.execute(payload.to_dto())
    return OrderResponse.from_dto(order_dto)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить заказ по ID",
    responses={
        200: {"description": "Заказ найден"},
        404: {"description": "Заказ не найден"},
    },
)
@inject
async def get_order(
    order_id: Annotated[
        int,
        Path(..., description="Уникальный идентификатор заказа", example=123),
    ],
    user_case: Annotated[
        UseCaseOneEntity,
        Depends(Provide[Container.get_order_uc]),
    ],
) -> OrderResponse:
    """
    Получение информации о заказе по его уникальному идентификатору.
    """
    order_dto = await user_case.execute(OrderId(order_id))
    return OrderResponse.from_dto(order_dto)


@router.get(
    "/",
    response_model=OrdersListResponse,
    status_code=status.HTTP_200_OK,
    summary="Список заказов",
    responses={
        200: {"description": "Список заказов успешно получен"},
    },
)
@inject
async def list_orders(
    user_case: Annotated[
        UseCaseMultipleEntities,
        Depends(Provide[Container.list_order_uc]),
    ],
) -> OrdersListResponse:
    """
    Получение списка всех заказов.

    Возвращает массив объектов `OrderResponse`.
    """
    orders_dto = await user_case.execute()
    return OrdersListResponse.from_dto_list(orders_dto)