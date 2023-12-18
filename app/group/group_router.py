from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.group.crud import GroupCrud
from app.database import get_session
from app.users.schemas import GetUser, CreateUserGroupRole
from app.users.models import GroupRoleEnum
from app.auth.token_handler import get_current_user_details
from app.group.schemas import CreateGroup, GetGroup
from app.users.crud import get_user_by_username

group_router = APIRouter(tags=["Group"])


@group_router.post("/create_group", response_model=CreateGroup)
def create_group_endpoint(group: CreateGroup, session: Session = Depends(get_session)):
    crud = GroupCrud(session)
    db_group = crud.get_group(group)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already registered")
    return crud.create_group(group)


@group_router.get("/get_group/{group_id}")
def get_group_endpoint(group_id: UUID, session: Session = Depends(get_session)):
    crud = GroupCrud(session)
    return crud.get_group_by_id(group_id)


@group_router.get("/get_all_groups")
def get_all_groups_endpoint(session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    crud = GroupCrud(session)
    return crud.get_all_groups(skip, limit)


@group_router.delete("/delete_group")
def delete_group_endpoint(group: GetGroup, session: Session = Depends(get_session)):
    crud = GroupCrud(session)
    return crud.delete_group(group)


@group_router.put("/join_group")
def add_user_to_group_endpoint(group: GetGroup, role: GroupRoleEnum, session: Session = Depends(get_session),
                               user: GetUser = Depends(get_current_user_details)):
    crud = GroupCrud(session)
    if crud.get_user_group_role(user):
        raise HTTPException(status_code=400, detail="User already belong to group")
    if not crud.get_group(group):
        raise HTTPException(status_code=404, detail="No such group")

    user_group_role = {
        "user_id": user.id,
        "group_id": group.id,
        "role": role
    }
    return crud.add_user_to_group(CreateUserGroupRole(**user_group_role))


@group_router.delete("/leave_group")
def delete_user_from_group_endpoint(user: GetUser = Depends(get_current_user_details),
                                    session: Session = Depends(get_session)):
    crud = GroupCrud(session)
    user_group_role = crud.get_user_group_role(user)
    if not user_group_role:
        raise HTTPException(status_code=400, detail="User does not belong to any group")
    return crud.delete_user_from_group(user_group_role)


@group_router.put("/assign_new_group_role_to_user")
def update_group_role_endpoint(username: str, new_role: GroupRoleEnum, session: Session = Depends(get_session)):
    user = get_user_by_username(username=username, session=session)
    crud = GroupCrud(session)
    user_group_role = crud.get_user_group_role(user)
    if not user_group_role:
        raise HTTPException(status_code=400, detail="User does not belong to any group")
    return crud.update_role(user=user, role=new_role)
