from fastapi import APIRouter, BackgroundTasks, Depends, Form, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import exceptions as exc
from app.core.roles import UserRole
from app.db.models import oauth_refresh as rt
from app.db.models import users
from app.oauth2.oauth2 import (
    UserRoleChecker,
    create_token,
    get_current_user,
    verify_token,
)
from app.oauth2.passcode_hash import verify_password
from app.schema import token_schema as ts

auth_router = APIRouter()

roles = UserRoleChecker({i.value for i in UserRole})


def add_refresh_token_to_db(
    oauth_service: rt.RefreshTokenCrud,
    incoming_val: ts.RefreshTokenCreate,
) -> None:
    oauth_service.add_with_user_id(incoming_val)


def remove_refresh_token_from_db(oauth_service: rt.RefreshTokenCrud, id: int) -> None:
    oauth_service.delete_by_user_id(user_id=id)


@auth_router.post(
    "/login",
    description="login with phone number.",
    response_model=ts.Token,
)
def login(
    back: BackgroundTasks,
    user_service: users.UserCrud = Depends(users.get_user_crud),
    oauth_service: rt.RefreshTokenCrud = Depends(rt.get_oauth_crud),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    request_user: users.User = user_service.login_with_phone(form_data.username)

    if request_user.is_active != True:
        raise exc.Forbidden()
    if not verify_password(form_data.password, request_user.password):
        raise exc.Unauthorized("Incorrect username or password.", headers=None)

    issued_tokens = create_token(
        role=request_user.role,
        id=request_user.id,
        name=request_user.get_name(),
    )

    incoming_token = ts.RefreshTokenCreate(
        user_id=request_user.id,
        token=issued_tokens["refresh_token"],
    )
    back.add_task(add_refresh_token_to_db, oauth_service, incoming_token)

    return issued_tokens


@auth_router.post(
    "/me/refresh",
    description="revoke access token with refresh token",
    response_model=ts.Token,
)
def refresh_token(
    back: BackgroundTasks,
    grant_type: str = Form(),
    refresh_token: str = Form(),
    user_service: users.UserCrud = Depends(users.get_user_crud),
    oauth_service: rt.RefreshTokenCrud = Depends(rt.get_oauth_crud),
):
    if grant_type != "refresh_token":
        raise exc.Unprocessable()
    data_from_token = verify_token(refresh_token, addadum="Sign in again.")
    user_result: users.User = user_service.get_by_id(data_from_token.client_id)

    if user_result.refresh_token.token != refresh_token:
        user_service.freeze(user_result.id)
        raise exc.Forbidden(headers={"WWW-Authenticate": "Bearer"})

    tokens = create_token(
        role=user_result.role,
        id=user_result.id,
        name=data_from_token.name,
    )
    incoming_token = ts.RefreshTokenCreate(
        user_id=user_result.id,
        token=tokens["refresh_token"],
    )
    back.add_task(add_refresh_token_to_db, oauth_service, incoming_token)

    return ts.Token(**tokens)


@auth_router.post(
    "/logout",
    description="logut",
    dependencies=[Depends(roles)],
)
def logout(
    back: BackgroundTasks,
    user_service: users.UserCrud = Depends(users.get_user_crud),
    oauth_service: rt.RefreshTokenCrud = Depends(rt.get_oauth_crud),
    info: ts.PayloadData = Depends(get_current_user),
):
    user_service.get_self(id=info.client_id)
    back.add_task(remove_refresh_token_from_db, oauth_service, info.client_id)

    return JSONResponse(content="success", status_code=status.HTTP_200_OK)
