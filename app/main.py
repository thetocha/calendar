from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session
#
# from app import work, models, schemas
# from .database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@app.get("/")
def simple_get():
    return {"Hello": "There"}


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.User, db: Session = Depends(get_db)):
#     db_user = work.get_user(db, user_id=user.id)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return work.create_user(db=db, user=user)
#
#
# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = work.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = work.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
