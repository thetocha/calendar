from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    LastName = Column(String)
    login = Column(String)
    password = Column(Integer)
    group = Column(Integer)
