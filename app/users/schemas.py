from pydantic import BaseModel
from uuid import UUID

from app.group.schemas import CreateGroup


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    group: CreateGroup


class GetUser(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    password: str

    class Config:
        from_attributes = True
