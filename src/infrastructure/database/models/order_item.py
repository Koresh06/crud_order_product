from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.infrastructure.database.models.base import Base


if TYPE_CHECKING:
    from src.infrastructure.database.models.product import Product
    from src.infrastructure.database.models.order import Order


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)

    order_rel: Mapped["Order"] = relationship("Order", back_populates="items")
    product_rel: Mapped["Product"] = relationship("Product")

    @property
    def total(self) -> float:
        return self.quantity * self.price