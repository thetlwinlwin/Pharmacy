from fastapi import Depends
from sqlalchemy import Connection, event
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.crud_base import CrudBase, exc
from app.db.get_session import get_db
from app.db.models import stocks
from app.schema.purchase import PurchaseCreate, PurchaseUpdate

from .purchase import Purchase, PurchasedProducts


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


def get_purchase_crud(db_session: Session = Depends(get_db)):
    return PurchaseCrud(
        db_session=db_session,
        model=Purchase,
    )


@event.listens_for(Purchase, "after_insert")
def update_inventory_after_insert(_, conn: Connection, target: Purchase):
    values = {}
    for i in target.purchased_products:
        if i.product_id in values:
            values[i.product_id]["stock_quantity"] += i.quantity
            values[i.product_id]["quantity_unit_id"] += i.quantity_unit_id
        else:
            values[i.product_id] = {
                "stock_quantity": i.quantity,
                "quantity_unit_id": i.quantity_unit_id,
            }

    stmt = postgresql.insert(stocks.Stock).values(
        [
            {
                "product_id": i,
                **ii,
            }
            for i, ii in values.items()
        ]
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=[stocks.Stock.product_id],
        set_={
            "stock_quantity": stocks.Stock.stock_quantity + stmt.excluded.stock_quantity
        },
    )
    try:
        conn.execute(stmt)
    except SQLAlchemyError as e:
        raise exc.BadRequest()
