from fastapi import APIRouter

from ..routers.auth_router import router as auth_router
from ..routers.register_router import router as register_router


router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["authentication"])
router.include_router(register_router, prefix="/register", tags=["registration"])
