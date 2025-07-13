from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.utils.to_camel_case import to_camel_case


class AssignProvinceRequest(BaseModel):
    province_id: UUID

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )


class ProvinceResponse(BaseModel):
    id: UUID
    name: str
    is_secondary: bool
    tax_reduction_info: str | None
    created_date: datetime
    updated_date: datetime

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )


class ProvinceListResponse(BaseModel):
    provinces: List[ProvinceResponse]


class MyProvinceResponse(BaseModel):
    id: UUID
    name: str
    is_secondary: bool
    tax_reduction_info: str | None
    created_date: datetime
    updated_date: datetime

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )
