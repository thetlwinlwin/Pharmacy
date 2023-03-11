from datetime import datetime as dt

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime

from app.db.base import Base


class Purchase(Base):
    """
    To monitor all of the purchased products.
    """

    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=dt.utcnow())

    issued_user = relationship(
        "User",
        back_populates="purchases",
        uselist=False,
    )
    purchased_products = relationship(
        "PurchasedProducts",
        back_populates="purchase",
        lazy=False,
        passive_deletes=True,
    )


class PurchasedProducts(Base):
    __tablename__ = "purchased_products"
    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey("products.id", ondelete="CASCADE"))
    purchase_id = Column(ForeignKey("purchases.id", ondelete="CASCADE"))
    quantity_unit_id = Column(
        ForeignKey("quantity_units.id", ondelete="set null"),
    )
    barcode = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    quantity_unit = relationship("QuantityUnit", uselist=False)

    purchase = relationship(
        "Purchase",
        back_populates="purchased_products",
        uselist=False,
    )
    product = relationship(
        "Products",
        lazy=False,
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"{self.purchase_id} and {self.quantity} {self.quantity_unit} and {self.product_id}"
