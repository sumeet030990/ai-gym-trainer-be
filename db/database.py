from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load variables from the .env file into the process environment.
load_dotenv()


# Base class that all SQLAlchemy ORM models (e.g. db/schemas/users.py) must
# inherit from. It gives SQLAlchemy the metadata it needs to map classes to
# database tables and is also what Alembic will read to autogenerate migrations.
class Base(DeclarativeBase):
    pass

# Connection details, pulled from environment variables (see .env).
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# "+asyncpg" tells SQLAlchemy to use the asyncpg driver, which is required
# for create_async_engine to work with Postgres.
DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# The engine manages the pool of connections to the database.
# NullPool disables connection pooling (a new connection is opened and closed
# for every use) rather than reusing a fixed set of connections.
engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)

# Factory for creating new AsyncSession objects bound to the engine.
# expire_on_commit=False keeps loaded attributes usable after a commit,
# instead of SQLAlchemy expiring them and forcing a re-fetch on next access.
Async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_db():
    # Open a connection and run a trivial query to fail fast on startup if
    # the database is unreachable. Table creation is left to Alembic
    # migrations rather than done here.
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

async def get_session():
    # FastAPI dependency: opens a session for the duration of a request and
    # closes it automatically afterwards, even if an error is raised.
    async with Async_session() as session:
        yield session
