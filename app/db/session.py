from sqlalchemy.orm import async_sessionmaker, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


def get_session_local(engine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
