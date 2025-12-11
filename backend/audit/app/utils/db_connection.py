import os
# Import SQLAlchemy components for asynchronous DB interaction
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Retrieve database connection settings from environment variables
# Defaults are provided for local development
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_DBNAME = os.getenv("POSTGRES_DB", "postgres")

# Construct the async PostgreSQL connection string
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DBNAME}"

class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy ORM models.
    """
    pass

# Create the asynchronous database engine
# echo=True logs generated SQL for debugging
engine = create_async_engine(DB_URL, echo=True)

# Configure the session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    """
    Dependency generator that provides a database session.
    Ensures the session is closed after use.
    """
    async with async_session() as session:
        yield session