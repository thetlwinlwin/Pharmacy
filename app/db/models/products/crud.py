from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.crud_base import CrudBase, exc
from app.db.get_session import get_db
from app.schema.products_schema import (
    ProductCreate,
    ProductNames,
    ProductResponse,
    ProductTypeCreate,
    ProductTypeResponse,
    ProductUpdate,
)

from .product_types import ProductType
from .products import Products


class ProductCrud(CrudBase[Products, ProductCreate, ProductUpdate]):
    def __init__(self, model: Products, db_session: Session) -> None:
        super().__init__(model, db_session)

    def create_in_bulk(
        self,
        input_objs: list[ProductCreate],
    ) -> None:
        try:
            self._db_session.execute(
                insert(self.model),
                [i.dict() for i in input_objs],
            )
            self._db_session.commit()
        except SQLAlchemyError as e:
            exc.Unprocessable()

    def get_all_product_names(self) -> list[ProductNames]:
        try:
            results = self._db_session.query(self.model.id, self.model.name).all()
            return results
        except SQLAlchemyError:
            raise exc.NotFound()

    def get_all_products(self) -> list[ProductResponse]:
        try:
            results = self._db_session.query(self.model).all()
            print(f"result is {results}")
            return results
        except SQLAlchemyError:
            raise exc.NotFound()


class ProductTypeCrud(CrudBase[ProductType, ProductTypeCreate, ProductTypeCreate]):
    def __init__(self, model: ProductType, db_session: Session) -> None:
        super().__init__(model, db_session)

    def create_in_bulk(
        self,
        input_objs: list[ProductTypeCreate],
    ) -> None:
        try:
            self._db_session.execute(
                insert(self.model),
                [i.dict() for i in input_objs],
            )
            self._db_session.commit()
        except SQLAlchemyError as e:
            exc.Unprocessable()

    def get_all_product_types(self) -> list[ProductTypeResponse]:
        try:
            results = self._db_session.query(self.model.id, self.model.type).all()
            return results
        except SQLAlchemyError:
            raise exc.NotFound()


# fastapi style depends
def get_product_crud(db_session: Session = Depends(get_db)):
    return ProductCrud(
        model=Products,
        db_session=db_session,
    )


def get_product_type_crud(db_session: Session = Depends(get_db)):
    return ProductTypeCrud(
        model=ProductType,
        db_session=db_session,
    )
