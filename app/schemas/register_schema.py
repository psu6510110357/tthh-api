from pydantic import BaseModel, ConfigDict
from ..utils.to_camel_case import to_camel_case


class RegisterUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str  # Added password field

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )
