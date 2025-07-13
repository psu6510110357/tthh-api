from fastapi import APIRouter

from ..routers.auth_router import router as auth_router
from ..routers.register_router import router as register_router
from ..routers.province_router import router as province_router
from ..routers.user_router import router as user_router

# Create the main router and include all sub-routers
router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["authentication"])
router.include_router(register_router, prefix="/register", tags=["registration"])
router.include_router(province_router, prefix="/provinces", tags=["province"])
router.include_router(user_router, prefix="/user", tags=["user"])
