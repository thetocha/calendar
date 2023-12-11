from pydantic import BaseModel
from uuid import UUID

from app.users.models import CourseEnum


class CreateGroup(BaseModel):
    course: CourseEnum
    number: int


class GetGroup(CreateGroup):
    id: UUID

    class Config:
        from_attributes = True
