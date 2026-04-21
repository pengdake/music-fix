from contextlib import asynccontextmanager
from app.core.logger import setup_logger
from fastapi import FastAPI
from redis.asyncio.sentinel import Sentinel
from app.core.config import get_settings
from app.core.cache import Cache

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在这里执行应用启动时的初始化操作，例如连接数据库、设置缓存等
    setup_logger()
    settings = get_settings()
    sentinel = Sentinel(settings.redis.sentinel_hosts)
    redis = sentinel.master_for(settings.redis.sentinel_master_name, socket_timeout=0.1, decode_responses=True, password=settings.redis.password)
    app.state.cache = Cache(redis)
    yield
    # 在这里执行应用关闭时的清理操作，例如关闭数据库连接、清理缓存等
    await app.state.cache.close()

