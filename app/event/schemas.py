from app.users.models import WeekEnum, WeekDayEnum
from pydantic import BaseModel
from uuid import UUID
from datetime import time, datetime


class CreateEvent(BaseModel):
    professor: str
    place: str
    name: str
    week: WeekEnum
    weekday: WeekDayEnum
    time: time
    date: datetime


class GetEvent(CreateEvent):
    id: UUID

    class Config:
        from_attributes = True


class CreateEventGroup(BaseModel):
    group: UUID
    event: UUID


class GetEventGroup(CreateEventGroup):
    id: UUID
