from datetime import datetime as dt

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime

from app.db.base import Base


class Sale(Base):
    """
    To record every sales
    """

    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=dt.utcnow())

    sales_person = relationship(
        "User",
        back_populates="all_sales",
        uselist=False,
    )
    saled_products = relationship(
        "SaledProducts",
        lazy=False,
        passive_deletes=True,
    )


class SaledProducts(Base):
    __tablename__ = "saled_products"
    id = Column(Integer, primary_key=True)
    product_id = Column(
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=False,
    )
    sales_id = Column(
        ForeignKey("sales.id", ondelete="CASCADE"),
    )
    quantity_unit_id = Column(
        ForeignKey("quantity_units.id", ondelete="set null"),
        nullable=False,
    )
    barcode = Column(String, nullable=True, index=True)
    quantity = Column(Integer, nullable=False)
    quantity_unit = relationship("QuantityUnit", uselist=False)

    sales = relationship(
        "Sale",
        back_populates="saled_products",
        uselist=False,
    )

    product = relationship(
        "Products",
        lazy=False,
        uselist=False,
    )
