from pydantic import BaseModel

from app.core.roles import UserRole


class Token(BaseModel):
    token_type: str | None = "bearer"
    access_token: str
    refresh_token: str


class PayloadData(BaseModel):
    client_id: int
    role: UserRole

    class Config:
        orm_mode = True
        use_enum_values = True


class TokenCreate(Token):
    refresh_token: str


class RefreshToken(BaseModel):
    token: str
    user_id: int

    class Confing:
        orm_mode = True


class RefreshTokenCreate(RefreshToken):
    ...


class RefreshTokenUpdate(RefreshToken):
    ...
