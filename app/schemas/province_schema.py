from pydantic import BaseModel
from uuid import UUID

class AssignProvinceRequest(BaseModel):
    province_id: UUID

