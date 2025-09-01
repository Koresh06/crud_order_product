from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Enum, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.domain.value_objects.currency import Currency
from src.domain.value_objects.order_status import OrderStatus
from src.infrastructure.database.models.base import Base


if TYPE_CHECKING:
    from src.infrastructure.database.models.order_item import OrderItem


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    currency: Mapped[Currency] = mapped_column(Enum(Currency), default=Currency.USD, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order_rel",
        cascade="all, delete",
        passive_deletes=True,
        lazy="selectin",
    )

    @property
    def total_amount(self) -> float:
        return sum(item.total for item in self.items)


