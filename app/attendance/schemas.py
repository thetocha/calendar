from pydantic import BaseModel
from uuid import UUID


class CreateAttendance(BaseModel):
    user: UUID
    event: UUID
    attended: bool
    promised: bool


class GetAttendance(CreateAttendance):
    id: UUID

    class Config:
        from_attributes = True
