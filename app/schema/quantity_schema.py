from pydantic import BaseModel


class QuantityUnitBase(BaseModel):
    unit: str


class QuantityUnitResponse(QuantityUnitBase):
    pass

    class Config:
        orm_mode = True
