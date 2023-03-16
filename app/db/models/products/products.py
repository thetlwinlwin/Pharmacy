from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Products(Base):
    """
    This to create the medicine products.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True, unique=True)
    description = Column(String, nullable=True)
    product_type_id = Column(ForeignKey("product_types.id"))
    product_type = relationship("ProductType", back_populates="products", uselist=False)
    # dose_amount = Column(Integer, nullable=False)
    # dose_unit_id = Column(ForeignKey("dose_units.id"))
    # dose_unit = relationship("DoseUnit", uselist=False)
    # category_id = Column(ForeignKey("product_categories.id"))
    # category = relationship("ProductCategory", back_populates="products", uselist=False)

    available = relationship(
        "PurchasedProducts",
        back_populates="product",
    )

    @classmethod
    def get_name(cls) -> str:
        return "Products"

    def __repr__(self) -> str:
        return f"{self.name}"


# class ProductCategory(Base):
#     """
#     To categorize the products according to user's liking.

#     For the sake of simplicity, there is no sub category.
#     The implementation can easily be done and it can be seen in test folder.
#      All the available products from certain category can be checked.
#     """

#     __tablename__ = "product_categories"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False, index=True)
#     # we really don't want to delete product if category is deleted. so omit the passvie_delete
#     products = relationship(
#         "Products", back_populates="category", order_by="Products.name"
#     )

#     @classmethod
#     def get_name(cls) -> str:
#         return "ProductCategory"

#     def __repr__(self) -> str:
#         return f"{self.name} category."


# class DoseUnit(Base):
#     """
#     Define unit for each product.

#     The relationship with product is purposely left out to remove the ability to filter/sort/group by.
#     """

#     __tablename__ = "dose_units"

#     id = Column(Integer, primary_key=True)
#     unit = Column(String(20), nullable=False)

#     @classmethod
#     def get_name(cls) -> str:
#         return "DoseUnit"


# NOTE: this is for querying all sub categories. More in test.py
#  all_sub_query = (
#         session.query(ProductCategory).filter(ProductCategory.parent_id != None).all()
#     )
