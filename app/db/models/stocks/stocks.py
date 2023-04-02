from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


# TODO: should add reorder level.
class Stock(Base):
    """
    To track stocks.
    """

    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        index=True,
        unique=True,
    )
    quantity_unit_id = Column(
        Integer, ForeignKey("quantity_units.id", ondelete="SET NULL")
    )
    stock_quantity = Column(Integer, nullable=False)
    quantity_unit = relationship(
        "QuantityUnit",
        uselist=False,
    )
    product = relationship(
        "Products",
        lazy=False,
        uselist=False,
    )
