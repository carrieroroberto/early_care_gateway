import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_DBNAME = os.getenv("POSTGRES_DB", "postgres")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DBNAME}"

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DB_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session