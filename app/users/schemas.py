from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    last_name: str


class User(UserBase):
    user_name: str
    id: int
    password: int
    group: int

    class Config:
        from_attributes = True
