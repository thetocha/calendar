from fastapi import FastAPI
from app.users.user_router import user_router
from app.auth.auth_router import auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello Start Point!"}
