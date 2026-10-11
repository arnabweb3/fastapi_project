from fastapi import status,Depends,HTTPException
from fastapi import APIRouter
from schemas.product import *
from dependencies.pagination import get_pagination
from dependencies.request_context import get_request_context
from dependencies.auth import require_admin
from data.products import products


from database import get_db
from sqlalchemy.orm import Session
from models.product import Product
from sqlalchemy import select


router = APIRouter(
    prefix="/products",
    tags= ["Products"]

)



@router.get("/headers")
def get_request_headers(client_id = Depends(get_request_context)):
    return {
        "client_id" : client_id
    }




# GET /products
@router.get(
        "/",  
        status_code=status.HTTP_200_OK, 
        response_model=list[ProductResponse]
)
def get_products(pagination = Depends(get_pagination) , db : Session = Depends(get_db)):
    # fetch the products from database
    statement = select(Product)
    products = db.scalars(statement=statement).all()
    
    page = pagination['page']
    limit = pagination['limit']

    if page and limit:
        start = (page - 1) * limit
        end = start + limit
        

        return products[start:end]
    return products





# # GET /products/{product_id}
@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def get_product_by_id(product_id:int, db : Session = Depends(get_db)):

    statement = select(Product).where(
        Product.id == product_id
    )
    product = db.scalars(statement=statement).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product
    


# # POST /products
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product : ProductCreate , db : Session = Depends(get_db)):
    
    new_product = Product(
        name = product.name,
        price = product.price,
        quantity = product.quantity,
        description = product.description
    )

    try: 

        db.add(new_product)

        db.commit()

        db.refresh(new_product)

    except Exception:

        db.rollback()
        raise 

    return new_product



@router.patch("/{product_id}" , status_code=status.HTTP_200_OK)
def update_product(product_id : int, product:ProductUpdate, db : Session = Depends(get_db)):


    statement = select(Product).where(
        Product.id == product_id
    )

    existing_product = db.scalars(statement=statement).first()


    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update_data = product.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(existing_product, field, value)



    try: 

        db.commit()

        db.refresh(existing_product)

    except Exception:

        db.rollback()
        raise

    return existing_product

       


# DELETE /products/{product_id}
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id:int, user = Depends(require_admin), db : Session = Depends(get_db)):
    statement = select(Product).where(
        Product.id == product_id
    )

    existing_product = db.scalars(statement=statement).first()

    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


    try:


        db.delete(existing_product)
        db.commit()

    except Exception:

        db.rollback()
        raise 

    return None


    # product_exists = any(product['id'] == product_id for product in products)
    
    
    # if product_exists:
    #     existing_product = next( p for p in products if p['id'] == product_id)
    #     products.remove(existing_product)

    #     return None
    # else:
    #     raise HTTPException(status_code=404,detail="Product Not found")
