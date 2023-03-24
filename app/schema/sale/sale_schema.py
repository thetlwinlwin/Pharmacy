from datetime import datetime as dt

from pydantic import BaseModel

from app.schema.user_schema import UserBase

from .sale_product_schema import SaleProductCreate, SaleProductResponse


class SaleBase(BaseModel):
    created_at: dt | None


class SaleIncoming(SaleBase):
    saled_products: list[SaleProductCreate]


class SaleCreate(SaleIncoming):
    user_id: int


class SaleUpdate(SaleIncoming):
    pass

    class Config:
        orm_mode = True


class SaleResponse(BaseModel):
    created_at: dt
    sales_person: UserBase
    saled_products: SaleProductResponse

    class Config:
        orm_mode = True
