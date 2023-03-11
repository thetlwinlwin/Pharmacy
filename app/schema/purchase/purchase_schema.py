from datetime import datetime as dt

from pydantic import BaseModel

from app.schema.user_schema import UserBase

from .purchase_product_schema import PurchaseProductCreate, PurchaseProductResponse


class PurchaseBase(BaseModel):
    user_id: int
    created_at: dt | None


class PurchaseCreate(PurchaseBase):
    purchased_products: list[PurchaseProductCreate]


class PurchaseUpdate(PurchaseCreate):
    pass

    class Config:
        orm_mode = True


class PurchaseResponse(BaseModel):
    created_at: dt
    issued_user: UserBase
    purchased_products: PurchaseProductResponse

    class Config:
        orm_mode = True
