from fastapi import Depends
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.crud_base import CrudBase, exc
from app.db.get_session import get_db
from app.schema.purchase import PurchaseCreate, PurchaseUpdate, QuantityUnitBase

from .purchase import Purchase, PurchasedProducts
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


class PurchaseCrud(CrudBase[Purchase, PurchaseCreate, PurchaseUpdate]):
    def __init__(self, model: Purchase, db_session: Session) -> None:
        super().__init__(model, db_session)

    def create(self, input_obj: PurchaseCreate) -> None:
        new_obj = self.model(
            user_id=input_obj.user_id,
            purchased_products=[
                PurchasedProducts(**x.dict()) for x in input_obj.purchased_products
            ],
        )
        try:
            self._db_session.add(new_obj)
            self._db_session.commit()
        except SQLAlchemyError as e:
            raise exc.Unprocessable()


def get_quantity_unit_crud(db_session: Session = Depends(get_db)):
    return QuantityUnitCrud(
        db_session=db_session,
        model=QuantityUnit,
    )


def get_purchase_crud(db_session: Session = Depends(get_db)):
    return PurchaseCrud(
        db_session=db_session,
        model=Purchase,
    )
