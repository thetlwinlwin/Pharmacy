from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class QuantityUnit(Base):
    """
    To Define the different types of product amount.
    """

    __tablename__ = "quantity_units"

    id = Column(Integer, primary_key=True)
    unit = Column(String(50), nullable=False, unique=True, index=True)
