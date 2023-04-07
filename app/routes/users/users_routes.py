from fastapi import APIRouter, Depends, Form, Request, Response, status

from app import exceptions as exc
from app.core.roles import UserRole
from app.core.settings import settings
from app.db.models import users
from app.oauth2.oauth2 import UserRoleChecker, get_current_user
from app.oauth2.passcode_hash import get_password_pash, verify_password
from app.schema import token_schema as ts
from app.schema import user_schema

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


creator = UserRoleChecker({UserRole.admin.value})


@user_router.get(
    "/search",
    description="Search user by name or phone",
    response_model=list[user_schema.UserResponse],
    dependencies=[Depends(creator)],
)
def admin_search_users(
    req: Request,
    user_service: users.UserCrud = Depends(users.get_user_crud),
):
    params: dict = req.query_params._dict
    return user_service.search(params)


@user_router.post(
    "/admin-origin",
    description="Create admin for the first time.",
)
def create_origin(
    new_obj: user_schema.UserCreate,
    user_service: users.UserCrud = Depends(users.get_user_crud),
):
    is_admin_apply = new_obj.role == UserRole.admin.value
    if not is_admin_apply:
        raise exc.Forbidden(details="Has to be an admin.")
    # don't need to catch exception as it has already done in crud.
    user_service.check_empty()
    new_obj.password = get_password_pash(password=new_obj.password)
    user_service.create(new_obj)
    return Response(status_code=status.HTTP_201_CREATED)


@user_router.post(
    "/create",
    description="To Create User",
    dependencies=[Depends(creator)],
)
def admin_create_user(
    new_obj: user_schema.UserCreate,
    user_service: users.UserCrud = Depends(users.get_user_crud),
):
    is_admin_apply = new_obj.role == UserRole.admin.value
    if is_admin_apply:
        user_service.is_admin_not_full(settings.admin_limits)
    new_obj.password = get_password_pash(password=new_obj.password)
    user_service.create(new_obj)
    return Response(status_code=status.HTTP_201_CREATED)


@user_router.get(
    "/me",
)
def get_self(
    user_service: users.UserCrud = Depends(users.get_user_crud),
    info: ts.PayloadData = Depends(get_current_user),
):
    return user_service.get_self(id=info.client_id)


@user_router.get(
    "/{id}",
    description="To Get User by id",
    response_model=user_schema.UserResponse,
    dependencies=[Depends(creator)],
)
def admin_get_user(
    id: int,
    user_service: users.UserCrud = Depends(users.get_user_crud),
):
    return user_service.get_by_id(id)


@user_router.put(
    "/update/{id_to_update}",
    description="To Update User. Admin cannot do anything to another admin.",
    response_model=user_schema.UserResponse,
    dependencies=[Depends(creator)],
)
def admin_update_user(
    id_to_update: int,
    new_obj: user_schema.UserUpdate,
    user_service: users.UserCrud = Depends(users.get_user_crud),
):
    old_obj_to_change = user_service.get_by_id(id_to_update)
    if old_obj_to_change.role == UserRole.admin:
        raise exc.Forbidden(
            details="Configuration of an admin cannot be changed by another admin."
        )

    if new_obj.role == UserRole.admin.value:
        user_service.is_admin_not_full(settings.admin_limits)

    if new_obj.password:
        new_obj.password = get_password_pash(password=new_obj.password)

    return user_service.update_by_id(id_to_update, new_obj)


# this is for non-admin user.
@user_router.put(
    "/me/update",
    description="To Update User. Only admin can change his role.",
    response_model=user_schema.UserResponse,
)
def update_user(
    new_obj: user_schema.UserUpdate,
    user_service: users.UserCrud = Depends(users.get_user_crud),
    info: ts.PayloadData = Depends(get_current_user),
):
    is_admin = info.role == UserRole.admin

    # this prevents from non admin to change his role.
    if not is_admin:
        new_obj.role = info.role

    return user_service.update_by_id(info.client_id, new_obj)


@user_router.delete(
    "/me/delete",
    description="To Delete User by id",
)
def delete_user(
    user_service: users.UserCrud = Depends(users.get_user_crud),
    info: ts.PayloadData = Depends(get_current_user),
):
    user_service.delete_by_id(info.client_id)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@user_router.put(
    "/me/change-passcode",
    response_model=user_schema.UserResponse,
)
def chanage_password(
    old_password: str = Form(),
    new_password: str = Form(),
    confirm_password: str = Form(),
    user_service: users.UserCrud = Depends(users.get_user_crud),
    info: ts.PayloadData = Depends(get_current_user),
):
    user_to_update: users.User = user_service.get_by_id(info.client_id)

    password_verification = verify_password(old_password, user_to_update.password)
    if new_password != confirm_password or not password_verification:
        raise exc.Unprocessable(details="Password doesn't match.")

    return user_service.change_passcode(
        id=user_to_update.id,
        new_password=get_password_pash(new_password),
    )
