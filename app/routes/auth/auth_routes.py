from fastapi import APIRouter, BackgroundTasks, Depends, Form, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import exceptions as exc
from app.db.models import oauth_refresh as rt
from app.db.models import users
from app.oauth2.oauth2 import create_token, verify_token
from app.oauth2.passcode_hash import verify_password
from app.schema import token_schema as ts

auth_router = APIRouter()


def add_refresh_token_to_db(
    oauth_service: rt.RefreshTokenCrud,
    incoming_val: ts.RefreshTokenCreate,
) -> None:
    oauth_service.add_with_user_id(incoming_val)


@auth_router.post(
    "/login",
    description="login with phone number.",
    response_model=ts.Token,
)
def login(
    back_task: BackgroundTasks,
    user_service: users.UserCrud = Depends(users.get_user_crud),
    oauth_service: rt.RefreshTokenCrud = Depends(rt.get_oauth_crud),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    request_user: users.User = user_service.login_with_phone(form_data.username)

    if request_user.is_active != True:
        raise exc.Forbidden()
    if not verify_password(form_data.password, request_user.password):
        raise exc.Unauthorized("Incorrect username or password.", headers=None)

    issued_tokens = create_token(role=request_user.role, id=request_user.id)

    back_task.add_task(
        add_refresh_token_to_db,
        oauth_service=oauth_service,
        incoming_val=ts.RefreshTokenCreate(
            user_id=request_user.id,
            token=issued_tokens["refresh_token"],
        ),
    )
    return issued_tokens


@auth_router.post(
    "/me/refresh",
    description="revoke access token with refresh token",
    response_model=ts.Token,
)
def refresh_token(
    back_task: BackgroundTasks,
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

    tokens = create_token(role=user_result.role, id=user_result.id)

    back_task.add_task(
        add_refresh_token_to_db,
        oauth_service=oauth_service,
        incoming_val=ts.RefreshTokenCreate(
            user_id=user_result.id,
            token=tokens["refresh_token"],
        ),
    )
    return ts.Token(**tokens)
