import contextlib
from copy import deepcopy
from typing import Any, AsyncGenerator, Coroutine, Generator
from uuid import UUID
import database.models.image
from sqlmodel import SQLModel, select, update, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from config import IMAGE_DB_1, IMAGE_DB_2, IMAGE_DB_3, IMAGE_DB_4
from fastapi import HTTPException
from fastapi import status
import asyncpg

engine_1 = create_async_engine(IMAGE_DB_1, echo=True, future=True)
async_session_1 = sessionmaker(engine_1, class_=AsyncSession, expire_on_commit=False)
engine_2 = create_async_engine(IMAGE_DB_2, echo=True, future=True)
async_session_2 = sessionmaker(engine_2, class_=AsyncSession, expire_on_commit=False)
engine_3 = create_async_engine(IMAGE_DB_3, echo=True, future=True)
async_session_3 = sessionmaker(engine_3, class_=AsyncSession, expire_on_commit=False)
engine_4 = create_async_engine(IMAGE_DB_4, echo=True, future=True)
async_session_4 = sessionmaker(engine_4, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    print("Initialize database models", flush=True)

    for engine in [engine_1, engine_2, engine_3, engine_4]:
        url = engine.url.set(drivername="postgresql")
        if not database_exists(url):
            create_database(url)

        async with engine.begin() as session:
            await session.run_sync(SQLModel.metadata.create_all)

    print("Finish Initializing database models", flush=True)


@contextlib.asynccontextmanager
async def get_session(id: UUID) -> AsyncGenerator[AsyncSession, None]:
    shradding = {
        "0123": async_session_1,
        "4567": async_session_2,
        "89ab": async_session_3,
        "cdef": async_session_4,
    }

    ch = str(id)[0]

    for k, session in shradding.items():
        if ch in k:
            async with session() as session:
                yield session
                return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Database not found"
    )
