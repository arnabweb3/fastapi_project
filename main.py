from fastapi import FastAPI

from routes.products import router as product_routes
from routes.orders import router as order_routes
from routes.users import router as user_routes
from routes.auth import router as auth_routes
app = FastAPI()






app.include_router(product_routes)
app.include_router(order_routes)
app.include_router(user_routes)
app.include_router(auth_routes)


# GET /
@app.get("/")
def home():
    return {"message" : "Welcome to FastAPI"}


