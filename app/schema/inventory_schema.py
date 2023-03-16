from datetime import datetime as dt

from pydantic import BaseModel


class InventoryBase(BaseModel):
    name: str
    quantity: int
    quantity_unit: str
