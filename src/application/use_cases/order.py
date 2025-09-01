from src.domain.dtos.order import CreateOrderDTO, OrderDTO, OrderId, UpdateOrderDTO
from src.application.use_cases.intarface import UseCaseMultipleEntities, UseCaseOneEntity, UseCaseNoReturn
from src.domain.services.order import OrderServiceInterface


class CreateOrderUseCase(UseCaseOneEntity[OrderDTO]):
    def __init__(self, order_service: OrderServiceInterface):
        self.order_service = order_service

    async def execute(self, create_dto: CreateOrderDTO) -> OrderDTO:
        return await self.order_service.add(create_dto)


class ListOrdersUseCase(UseCaseMultipleEntities[OrderDTO]):
    def __init__(self, order_service: OrderServiceInterface):
        self.order_service = order_service

    async def execute(self) -> list[OrderDTO]:
        return await self.order_service.list()


class GetOrderUseCase(UseCaseOneEntity[OrderDTO]):
    def __init__(self, order_service: OrderServiceInterface):
        self.order_service = order_service

    async def execute(self, order_id: OrderId) -> OrderDTO | None:
        return await self.order_service.get(order_id)


class UpdateOrderUseCase(UseCaseOneEntity[OrderDTO]):
    def __init__(self, order_service: OrderServiceInterface):
        self.order_service = order_service

    async def execute(self, order_id: OrderId, update_dto: UpdateOrderDTO) -> OrderDTO:
        return await self.order_service.update(order_id, update_dto)


class DeleteOrderUseCase(UseCaseNoReturn):
    def __init__(self, order_service: OrderServiceInterface):
        self.order_service = order_service

    async def execute(self, order_id: OrderId) -> None:
        await self.order_service.delete(order_id)
