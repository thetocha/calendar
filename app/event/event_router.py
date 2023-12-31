from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from uuid import UUID

from app.event.schemas import CreateEvent, GetEvent
from app.group.schemas import GetGroup
from app.event.crud import EventCrud
from app.group.crud import GroupCrud
from app.attendance.schemas import CreateAttendance
from app.attendance.attendance_router import create_attendance, get_user_event_attendance, delete_attendance
from app.group.group_router import get_all_group_users
from app.auth.token_handler import verify_is_not_default_user, verify_is_administrator

event_router = APIRouter(tags=["Event"])


def create_users_attendance(users: list, event_id: UUID, session: Session):
    for user in users:
        info = {
            "user": user.user_id,
            "event": event_id
        }
        attendance = CreateAttendance(**info)
        create_attendance(attendance, session=session)


def delete_users_attendance(users: list, event_id: UUID, session: Session):
    for user in users:
        attendance = get_user_event_attendance(user=user.user_id, event=event_id, session=session)
        delete_attendance(attendance, session=session)


@event_router.post("/create_event", response_model=CreateEvent, dependencies=[Depends(verify_is_administrator)])
def create_event_endpoint(event: CreateEvent, session: Session = Depends(get_session)):
    crud = EventCrud(session)
    db_event = crud.get_event_by_description(event)
    if db_event:
        raise HTTPException(status_code=400, detail="Such event already exist")
    return crud.create_event(event)


@event_router.delete("/delete_event", dependencies=[Depends(verify_is_administrator)])
def delete_event_endpoint(event: GetEvent, session: Session = Depends(get_session)):
    crud = EventCrud(session)
    db_event = crud.get_event_by_id(event.id)
    if not db_event:
        raise HTTPException(status_code=404, detail="No such event")
    return crud.delete_event(event)


@event_router.put("/update_event", dependencies=[Depends(verify_is_administrator)])
def update_event_endpoint(event: GetEvent, session: Session = Depends(get_session)):
    crud = EventCrud(session)
    if not crud.get_event_by_id(event.id):
        HTTPException(status_code=404, detail="No such event")
    return crud.update_event(event)


@event_router.get("/get_event/{event_id}")
def get_event_endpoint(event_id: UUID, session: Session = Depends(get_session)):
    crud = EventCrud(session)
    db_event = crud.get_event_by_id(event_id)
    if not db_event:
        HTTPException(status_code=404, detail="No such event")
    return db_event


@event_router.get("/get_all_events", response_model=list[GetEvent])
def get_all_event_endpoint(session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    crud = EventCrud(session)
    return crud.get_events(skip, limit)


@event_router.post("/add_event_to_groups", dependencies=[Depends(verify_is_not_default_user)])
def add_event_to_groups_endpoint(groups: list[GetGroup], event: GetEvent, session: Session = Depends(get_session)):
    event_crud = EventCrud(session)
    result = []
    group_crud = GroupCrud(session)
    if not event_crud.get_event_by_id(event.id):
        HTTPException(status_code=404, detail="No such event")
    for group in groups:
        if not group_crud.get_group_by_id(group.id):
            HTTPException(status_code=404, detail="No such group")
        result.append(event_crud.add_event_to_group(group, event))
        users = get_all_group_users(group.id, session=session)
        create_users_attendance(users, event.id, session)
    return result


@event_router.delete("/delete_groups_from_event", dependencies=[Depends(verify_is_not_default_user)])
def delete_groups_from_event_endpoint(groups: list[GetGroup], event: GetEvent, session: Session = Depends(get_session)):
    crud = EventCrud(session)
    result = []
    users = []
    for group in groups:
        db_group_event = crud.get_group_event(group=group, event=event)
        if not db_group_event:
            raise HTTPException(status_code=404, detail="No such group event")
        users.append(get_all_group_users(group.id, session=session))
        result.append(crud.delete_group_from_event(db_group_event))
    delete_users_attendance(users, event.id, session)
    return result


@event_router.get("/get_all_events_of_group/{group_id}")
def get_all_events_of_group_endpoint(group_id: UUID, session: Session = Depends(get_session)):
    event_crud = EventCrud(session)
    group_crud = GroupCrud(session)
    if not group_crud.get_group_by_id(group_id):
        HTTPException(status_code=404, detail="No such group")
    return event_crud.get_all_group_events(group_id)


@event_router.post("/add_events_to_group", dependencies=[Depends(verify_is_not_default_user)])
def add_events_to_group_endpoint(group: GetGroup, events: list[GetEvent], session: Session = Depends(get_session)):
    crud = EventCrud(session)
    result = []
    users = get_all_group_users(group.id, session=session)
    for event in events:
        if crud.get_group_event(event=event, group=group):
            raise HTTPException(status_code=400, detail="This group already registered for this event")
        result.append(crud.add_event_to_group(group, event))
        create_users_attendance(users, event.id, session)
    return result


@event_router.delete("/delete_group_events", dependencies=[Depends(verify_is_not_default_user)])
def delete_group_events_endpoint(group: GetGroup, events: list[GetEvent], session: Session = Depends(get_session)):
    crud = EventCrud(session)
    result = []
    users = get_all_group_users(group.id, session=session)
    for event in events:
        db_group_event = crud.get_group_event(event, group)
        if not db_group_event:
            raise HTTPException(status_code=404, detail="No such group event")
        delete_users_attendance(users, event.id, session)
        result.append(crud.delete_group_from_event(db_group_event))
    return result
