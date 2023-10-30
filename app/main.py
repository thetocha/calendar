from fastapi import FastAPI
from .users.user_router import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello Start Point!"}
