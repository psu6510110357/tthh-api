from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ..core.database import get_session
from ..models.province_model import DBProvince
from ..schemas.province_schema import AssignProvinceRequest
from ..schemas.user_schema import UserResponseWithProvince
from ..core.deps import get_current_user
from ..models.user_model import DBUser, User

router = APIRouter(tags=["user"])

# Define the endpoint to get the current user
@router.get("/me", response_model=User)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


# Define the endpoint to assign a province to a user
@router.patch("/assign-province", response_model=UserResponseWithProvince)
async def assign_province_to_user(
    req: AssignProvinceRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):  # Get the current user from the get_current_user dependency
    user = await session.get(DBUser, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    province = await session.get(DBProvince, req.province_id)
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    user.province_id = req.province_id  # Assign the province ID to the user
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserResponseWithProvince(  # Create UserResponseWithProvince from DBUser
        id=str(user.id),
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        province_id=str(user.province_id),
        province_name=province.name,
    )


# Define the endpoint to get the user's province
@router.get("/province", response_model=DBProvince)
async def get_my_province(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if not current_user.province_id:
        raise HTTPException(status_code=404, detail="User has no province assigned")
    province = await session.get(DBProvince, current_user.province_id)
    if not province:
        raise HTTPException(status_code=404, detail="Province not found")
    return province
