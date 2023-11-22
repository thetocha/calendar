from enum import Enum

from pydantic import BaseModel
from uuid import UUID


class Group(BaseModel):
    id: UUID
    course: Enum
    number: int


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    group: Group


class GetUser(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    password: str

    class Config:
        from_attributes = True
