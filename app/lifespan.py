from contextlib import asynccontextmanager
from app.core.logger import setup_logger
from fastapi import FastAPI
from redis.asyncio.sentinel import Sentinel
from app.core.config import get_settings
from app.core.cache import Cache
from sqlmodel import create_async_engine

from app.db.session import get_session_local

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在这里执行应用启动时的初始化操作，例如连接数据库、设置缓存等
    setup_logger()
    settings = get_settings()
    sentinel = Sentinel(settings.redis.sentinel_hosts)
    redis = sentinel.master_for(settings.redis.sentinel_master_name, socket_timeout=0.1, decode_responses=True, password=settings.redis.password)
    app.state.cache = Cache(redis)
    db_write_url = settings.database.write_url.format(
        user=settings.database.user,
        password=settings.database.password,
        write_svc=settings.database.write_svc,
        db=settings.database.db
    )
    app.state.write_engine = create_async_engine(db_write_url, echo=True, pool_size=10, max_overflow=20)
    app.state.write_session_local = get_session_local(app.state.write_engine)
    db_read_url = settings.database.read_url.format(
        user=settings.database.user,
        password=settings.database.password,
        read_svc=settings.database.read_svc,
        db=settings.database.db
    )
    app.state.read_engine = create_async_engine(db_read_url, echo=True, pool_size=10, max_overflow=20)
    app.state.read_session_local = get_session_local(app.state.read_engine)
    yield
    # 在这里执行应用关闭时的清理操作，例如关闭数据库连接、清理缓存等
    await app.state.cache.close()
    await app.state.write_engine.dispose()
    await app.state.read_engine.dispose()

