from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="refresh_token")

    @classmethod
    def get_name(cls) -> str:
        return "RefreshToken"

    def __repr__(self) -> str:
        return f"{self.id} is token of {self.user_id}."
