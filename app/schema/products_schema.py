from pydantic import BaseModel, validator


class ProductTypeBase(BaseModel):
    type: str

    class Config:
        orm_mode = True


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeResponse(ProductTypeBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: str | None


class ProductCreate(ProductBase):
    product_type_id: int


class ProductUpdate(BaseModel):
    name: str | None
    description: str | None
    product_type_id: int | None


class ProductResponse(ProductBase):
    product_type: ProductTypeBase

    class Config:
        orm_mode = True


class ProductNames(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
