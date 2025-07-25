import datetime
import uuid
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional

# Define the Province model with necessary fields
class Province(BaseModel):
    name: str = Field(unique=True, index=True, nullable=False)
    is_secondary: bool = Field(default=False)
    tax_reduction_info: Optional[str] = Field(default=None)

# Define the database model for Province
class DBProvince(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True)
    is_secondary: bool = Field(default=False)
    tax_reduction_info: str
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
