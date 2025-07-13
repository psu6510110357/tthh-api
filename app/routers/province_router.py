from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List
from ..models.province_model import DBProvince
from ..models.user_model import DBUser
from ..core.database import get_session
from ..schemas.province_schema import AssignProvinceRequest
from ..schemas.user_schema import UserResponseWithProvince

router = APIRouter(tags=["province"])


@router.get("/", response_model=List[DBProvince])
async def read_all_provinces(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(DBProvince))
    provinces = result.all()
    return provinces


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
