from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import backref, relationship

from app.core.roles import UserRole
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True, index=True)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False)
    password = Column(String, nullable=False)
    refresh_token = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        uselist=False,
    )
    purchases = relationship(
        "Purchase",
        back_populates="issued_user",
        lazy=True,
    )

    @classmethod
    def get_name(cls) -> str:
        return "User"

    def __repr__(self) -> str:
        return f"{self.name} is {self.role} with {self.phone} at{self.address}"
