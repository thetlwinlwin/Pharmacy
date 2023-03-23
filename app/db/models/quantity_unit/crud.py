from fastapi import Depends
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.crud_base import CrudBase, exc
from app.db.get_session import get_db
from app.schema.quantity_schema import QuantityUnitBase

from .quantity_unit import QuantityUnit


class QuantityUnitCrud(CrudBase[QuantityUnit, QuantityUnitBase, QuantityUnitBase]):
    def __init__(self, model: QuantityUnit, db_session: Session) -> None:
        super().__init__(model, db_session)

    def create_in_bulk(
        self,
        input_objs: list[QuantityUnitBase],
    ) -> None:
        try:
            self._db_session.execute(
                insert(self.model),
                [i.dict() for i in input_objs],
            )
            self._db_session.commit()
        except SQLAlchemyError as e:
            exc.Unprocessable()


def get_quantity_unit_crud(db_session: Session = Depends(get_db)):
    return QuantityUnitCrud(
        db_session=db_session,
        model=QuantityUnit,
    )
