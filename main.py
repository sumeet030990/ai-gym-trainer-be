from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.middlewares import StructuredResponseMiddleware
from db.database import engine, init_db
from routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup, before the app accepts requests.
    await init_db()
    print("Database connected")

    # App serves requests while suspended here.
    yield

    # Runs once on shutdown: release pooled DB connections cleanly.
    await engine.dispose()
    print("Database connection closed")


app = FastAPI(lifespan=lifespan)

app.add_middleware(StructuredResponseMiddleware)

app.include_router(api_router)