import os
# Import SQLAlchemy modules for asynchronous database connection and ORM
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Retrieve database connection parameters from environment variables
# Defaults are set for local development environment
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_DBNAME = os.getenv("POSTGRES_DB", "postgres")

# Construct the connection URL for the asynchronous PostgreSQL driver (asyncpg)
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DBNAME}"

class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy ORM models.
    """
    pass

# Create the asynchronous engine
# echo=True enables logging of generated SQL statements for debugging
engine = create_async_engine(DB_URL, echo=True)

# Configure the session factory for creating asynchronous sessions
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    """
    Dependency generator that yields a database session.
    Ensures the session is properly closed after the request is finished.
    """
    async with async_session() as session:
        yield session