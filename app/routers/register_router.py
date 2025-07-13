from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.user_model import DBUser
from ..models.province_model import DBProvince
from ..core.database import get_session
from ..core.security import get_encrypted_password
from ..schemas.user_schema import RegisterUser, UserResponse
import uuid

router = APIRouter(tags=["registration"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: RegisterUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserResponse:
    # Check if username already exists
    result = await session.exec(select(DBUser).where(DBUser.username == user.username))
    existing_user_by_username = result.first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )

    # Check if email already exists
    result = await session.exec(select(DBUser).where(DBUser.email == user.email))
    existing_user_by_email = result.first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    # Check if province exists
    province = await session.get(DBProvince, user.province_id)
    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province not found",
        )

    # Hash the password before storing
    hashed_password = get_encrypted_password(user.password)

    db_user = DBUser(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password,  # Store hashed password
        id=uuid.uuid4(),  # Generate UUID
        province_id=user.province_id,  # Assign province
    )

    # Save user to the database
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    # Return the created user
    return UserResponse(
        id=str(db_user.id),
        username=db_user.username,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        province_id=str(db_user.province_id),
    )
