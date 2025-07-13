from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List
from ..models.province_model import DBProvince
from ..core.database import get_session

router = APIRouter(tags=["province"])


@router.get("/", response_model=List[DBProvince])
async def read_all_provinces(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(DBProvince))
    provinces = result.all()
    return provinces


