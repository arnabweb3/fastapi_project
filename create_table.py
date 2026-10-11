from database import engine,Base
from models.product import Product
from models.order import Order


Base.metadata.create_all(bind=engine)

print("Table created in database successfully")
