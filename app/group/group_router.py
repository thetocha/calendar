from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.group.crud import get_group, create_group, get_user_group_role, add_user_to_group, \
    delete_user_from_group, delete_group, update_role
from app.database import get_session
from app.users.schemas import GetUser, CreateUserGroupRole
from app.users.models import GroupRoleEnum
from app.auth.token_handler import get_current_user_details
from app.group.schemas import CreateGroup, GetGroup
from app.users.crud import get_user_by_username

group_router = APIRouter(tags=["Group"])


@group_router.post("/create_group", response_model=CreateGroup)
def create_group_endpoint(group: CreateGroup, session: Session = Depends(get_session)):
    db_group = get_group(group, session)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already registered")
    return create_group(group, session)


@group_router.delete("/delete_group")
def delete_group_endpoint(group: GetGroup, session: Session = Depends(get_session)):
    return delete_group(group, session)


@group_router.put("/join_group")
def add_user_to_group_endpoint(group: GetGroup, role: GroupRoleEnum, session: Session = Depends(get_session),
                               user: GetUser = Depends(get_current_user_details)):
    if get_user_group_role(user, session):
        raise HTTPException(status_code=400, detail="User already belong to group")
    if not get_group(group, session):
        raise HTTPException(status_code=404, detail="No such group")

    user_group_role = {
        "user_id": user.id,
        "group_id": group.id,
        "role": role
    }
    return add_user_to_group(CreateUserGroupRole(**user_group_role), session)


@group_router.delete("/leave_group")
def delete_user_from_group_endpoint(user: GetUser = Depends(get_current_user_details),
                                    session: Session = Depends(get_session)):
    user_group_role = get_user_group_role(user, session)
    if not user_group_role:
        raise HTTPException(status_code=400, detail="User does not belong to any group")
    return delete_user_from_group(user_group_role, session)


@group_router.put("/assign_new_group_role_to_user")
def update_group_role_endpoint(username: str, new_role: GroupRoleEnum, session: Session = Depends(get_session)):
    user = get_user_by_username(username=username, session=session)
    user_group_role = get_user_group_role(user, session)
    if not user_group_role:
        raise HTTPException(status_code=400, detail="User does not belong to any group")
    return update_role(user=user, role=new_role, session=session)
