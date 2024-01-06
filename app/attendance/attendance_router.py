from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.orm import Session

from app.attendance.schemas import GetAttendance, CreateAttendance
from app.users.models import RoleEnum, GroupRoleEnum
from app.users.schemas import GetUser
from app.attendance.crud import AttendanceCrud
from app.auth.token_handler import get_current_user_group, get_current_user_details, verify_is_administrator, \
    get_current_user_role, get_current_user_group_role
from app.users.crud import UserCrud
from app.event.crud import EventCrud
from app.group.crud import GroupCrud
from app.database import get_session

attendance_router = APIRouter(tags=["Attendance"])


@attendance_router.post("/create_attendance")
def create_attendance(attendance: CreateAttendance, session: Session = Depends(get_session)):
    user_crud = UserCrud(session)
    event_crud = EventCrud(session)
    attendance_crud = AttendanceCrud(session)
    if not user_crud.get_user(attendance.user):
        raise HTTPException(status_code=404, detail="User not found")
    if not event_crud.get_event_by_id(attendance.event):
        raise HTTPException(status_code=404, detail="Event not found")
    db_attendance = attendance_crud.get_attendance(attendance)
    if db_attendance:
        raise HTTPException(status_code=400, detail="Such attendance already exist")
    return attendance_crud.create_attendance(attendance)


@attendance_router.get("/get_attendance/{attendance_id}")
def get_attendance(attendance_id: UUID, session: Session = Depends(get_session)):
    crud = AttendanceCrud(session)
    db_attendance = crud.get_attendance_by_id(attendance_id)
    if not db_attendance:
        raise HTTPException(status_code=404, detail="No such attendance")
    return db_attendance


@attendance_router.delete("/delete_attendance", dependencies=[Depends(verify_is_administrator)])
def delete_attendance(attendance: GetAttendance, session: Session = Depends(get_session)):
    crud = AttendanceCrud(session)
    db_attendance = crud.get_attendance(attendance)
    if not db_attendance:
        raise HTTPException(status_code=404, detail="No such attendance")
    return crud.delete_attendance(attendance)


@attendance_router.put("/update_attendance")
def update_attendance(attendance: CreateAttendance, id_to_update: UUID, session: Session = Depends(get_session),
                      role: RoleEnum = Depends(get_current_user_role),
                      group_role: GroupRoleEnum = Depends(get_current_user_group_role),
                      current_user_group: UUID = Depends(get_current_user_group)):
    group_crud = GroupCrud(session)
    updated_user_group = group_crud.get_user_group_by_id(attendance.user)
    if role is RoleEnum.DEFAULT_USER and \
            (group_role is GroupRoleEnum.DEFAULT_STUDENT or updated_user_group != current_user_group):
        raise HTTPException(status_code=403, detail="You have no rights for this")
    crud = AttendanceCrud(session)
    db_attendance = crud.get_attendance_by_id(id_to_update)
    if not db_attendance:
        raise HTTPException(status_code=404, detail="No such attendance")
    return crud.update_attendance(attendance, id_to_update)


@attendance_router.put("/update_attendance_promised")
def update_attendance_promised(id_to_update: UUID, new_promised: bool, session: Session = Depends(get_session),
                               user: GetUser = Depends(get_current_user_details)):
    attendance_crud = AttendanceCrud(session)
    attendance = attendance_crud.get_attendance_by_id(id_to_update)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance no found")
    if attendance.user != user.id:
        raise HTTPException(status_code=403, detail="You have no rights for this")
    return attendance_crud.update_promised(attendance_id=id_to_update, new_promised=new_promised)


@attendance_router.get("/get_user_attendance/{user_id}")
def get_user_attendance(user_id: UUID, session: Session = Depends(get_session)):
    user_crud = UserCrud(session)
    attendance_crud = AttendanceCrud(session)
    if not user_crud.get_user(user_id):
        raise HTTPException(status_code=404, detail="No such user")
    return attendance_crud.get_user_attendance(user_id)


@attendance_router.get("/get_event_attendance")
def get_event_attendance(event_id: UUID, session: Session = Depends(get_session)):
    event_crud = EventCrud(session)
    attendance_crud = AttendanceCrud(session)
    if not event_crud.get_event_by_id(event_id):
        raise HTTPException(status_code=404, detail="No such event")
    return attendance_crud.get_event_attendance(event_id)


@attendance_router.get("/get_user_event_attendance")
def get_user_event_attendance(event: UUID, user: UUID, session: Session = Depends(get_session)):
    attendance_crud = AttendanceCrud(session)
    user_crud = UserCrud(session)
    event_crud = EventCrud(session)
    if not event_crud.get_event_by_id(event):
        raise HTTPException(status_code=404, detail="No such event")
    if not user_crud.get_user(user):
        raise HTTPException(status_code=404, detail="No such user")
    return attendance_crud.get_user_event_attendance(user, event)


@attendance_router.get("/get_group_attendance/{group_id}")
def get_group_attendance(group_id: UUID, session: Session = Depends(get_session)):
    group_crud = GroupCrud(session)
    if not group_crud.get_group_by_id(group_id):
        raise HTTPException(status_code=404, detail="No such group")
    users = group_crud.get_all_group_user(group_id)
    result = []
    attendance_crud = AttendanceCrud(session)
    for user in users:
        result.append(attendance_crud.get_user_attendance(user.user_id))
    return result
