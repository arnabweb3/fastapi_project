from fastapi import Depends,HTTPException,status
from schemas.order import *
from dependencies.pagination import get_pagination
from dependencies.request_context import get_request_context
from dependencies.auth import require_admin
from data.orders import orders


from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.order import Order
from models.product import Product

from fastapi import APIRouter


router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)




# GET /orders
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderResponse])
def get_orders(pagination = Depends(get_pagination) , db : Session = Depends(get_db)):
    statement = select(Order)
    orders = db.scalars(statement=statement).all()


    page = pagination['page']
    limit = pagination['limit']

    if page and limit :
        start = (page - 1) * limit
        end = start + limit
        return orders[start:end]

    return orders

# POST /orders
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(order:OrderCreate ,  db : Session = Depends(get_db)):

    new_order = Order(
        product_id = order.product_id,
        quantity = order.quantity      
    )

    try: 

        db.add(new_order)
        db.commit()

        db.refresh(new_order)  

    except Exception:

        db.rollback() 
        raise

    return new_order


# GET /orders/{id}
@router.get("/{order_id}", status_code=status.HTTP_200_OK,  response_model=OrderResponse)
def get_order_by_id(order_id:int , db : Session = Depends(get_db)):

    statement = select(Order).where(
        Order.id == order_id
    )
    existing_order = db.scalars(statement=statement).first()


    if existing_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return existing_order

   



# PATCH /orders/{id}
@router.patch("/{order_id}", status_code=status.HTTP_200_OK)
def update_order(order_id:int,order:OrderUpdate , db : Session = Depends(get_db)):
    # order_exists = any(order['id'] == order_id for order in orders)

    statement = select(Order).where(
        Order.id == order_id
    )
    existing_order = db.scalars(statement=statement).first()

    if existing_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )


    update_data = order.model_dump(
        exclude_unset=True
    )


    if "product_id" in update_data:
        product_statement = select(Product).where(
            Product.id == update_data['product_id']
        )

        product = db.scalars(product_statement).first()

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

    for index,value in update_data.items():
        setattr( existing_order, index, value)


    try:
        db.commit()
        db.refresh(existing_order)

    except Exception:
        db.rollback()
        raise

    return existing_order
    
   
# DELETE /orders/{id}
@router.delete("/{order_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id:int, is_admin = Depends(require_admin), db: Session = Depends(get_db)):
    
    statement = select(Order).where(
        Order.id == order_id
    )
    existing_order = db.scalars(statement=statement).first()

    if existing_order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    try:
        db.delete(existing_order)
        db.commit()
    except Exception:
        db.rollback()
        raise


    return None
    
   
    