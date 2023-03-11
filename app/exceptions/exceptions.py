from fastapi import status
from fastapi.responses import JSONResponse

from .generic_exceptions import AppExceptionBase


class AppException(AppExceptionBase):
    __slots__ = ("details", "status_code", "headers")

    def __init__(
        self,
        details: str,
        status_code: int,
        headers: dict[str, str] = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        self.details = details
        self.status_code = status_code
        self.headers = headers

    def handle(self) -> JSONResponse:
        return JSONResponse(
            headers=self.headers,
            content={"error": self.details},
            status_code=self.status_code,
        )


class Forbidden(AppException):
    def __init__(
        self,
        details: str = "You are not allowed. Contact admin for more info.",
        headers: dict[str, str] = None,
    ) -> None:
        super().__init__(
            details,
            status.HTTP_403_FORBIDDEN,
            headers,
        )


class Unauthorized(AppException):
    def __init__(
        self,
        details: str = "You do not have enough permission.",
        headers: dict[str, str] = None,
    ) -> None:
        super().__init__(
            details,
            status.HTTP_401_UNAUTHORIZED,
            headers,
        )


class BadRequest(AppException):
    def __init__(
        self,
        details: str = "Your request cannot be handled.",
        headers: dict[str, str] = None,
    ) -> None:
        super().__init__(
            details,
            status.HTTP_400_BAD_REQUEST,
            headers,
        )


class NotFound(AppException):
    def __init__(
        self,
        details: str = "The request does not exist.",
        headers: dict[str, str] = None,
    ) -> None:
        super().__init__(
            details,
            status.HTTP_404_NOT_FOUND,
            headers,
        )


class Unprocessable(AppException):
    def __init__(
        self,
        details: str = "Input is invalid.",
        headers: dict[str, str] = None,
    ) -> None:
        super().__init__(
            details,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            headers,
        )
