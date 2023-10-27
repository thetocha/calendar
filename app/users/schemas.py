from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    name: str
    last_name: str


class GetUser(UserBase):
    user_name: str
    id: UUID
    group: int

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    user_name: str
    password: int
    group: int

    class Config:
        from_attributes = True
