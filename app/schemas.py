from pydantic import BaseModel


class UserBase(BaseModel):
    Name: str
    LastName: str


class User(UserBase):
    login: str
    id: int
    password: int
    group: int

    class Config:
        from_attributes = True
