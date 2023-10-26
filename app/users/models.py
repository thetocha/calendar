import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), index=True)
    name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    user_name = Column(String(100), nullable=False, unique=True)
    password = Column(Integer, nullable=False)
    group = Column(Integer, nullable=False)
