import datetime
from uuid import UUID
import uuid
from typing import Optional

import pydantic
from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel, Field, Relationship

from ..models.province_model import DBProvince


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    email: str = pydantic.Field(json_schema_extra=dict(example="admin@email.local"))
    username: str = pydantic.Field(json_schema_extra=dict(example="admin"))
    first_name: str = pydantic.Field(json_schema_extra=dict(example="Firstname"))
    last_name: str = pydantic.Field(json_schema_extra=dict(example="Lastname"))


class User(BaseUser):
    id: UUID
    last_login_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )
    register_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )
    province_id: Optional[UUID] = None
    password: str = ""


class DBUser(BaseUser, SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    password: str

    register_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_login_date: datetime.datetime | None = Field(default=None)
    status: str = Field(default="active")

    province_id: Optional[UUID] = Field(default=None, foreign_key="dbprovince.id")
    province: Optional[DBProvince] = Relationship(back_populates="users")
