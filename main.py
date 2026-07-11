from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database import engine, init_db
from routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database connected")
    yield
    await engine.dispose()
    print("Database connection closed")


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)