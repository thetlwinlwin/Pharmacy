from fastapi import APIRouter, Depends, status

import app.schema.quantity_schema as schema
from app.core.roles import UserRole
from app.db.models import quantity_unit as service
from app.oauth2.oauth2 import UserRoleChecker

quantity_unit_router = APIRouter(
    prefix="/quantity-units",
    tags=["quantity units"],
)


allow_roles = UserRoleChecker((UserRole.admin.value, UserRole.doctor.value))

admin_role = UserRoleChecker((UserRole.admin.value))


@quantity_unit_router.post(
    "/batch",
    description="create quantity unit in bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(admin_role),
    ],
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
    dependencies=[
        Depends(admin_role),
    ],
)
def delete_quantity_unit(
    id: int,
    service: service.QuantityUnitCrud = Depends(service.get_quantity_unit_crud),
):
    service.delete_by_id(id)
