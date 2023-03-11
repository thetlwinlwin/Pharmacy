import abc

from fastapi import Request
from fastapi.responses import JSONResponse


class AppExceptionBase(Exception, abc.ABC):
    """
    Abstract exception for all exceptions.
    """

    @abc.abstractmethod
    def __init__(self, details: str, status_code: int) -> None:
        pass

    @abc.abstractmethod
    def handle(self) -> JSONResponse:
        pass


def handler(req: Request, exc: AppExceptionBase):
    return exc.handle()
