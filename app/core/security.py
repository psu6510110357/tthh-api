import datetime
from jose import jwt
from . import config
import bcrypt


ALGORITHM = "HS256"

settings = config.get_settings()

# Create access token with expiration by encoding the data
def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "sub": str(data.get("sub", 0))})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Create refresh token with expiration by encoding the data
def create_refresh_token(
    data: dict, expires_delta: datetime.timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "sub": str(data.get("sub", 0))})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Hash password using bcrypt
def get_encrypted_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt=bcrypt.gensalt()).decode(
        "utf-8"
    )

# Password encryption
def set_password(plain_password: str) -> str:
    return get_encrypted_password(plain_password)

# Verify password using bcrypt returns True if the password matches the hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
