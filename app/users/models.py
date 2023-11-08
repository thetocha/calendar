import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), index=True)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    group = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))

    roles = relationship("Role", back_populates="roles")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(20), nullable=False)

    users = relationship("User", back_populates="roles")


