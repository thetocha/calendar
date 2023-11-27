from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.group.crud import get_group, create_group, get_user_group_role, add_user_to_group
from app.database import get_session
from app.users.schemas import GetUser
from app.auth.token_handler import get_current_user_details
from app.group.schemas import CreateGroup, GetGroup, GetGroupRole, CreateUserGroupRole

group_router = APIRouter(tags=["Group"])


@group_router.post("/create_group", response_model=CreateGroup)
def create_group(group: CreateGroup, session: Session = Depends(get_session)):
    db_group = get_group(group, session)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already registered")
    return create_group(group, session)


@group_router.put("/join_group")
def add_user_to_group(group: GetGroup, role: GetGroupRole, session: Session = Depends(get_session),
                      user: GetUser = Depends(get_current_user_details)):
    if get_user_group_role(user, session):
        raise HTTPException(status_code=400, detail="User already belong to group")
    data = group.dict
    data.update(role.dict)
    data.update(user.dict)
    user_group_role = CreateUserGroupRole(data)
    return add_user_to_group(user_group_role)
