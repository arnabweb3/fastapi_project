from pydantic import BaseModel,Field, ConfigDict

class OrderCreate(BaseModel):
    product_id : int = Field(gt = 0)
    quantity : int = Field(gt = 0)


class OrderUpdate(BaseModel):
    product_id : int | None = None
    quantity: int | None = Field(default=None, gt=0)


class OrderProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # id : int
    name : str
    price : float


class OrderResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id : int
    product_id : int
    quantity : int
    status : str
    product : OrderProductResponse


