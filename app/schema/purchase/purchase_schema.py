from datetime import datetime as dt

from pydantic import BaseModel

from app.schema.user_schema import UserBase

from .purchase_product_schema import PurchaseProductCreate, PurchaseProductResponse


class PurchaseBase(BaseModel):
    created_at: dt | None


class PurchaseIncoming(PurchaseBase):
    purchased_products: list[PurchaseProductCreate]


class PurchaseCreate(PurchaseIncoming):
    user_id: int


class PurchaseUpdate(PurchaseIncoming):
    pass

    class Config:
        orm_mode = True


class PurchaseResponse(BaseModel):
    created_at: dt
    issued_user: UserBase
    purchased_products: PurchaseProductResponse

    class Config:
        orm_mode = True
