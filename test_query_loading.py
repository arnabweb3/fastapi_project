from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import engine
from models.order import Order
from models.product import Product

with Session(engine) as db:
    statement = (
        select(Order)
        .options(selectinload(Order.product))
    )

    orders = db.scalars(statement).all()

    for order in orders:
        print(
            f"Order {order.id}: "
            f"Product = {order.product.name}"
        )