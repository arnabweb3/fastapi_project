from database import Base
from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import Integer, String , ForeignKey
# from models.product import Product
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.product import Product


class Order(Base):
    __tablename__ = 'orders'


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=False
    )

   
    product_id: Mapped[int] = mapped_column(
        # Integer,
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="orders"

    )
    



    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="SUCCESS"
    )