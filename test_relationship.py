from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models.order import Order
from models.product import Product

with Session(engine) as db:
    order = db.scalars(select(Order)).first()

    if order is not None:
        print("Order ID:", order.id)
        print("Product:", order.product.name)
        print("Product ID:", order.product.id)

    product = db.scalars(select(Product)).first()

    if product is not None:
        print("Product:", product.name)
        print("Order count:", len(product.orders))