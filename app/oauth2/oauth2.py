from datetime import datetime, timedelta

from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt

from app import exceptions as exc
from app.core.settings import settings
from app.db.models import users
from app.schema.token_schema import PayloadData

from ..core.roles import UserRole

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINS = settings.access_token_expire_mins
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

# the tokenurl is whatever url in auth.py login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(role: UserRole, id: int) -> dict[str, str]:
    """
    Responsible for creating the refresh and access token.
    """
    data = PayloadData(client_id=id, role=role)

    access_expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    refresh_expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = jwt.encode(
        data.copy(update={"exp": access_expire}).dict(),
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    refresh_token = jwt.encode(
        data.copy(update={"exp": refresh_expire}).dict(),
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


def verify_token(incoming_token: str, addadum: str = "") -> PayloadData:
    """
    Verify the incoming token.
    If client_id is missing, this will raise http exception.
    """
    try:
        payload = jwt.decode(
            incoming_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        token_data = PayloadData(**payload)
        return token_data
    except JWTError as e:
        if isinstance(e, ExpiredSignatureError):
            raise exc.Unauthorized(
                details=f"{str(e)}{addadum}", headers={"WWW-Authenticate": "Bearer"}
            )
        raise exc.Unauthorized(details=str(e), headers={"WWW-Authenticate": "Bearer"})


def get_current_user(
    user_service: users.UserCrud = Depends(users.get_user_crud),
    # access_token: str = Depends(oauth2_scheme),
    access_token: str | None = Cookie(default=None),
) -> PayloadData:
    """
    get the payload data from access_token.
    """

    result: PayloadData = verify_token(access_token)

    # this sql will raise error if user is not active.
    current_user = user_service.get_only_the_id(id=result.client_id)
    if not current_user.is_active:
        raise exc.Forbidden(headers={"WWW-Authenticate": "Bearer"})
    return result


class UserRoleChecker:
    def __init__(self, allowed_roles: set[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        data: PayloadData = Depends(get_current_user),
    ) -> PayloadData:
        if not data.role in self.allowed_roles:
            raise exc.Unauthorized(
                details="You don't have enough permission.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return data


# NOTE: it doesn't make sense to use the security scope here.

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="login",
#     scopes=UserRole.get_all_scopes(),
# )

# def get_current_user(
#     security_scopes: SecurityScopes,
#     access_token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db),
# ) -> None | PayloadData:

#     if security_scopes.scopes:
#         auth_values = f'Bearer scope="{security_scopes.scope_str}"'
#     else:
#         auth_values = f"Bearer"
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": auth_values},
#     )

#     data: PayloadData = verify_token(
#         incoming_token=access_token,
#         credentials_exception=credentials_exception,
#     )
#     # no need to raise error as it's been already raised in crud model.
#     users.user_crud.get_by_id(db, data.client_id)
#     for scope in security_scopes.scopes:
#         print(f"security scopes {scope}")
#         if scope != data.role:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not enough permissions",
#                 headers={"WWW-Authenticate": auth_values},
#             )
#     return data
