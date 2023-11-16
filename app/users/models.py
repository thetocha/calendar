import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from enum import Enum

from app.database import Base


class CourseEnum(Enum):
    first = "First"
    second = "Second"
    third = "Third"
    forth = "Forth"


class WeekDayEnum(Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"


class WeekEnum(Enum):
    odd = "Odd"
    even = "Even"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(1000), nullable=False)
    group_role = Column(Integer, ForeignKey("user_group_roles.id"))
    user_role = Column(Integer, ForeignKey("user_roles.id"))

    user_roles = relationship("UserRole", back_populates="users")
    user_group_roles = relationship("UserGroupRole", back_populates="users")
    notifications = relationship("Notification", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(20), nullable=False)

    user_roles = relationship("User", back_populates="roles")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    users = relationship("User", back_populates="user_roles")
    roles = relationship("Role", back_populates="user_roles")


class GroupRole(Base):
    __tablename__ = "group_roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), nullable=False)

    user_group_roles = relationship("UserGroupRole", back_populates="group_roles")


class UserGroupRole(Base):
    __tablename__ = "user_group_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    group_id = Column(UUID, ForeignKey("groups.id"))
    role_id = Column(Integer, ForeignKey("group_roles.id"))

    groups = relationship("Group", back_populates="group_roles")
    group_roles = relationship("GroupRole", back_populates="user_group_roles")
    users = relationship("User", back_populates="user_group_roles")


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), index=True)
    number = Column(Integer, nullable=False)
    course = Column(ENUM(CourseEnum), nullable=False)

    group_roles = relationship("UserGroupRole", back_populates="groups")
    group_events = relationship("EventGroup", back_populates="groups")


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), index=True)
    professor = Column(String(30))
    place = Column(String(20))
    week = Column(ENUM(WeekEnum), nullable=False)
    weekday = Column(ENUM(WeekDayEnum), nullable=False)

    event_groups = relationship("EventGroup", back_populates="events")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), index=True)
    user = Column(UUID, ForeignKey("users.id"))
    event = Column(UUID, ForeignKey("events.id"))
    attended = Column(Boolean)
    promised = Column(Boolean)

    users = relationship("User", back_populates="attendance")
    events = relationship("Event", back_populates="attendance")


class EventGroup(Base):
    __tablename__ = "event_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), index=True)
    group = Column(UUID, ForeignKey("groups.id"))
    event = Column(UUID, ForeignKey("events.id"))

    groups = relationship("Group", back_populates="group_events")
    events = relationship("Event", back_populates="event_groups")


class StatusEnum(Enum):
    sent = "Sent"
    not_sent = "Not Sent"
    error = "Error"
    sending = "Sending"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), index=True)
    text = Column(String(1000), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    status = Column(ENUM(StatusEnum), nullable=False)
    user = Column(UUID, ForeignKey("users.id"))

    users = relationship("User", back_populates="notifications")
