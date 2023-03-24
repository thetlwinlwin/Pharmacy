from fastapi import APIRouter, Depends, status

import app.db.models.sales as sale_service
import app.schema.sale as sale_schema
from app.core.roles import UserRole
from app.oauth2.oauth2 import UserRoleChecker
from app.schema import token_schema

sale_router = APIRouter(
    prefix="/sales",
    tags=["sales"],
)

allow_roles = UserRoleChecker(
    (
        UserRole.admin.value,
        UserRole.doctor.value,
    )
)


@sale_router.post(
    "/",
    description="Create sale",
    status_code=status.HTTP_201_CREATED,
)
def create_sale(
    new_obj: sale_schema.SaleIncoming,
    user_role: token_schema.PayloadData = Depends(allow_roles),
    sale_service: sale_service.SaleCrud = Depends(sale_service.get_sale_crud),
):
    obj_to_create = sale_schema.SaleCreate(
        **new_obj.dict(),
        user_id=user_role.client_id,
    )
    sale_service.create(obj_to_create)
