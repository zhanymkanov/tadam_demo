from fastapi import FastAPI

from app.auth.routers import router as auth_router
from app.videos.routers import router as video_router

from .database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(video_router, prefix="/videos", tags=["Video"])
