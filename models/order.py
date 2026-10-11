from database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer, String , ForeignKey

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
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="SUCCESS"
    )