import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.utils.to_camel_case import to_camel_case


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime
    user_id: UUID

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )
