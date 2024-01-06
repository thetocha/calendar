from sqlalchemy import extract

from app.event.schemas import CreateEvent, GetEvent, GetEventGroup
from app.users.models import Event, EventGroup
from app.group.schemas import GetGroup
from app.database import get_session
from uuid import UUID


class EventCrud:
    def __init__(self, session):
        if session:
            self.session = session
        else:
            self.session = next(get_session())

    def create_event(self, event: CreateEvent):
        new_event = Event(**event.dict())
        self.session.add(new_event)
        self.session.commit()
        return new_event

    def get_event_by_id(self, id: UUID):
        return self.session.query(Event).filter(Event.id == id).first()

    def get_event_by_description(self, event: CreateEvent):
        return self.session.query(Event).filter(Event.week == event.week, Event.weekday == event.weekday,
                                                Event.professor == event.professor).first()

    def delete_event(self, event: GetEvent):
        event_to_delete = self.get_event_by_id(event.id)
        self.session.delete(event_to_delete)
        self.session.commit()
        return event_to_delete

    def update_event(self, event: GetEvent):
        update_query = self.session.query(Event).filter(Event.id == event.id)
        event_to_update = update_query.first()
        if event_to_update is None:
            return None
        update_query.update(event.dict())
        self.session.commit()
        return event

    def get_event(self, event: GetEvent):
        return self.get_event_by_id(event.id)

    def get_events(self, skip: int = 0, limit: int = 100):
        return self.session.query(Event).offset(skip).limit(limit).all()

    def add_event_to_group(self, group: GetGroup, event: GetEvent):
        data = {
            "group": group.id,
            "event": event.id
        }
        event_group = EventGroup(**data)
        self.session.add(event_group)
        self.session.commit()
        return data

    def get_group_event(self, event: GetEvent, group: GetGroup):
        return self.session.query(EventGroup).filter(EventGroup.group == group.id, EventGroup.event == event.id).first()

    def delete_group_from_event(self, event_group: GetEventGroup):
        event_group_to_delete = self.session.query(EventGroup).filter(EventGroup.id == event_group.id).first()
        self.session.delete(event_group_to_delete)
        self.session.commit()
        return event_group_to_delete

    def get_all_group_events(self, group_id: UUID):
        return self.session.query(EventGroup).filter(EventGroup.group == group_id).all()

    def get_all_group_events_for_month(self, group_id: UUID, month: int, year: int):
        events = []
        group_events = self.get_all_group_events(group_id)
        for group_event in group_events:
            event = self.session.query(Event).filter(Event.id == group_event.event).filter(
                extract('month', Event.date) == month).filter(extract('year', Event.date) == year).first()
            if event:
                events.append(event)
        return events
