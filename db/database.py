from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from core.config import get_settings


# Deterministic names for indexes/constraints so Alembic autogenerate never
# emits unnamed constraints (e.g. op.create_foreign_key(None, ...)), which
# breaks the corresponding downgrade's op.drop_constraint(None, ...).
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


# Base class that all SQLAlchemy ORM models (e.g. db/schemas/users.py) must
# inherit from. It gives SQLAlchemy the metadata it needs to map classes to
# database tables and is also what Alembic will read to autogenerate migrations.
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

# The engine manages the pool of connections to the database.
# NullPool disables connection pooling (a new connection is opened and closed
# for every use) rather than reusing a fixed set of connections.
engine = create_async_engine(get_settings().database_url, echo=True, poolclass=NullPool)

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
