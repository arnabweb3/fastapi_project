from database import Base
from sqlalchemy import Integer, String, Float, Text, CheckConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship
# from models.order import Order
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.order import Order


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_products_price_nonnegative"),
        CheckConstraint("quantity >= 0", name="ck_quantity_nonnegative")
    )

    id: Mapped[int] = mapped_column(

        Integer,
        primary_key = True,
        index = True
    )

    orders : Mapped[list["Order"]] = relationship(
        "Order",
        back_populates='product'

    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    quantity:Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


