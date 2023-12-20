from sqlalchemy.orm import Session
from app.users.models import User
from app.users.schemas import CreateUser

from uuid import UUID


class UserCrud:

    def __init__(self, session: Session):
        self.session = session

    def get_user_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def get_user(self, user_id: UUID):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.session.query(User).offset(skip).limit(limit).all()

    def delete_user(self, id: UUID):
        user_to_delete = self.get_user(id)
        self.session.delete(user_to_delete)
        self.session.commit()
        return user_to_delete

    def create_user(self, user: CreateUser):
        user_to_add = User(**user.dict())
        self.session.add(user_to_add)
        self.session.commit()
        return user_to_add

    def update_user(self, user: CreateUser, id_to_update: UUID):
        update_query = self.session.query(User).filter(User.id == id_to_update)
        user_to_update = update_query.first()
        if user_to_update is None:
            return None
        info = {"id": user_to_update.id}
        info.update(**user.dict())
        update_query.update(info)
        self.session.commit()
        return user_to_update
