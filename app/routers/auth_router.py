from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from sqlmodel import select
from typing import Annotated
import datetime

from ..core.config import get_settings
from ..core.database import get_session, AsyncSession
from ..core.security import create_access_token, create_refresh_token, verify_password
from ..models.user_model import DBUser
from ..models.token_model import Token


router = APIRouter(tags=["authentication"])

settings = get_settings()

# Define the authentication endpoint
@router.post(
    "/token",
)
async def authentication(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Token:
    print("form_data", form_data)
    print("form_data.password", form_data.password)  # Debug log
    print("form_data.password repr:", repr(form_data.password))  # Show exact chars
    print("form_data.password length:", len(form_data.password))  # Show length
    actual_password = form_data.password

    # Simplify user lookup by username or email
    result = await session.exec(
        select(DBUser).where(
            (DBUser.username == form_data.username)
            | (DBUser.email == form_data.username)
        )
    )
    user = result.one_or_none() # Get one user or None if not found

    print("user", user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # Verify password
    try:
        password_valid = verify_password(actual_password, user.password)
        print(f"Password verification result: {password_valid}")  # Debug log
    except Exception as e:
        print(f"Password verification error: {e}")  # Debug log
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password verification failed",
        )

    if not password_valid:
        print("Stored password:", user.password)  # Debug log
        print("Input password:", actual_password)  # Debug log
        print("Input password repr:", repr(actual_password))  # Debug log
        print("Input password length:", len(actual_password))  # Debug log

        # Let's also test the password manually here
        import bcrypt

        manual_check = bcrypt.checkpw(
            actual_password.encode("utf-8"), user.password.encode("utf-8")
        )
        print(f"Manual bcrypt check: {manual_check}")  # Debug log

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # Update last login date
    try:
        user.last_login_date = datetime.datetime.now()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(
            f"User last login updated successfully: {user.last_login_date}"
        )  # Debug log
    except Exception as e:
        print("Database commit failed:", e)  # Debug log
        await session.rollback()  # Explicitly rollback on error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    # Generate tokens
    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token_expires = datetime.timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    return Token(  # return Token object with access and refresh tokens
        access_token=create_access_token(
            data={"sub": str(user.id)}, 
            expires_delta=access_token_expires,
        ),
        refresh_token=create_refresh_token(
            data={"sub": str(user.id)},
            expires_delta=refresh_token_expires,
        ),
        token_type="Bearer",
        scope="",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expires_at=datetime.datetime.now() + access_token_expires,
        issued_at=user.last_login_date,
        user_id=user.id,
    )
