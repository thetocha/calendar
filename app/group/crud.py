from uuid import UUID
from sqlalchemy.orm import Session
from app.group.schemas import CreateGroup, GetGroup
from app.users.schemas import GetUser, GetUserGroupRole, CreateUserGroupRole
from app.users.models import Group, UserGroupRole, GroupRoleEnum


def create_group(group: CreateGroup, session: Session):
    new_db_group = Group(**group.dict())
    session.add(new_db_group)
    session.commit()
    return new_db_group


def get_group(group: CreateGroup, session: Session):
    return session.query(Group).filter(Group.number == group.number, Group.course == group.course).first()


def get_group_by_id(id: UUID, session):
    return session.query(Group).filter(Group.id == id).first()


def delete_group(group: GetGroup, session: Session):
    group_to_delete = get_group_by_id(group.id, session)
    session.delete(group_to_delete)
    session.commit()
    return group_to_delete


def add_user_to_group(user_group_role: CreateUserGroupRole, session: Session):
    new_user = UserGroupRole(**user_group_role.dict())
    session.add(new_user)
    session.commit()
    return user_group_role.dict()


def delete_user_from_group(user_group_role: GetUserGroupRole, session: Session):
    user_group_role_to_delete = session.query(UserGroupRole).filter(UserGroupRole.id == user_group_role.id).first()
    session.delete(user_group_role_to_delete)
    session.commit()
    return user_group_role_to_delete


def get_user_group_role(user: GetUser, session: Session) -> GetUserGroupRole:
    return session.query(UserGroupRole).filter(UserGroupRole.user_id == user.id).first()


def get_user_group(user: GetUser, session: Session):
    user_group_role = get_user_group_role(user, session)
    return session.query(Group).filter(Group.id == user_group_role.group.id).first()


def update_role(user: GetUser, role: GroupRoleEnum, session: Session):
    update_query = session.query(UserGroupRole).filter(UserGroupRole.user_id == user.id)
    user_group_role = update_query.first()
    if not user_group_role:
        return None
    new_data = {
        "user_id": user.id,
        "group_id": user_group_role.group_id,
        "role": role
    }
    update_query.update(new_data)
    session.commit()
    return new_data
