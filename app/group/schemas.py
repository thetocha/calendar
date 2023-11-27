from pydantic import BaseModel
from uuid import UUID
from enum import Enum

from app.users.schemas import GetUser


class CreateGroup(BaseModel):
    course: Enum
    number: int


class GetGroup(CreateGroup):
    id: UUID

    class Config:
        from_attributes = True


class GetGroupRole(BaseModel):
    id: int
    role_name: str


class CreateUserGroupRole(BaseModel):
    user: GetUser
    group: GetGroup
    role: GetGroupRole

    class Config:
        from_attributes = True


class GetUserGroupRole(CreateGroup):
    id: int

    class Config:
        from_attributes = True
