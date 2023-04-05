import time

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import exceptions as exc
from app import routes


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """ReWrite the pydantic request model error into simple one line."""

    error_message = ""
    for i in exc.errors():
        error_message = i.get("msg")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": error_message},
    )


app = FastAPI(
    title="My Pharmacy",
    exception_handlers={
        exc.AppExceptionBase: exc.handler,
        RequestValidationError: validation_exception_handler,
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(routes.auth_router)
app.include_router(routes.user_router)
app.include_router(routes.products_router)
app.include_router(routes.purchase_router)
app.include_router(routes.quantity_unit_router)
app.include_router(routes.sale_router)
