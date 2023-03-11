from pydantic import BaseModel, validator
from app.core.roles import UserRole


class UserBase(BaseModel):
    name: str
    phone: str
    address: str = None
    role: UserRole

    class Config:
        use_enum_values = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    is_active: bool = True
    password: str = None


class UserResponse(UserBase):
    is_active: bool

    class Config:
        orm_mode = True
        use_enum_values = True
