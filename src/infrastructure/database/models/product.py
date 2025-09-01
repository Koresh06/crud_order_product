from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, Float, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.value_objects.product_category import ProductCategory
from src.infrastructure.database.models.base import Base


if TYPE_CHECKING:
    from src.infrastructure.database.models.order_item import OrderItem


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(225))
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[ProductCategory] = mapped_column(SAEnum(ProductCategory), default=ProductCategory.OTHER)
    description: Mapped[str | None] = mapped_column(String)

    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product_rel",
        cascade="all, delete",
        passive_deletes=True,
    )