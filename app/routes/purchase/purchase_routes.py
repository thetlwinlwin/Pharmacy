from fastapi import APIRouter

purchase_router = APIRouter(
    prefix="/purchase",
    tags=["purchases"],
)
