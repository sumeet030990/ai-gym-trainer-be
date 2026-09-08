from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares import StructuredResponseMiddleware
from core.config import settings
from db.database import engine, init_db
from routers import api_router
from dotenv import load_dotenv
# Inject variables from .env into the application environment
load_dotenv() 

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(StructuredResponseMiddleware)

app.include_router(api_router)