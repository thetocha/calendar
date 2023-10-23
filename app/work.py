# from sqlalchemy.orm import Session
#
# from app import models, schemas
#
#
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#
#
# def create_user(db: Session, user: schemas.User):
#     db_user = models.User(Name=user.Name, Age=user.Age)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
