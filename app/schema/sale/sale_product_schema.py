from pydantic import BaseModel

from app.schema.products_schema import ProductResponse
from app.schema.quantity_schema import QuantityUnitResponse


class SaleProductBase(BaseModel):
    barcode: str | None
    quantity: int
    quantity_unit_id: int


class SaleProductCreate(SaleProductBase):
    product_id: int


class SaleProudctUpdate(BaseModel):
    product_id: int | None
    barcode: str | None
    quantity: int | None


class SaleProductResponse(BaseModel):
    product: ProductResponse
    quantity_unit: int
    quantity_unit: QuantityUnitResponse

    class Config:
        orm_mode = True
