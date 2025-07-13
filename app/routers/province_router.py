from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


from app.schemas.province_schema import ProvinceListResponse
from ..models.province_model import DBProvince
from ..core.database import get_session
from ..core.deps import get_current_user

router = APIRouter(tags=["province"])


@router.get("/", response_model=ProvinceListResponse)
async def read_all_provinces(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    result = await session.exec(select(DBProvince))
    provinces = result.all()
    return {"provinces": provinces}
