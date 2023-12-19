import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.types import TIME
from enum import Enum

from app.database import Base


class CourseEnum(str, Enum):
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"
    FORTH = "forth"


class WeekDayEnum(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class WeekEnum(str, Enum):
    ODD = "odd"
    EVEN = "even"


class RoleEnum(str, Enum):
    ADMINISTRATOR = "administrator"
    MANAGER = "manager"
    DEFAULT_USER = "default_user"


class GroupRoleEnum(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    DEFAULT_STUDENT = "default_student"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(1000), nullable=False)
    role = Column(ENUM(RoleEnum), nullable=False)

    # user_roles = relationship("UserRole", back_populates="general_users")
    user_group_roles = relationship("UserGroupRole", back_populates="users")
    notifications = relationship("Notification", back_populates="users")
    attendance = relationship("Attendance", back_populates="users")


# class UserRole(Base):
#     __tablename__ = "user_roles"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(UUID, ForeignKey("users.id"))
#     role = Column(ENUM(RoleEnum), nullable=False)
#
#     general_users = relationship("User", back_populates="user_roles", foreign_keys="UserRole.user_id")


class UserGroupRole(Base):
    __tablename__ = "user_group_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    group_id = Column(UUID, ForeignKey("groups.id"))
    role = Column(ENUM(GroupRoleEnum), nullable=False)

    groups = relationship("Group", back_populates="group_roles", foreign_keys="UserGroupRole.group_id")
    users = relationship("User", back_populates="user_group_roles", foreign_keys="UserGroupRole.user_id")


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    number = Column(Integer, nullable=False)
    course = Column(ENUM(CourseEnum), nullable=False)

    group_roles = relationship("UserGroupRole", back_populates="groups")
    group_events = relationship("EventGroup", back_populates="groups")


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    professor = Column(String(30))
    place = Column(String(20))
    week = Column(ENUM(WeekEnum), nullable=False)
    weekday = Column(ENUM(WeekDayEnum), nullable=False)
    time = Column(TIME, nullable=False)

    event_groups = relationship("EventGroup", back_populates="events")
    attendance = relationship("Attendance", back_populates="events")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user = Column(UUID, ForeignKey("users.id"))
    event = Column(UUID, ForeignKey("events.id"))
    attended = Column(Boolean)
    promised = Column(Boolean)

    users = relationship("User", back_populates="attendance", foreign_keys="Attendance.user")
    events = relationship("Event", back_populates="attendance", foreign_keys="Attendance.event")


class EventGroup(Base):
    __tablename__ = "event_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    group = Column(UUID, ForeignKey("groups.id"))
    event = Column(UUID, ForeignKey("events.id"))

    groups = relationship("Group", back_populates="group_events", foreign_keys="EventGroup.group")
    events = relationship("Event", back_populates="event_groups", foreign_keys="EventGroup.event")


class StatusEnum(Enum):
    SENT = "Sent"
    NOT_SENT = "Not Sent"
    ERROR = "Error"
    SENDING = "Sending"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    text = Column(String(1000), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    status = Column(ENUM(StatusEnum), nullable=False)
    user = Column(UUID, ForeignKey("users.id"))

    users = relationship("User", back_populates="notifications")
