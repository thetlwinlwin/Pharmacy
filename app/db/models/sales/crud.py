from fastapi import Depends
from sqlalchemy import Connection, event, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.crud_base import CrudBase, exc
from app.db.get_session import get_db
from app.db.models import stocks
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


@event.listens_for(Sale, "after_insert")
def update_inventory_after_insert(_, conn: Connection, target: Sale):
    values = {}
    for i in target.saled_products:
        if i.product_id in values:
            values[i.product_id]["stock_quantity"] += i.quantity
            values[i.product_id]["quantity_unit_id"] += i.quantity_unit_id
        else:
            values[i.product_id] = {
                "stock_quantity": i.quantity,
                "quantity_unit_id": i.quantity_unit_id,
            }

    for input_product_id, input_sale_quantity in values.items():
        in_stock = conn.scalar(
            select(stocks.Stock.stock_quantity).where(
                stocks.Stock.product_id == input_product_id
            )
        )
        if input_sale_quantity["stock_quantity"] > in_stock:
            raise exc.Unprocessable(details="Sale volume is greater than stocks")

    try:
        for id, input_dict in values.items():
            stmt = (
                update(stocks.Stock)
                .where(stocks.Stock.product_id == id)
                .values(
                    stock_quantity=stocks.Stock.stock_quantity
                    - input_dict["stock_quantity"]
                )
            )
            conn.execute(stmt)
    except SQLAlchemyError as e:
        raise exc.BadRequest()


# TODO: this is old
# @event.listens_for(Sale, "after_insert")
# def update_stock(_, conn: Connection, target: Sale):
#     incoming_list = target.saled_products
#     try:
#         for i in incoming_list:
#             stock_item: stocks.Stock = conn.execute(
#                 stocks.Stock.__table__.select().where(
#                     stocks.Stock.product_id == i.product_id
#                 )
#             ).fetchone()
#             if (
#                 stock_item is not None
#                 and stock_item.quantity_unit_id == i.quantity_unit_id
#             ):
#                 conn.execute(
#                     stocks.Stock.__table__.update()
#                     .values(
#                         {
#                             "stock_quantity": stock_item.stock_quantity - i.quantity,
#                         }
#                     )
#                     .where(stocks.Stock.id == stock_item.id)
#                 )
#             else:
#                 conn.execute(
#                     stocks.Stock.__table__.insert().values(
#                         {
#                             "stock_quantity": i.quantity,
#                             "quantity_unit_id": i.quantity_unit_id,
#                             "product_id": i.product_id,
#                         }
#                     )
#                 )
#     except SQLAlchemyError as e:
#         raise exc.BadRequest()
