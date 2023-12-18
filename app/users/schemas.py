from enum import Enum

from pydantic import BaseModel
from uuid import UUID

from app.group.schemas import CreateGroup
from app.users.models import GroupRoleEnum, RoleEnum


class Group(BaseModel):
    id: UUID
    course: Enum
    number: int


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    role: RoleEnum


class GetUser(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    password: str

    class Config:
        from_attributes = True


class CreateUserGroupRole(BaseModel):
    user_id: UUID
    group_id: UUID
    role: GroupRoleEnum

    class Config:
        from_attributes = True


class GetUserGroupRole(CreateGroup):
    id: int

    class Config:
        from_attributes = True
