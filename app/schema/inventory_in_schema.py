from datetime import datetime as dt

from pydantic import BaseModel

from .products_schema import ProductBase
from .user_schema import UserBase


class InventoryInBase(BaseModel):
    created_at: dt | None


class InventoryInCreate(InventoryInBase):
    user_id: int
    quantity: int
    quantity_unit_id: int
    product_id: int
