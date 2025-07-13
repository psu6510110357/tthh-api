from pydantic import BaseModel, ConfigDict
from uuid import UUID

from ..utils.to_camel_case import to_camel_case


class RegisterUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    province_id: UUID

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    province_id: str

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )
