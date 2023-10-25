from fastapi import FastAPI, Depends
from .users import user_router

app = FastAPI()

app.include_router(user_router.router)


@app.get("/")
async def root():
    return {"message": "Hello Start Point!"}
