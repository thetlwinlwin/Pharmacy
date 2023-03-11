from fastapi import APIRouter, Depends, status

from app.db.models import purchase as service
from app.schema import purchase as schema

quantity_unit_router = APIRouter(
    prefix="/quantity-units",
    tags=["quantity units"],
)


@quantity_unit_router.post(
    "/batch",
    description="create quantity unit in bulk",
    status_code=status.HTTP_201_CREATED,
)
def create_unit_in_bulk(
    new_objs: list[schema.QuantityUnitBase],
    service: service.QuantityUnitCrud = Depends(service.get_quantity_unit_crud),
):
    service.create_in_bulk(new_objs)


@quantity_unit_router.delete(
    "/{id}",
    description="delete quantity unit by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_quantity_unit(
    id: int,
    service: service.QuantityUnitCrud = Depends(service.get_quantity_unit_crud),
):
    service.delete_by_id(id)
