from uuid import UUID
from app.group.schemas import CreateGroup, GetGroup
from app.users.schemas import GetUser, GetUserGroupRole, CreateUserGroupRole
from app.users.models import Group, UserGroupRole, GroupRoleEnum


class GroupCrud:
    def __init__(self, session):
        self.session = session

    def create_group(self, group: CreateGroup):
        new_db_group = Group(**group.dict())
        self.session.add(new_db_group)
        self.session.commit()
        return new_db_group

    def get_group(self, group: CreateGroup):
        return self.session.query(Group).filter(Group.number == group.number, Group.course == group.course).first()

    def get_group_by_id(self, id: UUID):
        return self.session.query(Group).filter(Group.id == id).first()

    def get_all_groups(self, skip: int = 0, limit: int = 100):
        return self.session.query(Group).offset(skip).limit(limit).all()

    def delete_group(self, group: GetGroup):
        group_to_delete = self.get_group_by_id(group.id)
        self.session.delete(group_to_delete)
        self.session.commit()
        return group_to_delete

    def add_user_to_group(self, user_group_role: CreateUserGroupRole):
        new_user = UserGroupRole(**user_group_role.dict())
        self.session.add(new_user)
        self.session.commit()
        return user_group_role.dict()

    def delete_user_from_group(self, user_group_role: GetUserGroupRole):
        user_group_role_to_delete = self.session.query(UserGroupRole)\
            .filter(UserGroupRole.id == user_group_role.id).first()
        self.session.delete(user_group_role_to_delete)
        self.session.commit()
        return user_group_role_to_delete

    def get_user_group_role(self, user: GetUser) -> GetUserGroupRole:
        return self.session.query(UserGroupRole).filter(UserGroupRole.user_id == user.id).first()

    def get_user_group(self, user: GetUser):
        user_group_role = self.get_user_group_role(user)
        return self.session.query(Group).filter(Group.id == user_group_role.group.id).first()

    def update_role(self, user: GetUser, role: GroupRoleEnum):
        update_query = self.session.query(UserGroupRole).filter(UserGroupRole.user_id == user.id)
        user_group_role = update_query.first()
        if not user_group_role:
            return None
        new_data = {
            "user_id": user.id,
            "group_id": user_group_role.group_id,
            "role": role
        }
        update_query.update(new_data)
        self.session.commit()
        return new_data
