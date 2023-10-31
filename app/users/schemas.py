from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    group: int


class GetUser(UserBase):
    id: UUID

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    password: str

    class Config:
        from_attributes = True
