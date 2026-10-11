from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name :  str = Field(min_length = 2, max_length = 30)
    price : float = Field(ge = 0)
    quantity : int = Field(ge = 0)
    description: str | None = None


class ProductUpdate(BaseModel):
    name : str | None = None
    price : float | None = Field(default=None, ge=0)
    quantity : int | None = Field(default=None, ge=0)
    description: str | None = None



class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id :  int
    name : str
    price : float
    quantity : int
    description :  str | None


