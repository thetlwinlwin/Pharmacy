from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProductType(Base):
    """
    Define the product type like tablet, liquid etc.
    All the available products from certain type can be checked.
    """

    __tablename__ = "product_types"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True, index=True)
    products = relationship(
        "Products", back_populates="product_type", order_by="Products.name"
    )

    @classmethod
    def get_name(cls) -> str:
        return "ProductType"

    def __repr__(self) -> str:
        return self.type  # type: ignore
