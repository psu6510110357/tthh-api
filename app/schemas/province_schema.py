from pydantic import BaseModel
from uuid import UUID

class AssignProvinceRequest(BaseModel):
    user_id: UUID
    province_id: UUID

