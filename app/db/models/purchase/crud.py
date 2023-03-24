from fastapi import Depends
from sqlalchemy import Connection, event
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
    incoming_list = target.purchased_products
    stock_values = []
    try:
        for i in incoming_list:
            stock_item: stocks.Stock = conn.execute(
                stocks.Stock.__table__.select().where(
                    stocks.Stock.product_id == i.product_id
                )
            ).fetchone()
            if (
                stock_item is not None
                and stock_item.quantity_unit_id == i.quantity_unit_id
            ):
                conn.execute(
                    stocks.Stock.__table__.update()
                    .values(
                        {
                            "stock_quantity": stock_item.stock_quantity + i.quantity,
                        }
                    )
                    .where(stocks.Stock.id == stock_item.id)
                )
            else:
                conn.execute(
                    stocks.Stock.__table__.insert().values(
                        {
                            "stock_quantity": i.quantity,
                            "quantity_unit_id": i.quantity_unit_id,
                            "product_id": i.product_id,
                        }
                    )
                )
    except SQLAlchemyError as e:
        raise exc.BadRequest()
