import datetime
import uuid
from pydantic import BaseModel
from sqlmodel import UUID, SQLModel, Field, Relationship
from typing import Optional, List
from ..models.user_model import DBUser


class Province(BaseModel):
    name: str = Field(unique=True, index=True, nullable=False)
    is_secondary: bool = Field(default=False)
    tax_reduction_info: Optional[str] = Field(default=None)


class DBProvince(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)

    users: List[DBUser] = Relationship(back_populates="province")
