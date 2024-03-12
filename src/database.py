from typing import AsyncGenerator

from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from src.config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USERNAME,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
)

DATABASE_URL = (
    f"postgresql+asyncpg://" f"{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

Base: DeclarativeMeta = declarative_base()

async_engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_redis_object():
    return Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )


redis = get_redis_object()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SCHEMA_FOR_SETTINGS = "settings"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
