from pydantic import BaseModel

from app.schema.products_schema import ProductResponse
from app.schema.quantity_schema import QuantityUnitResponse


class PurchaseProductBase(BaseModel):
    quantity_unit_id: int
    barcode: str | None
    quantity: int


class PurchaseProductCreate(PurchaseProductBase):
    product_id: int


class PurchaseProudctUpdate(BaseModel):
    product_id: int | None
    quantity_unit_id: int | None
    barcode: str | None
    quantity: int | None


class PurchaseProductResponse(BaseModel):
    product: ProductResponse
    quantity_unit: int
    quantity_unit: QuantityUnitResponse

    class Config:
        orm_mode = True
