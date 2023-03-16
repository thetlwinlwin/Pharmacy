from fastapi import APIRouter, Depends, status

import app.db.models.purchase as purchase_service
import app.schema.purchase as purchase_schema
from app.core.roles import UserRole
from app.oauth2.oauth2 import UserRoleChecker
from app.schema import token_schema

purchase_router = APIRouter(
    prefix="/purchase",
    tags=["purchases"],
)
allow_roles = UserRoleChecker((UserRole.admin.value, UserRole.doctor.value))


@purchase_router.post(
    "/",
    description="Create purchase",
    status_code=status.HTTP_201_CREATED,
)
def create_purchase(
    new_obj: purchase_schema.PurchaseIncoming,
    user_role: token_schema.PayloadData = Depends(allow_roles),
    purchase_service: purchase_service.PurchaseCrud = Depends(
        purchase_service.get_purchase_crud
    ),
):
    obj_to_create = purchase_schema.PurchaseCreate(
        **new_obj.dict(),
        user_id=user_role.client_id,
    )
    purchase_service.create(obj_to_create)
