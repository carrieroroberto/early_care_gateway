import os
# Import SQLAlchemy components for asynchronous database interaction
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Retrieve database credentials and connection details from environment variables
# Default values are provided for local development convenience
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_DBNAME = os.getenv("POSTGRES_DB", "postgres")

# Construct the asynchronous PostgreSQL connection URL using asyncpg driver
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DBNAME}"

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass

# Create the asynchronous engine
# echo=True enables logging of generated SQL for debugging purposes
engine = create_async_engine(DB_URL, echo=True)

# Create a session factory to generate AsyncSession instances
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    """
    Dependency generator that yields a database session.
    Ensures the session is closed after the request is processed.
    """
    async with async_session() as session:
        yield session