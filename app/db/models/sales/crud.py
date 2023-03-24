from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.crud_base import CrudBase, exc
from app.db.get_session import get_db
from app.schema import sale as schema

from .sales import Sale, SaledProducts


class SaleCrud(CrudBase[Sale, schema.SaleCreate, schema.SaleUpdate]):
    def __init__(self, model: Sale, db_session: Session) -> None:
        super().__init__(model, db_session)

    def create(self, input_obj: schema.SaleCreate) -> None:
        new_obj = self.model(
            user_id=input_obj.user_id,
            saled_products=[
                SaledProducts(**x.dict()) for x in input_obj.saled_products
            ],
        )
        try:
            self._db_session.add(new_obj)
            self._db_session.commit()
        except SQLAlchemyError as e:
            raise exc.Unprocessable()


def get_sale_crud(db_session: Session = Depends(get_db)):
    return SaleCrud(
        db_session=db_session,
        model=Sale,
    )
