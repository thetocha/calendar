from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    first_name: str
    last_name: str


class GetUser(UserBase):
    username: str
    id: UUID
    group: int

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    username: str
    password: str
    group: int

    class Config:
        from_attributes = True
