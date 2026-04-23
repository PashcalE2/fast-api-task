from fastapi import APIRouter

from src.api.v1.endpoints import trading


router = APIRouter(prefix="/api/v1")

router.include_router(
    router=trading.router,
    prefix="/trading",
    tags=["Trading"],
)
