from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ..core.database import get_session
from ..models.province_model import DBProvince
from ..schemas.province_schema import AssignProvinceRequest
from ..schemas.user_schema import UserResponseWithProvince
from ..core.deps import get_current_user
from ..models.user_model import DBUser, User

router = APIRouter(tags=["user"])


@router.get("/me", response_model=User)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/assign-province", response_model=UserResponseWithProvince)
async def assign_province_to_user(
    req: AssignProvinceRequest, session: AsyncSession = Depends(get_session)
):
    user = await session.get(DBUser, req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    province = await session.get(DBProvince, req.province_id)
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    user.province_id = req.province_id
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserResponseWithProvince(
        id=str(user.id),
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        province_id=str(user.province_id),
        province_name=province.name,
    )
