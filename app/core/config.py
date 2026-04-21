from fastapi import FastAPI
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field, SecretStr
from functools import lru_cache

class RedisSettings(BaseModel):
    sentinel_hosts: list[tuple[str, int]] = [("redis.default.svc", 26379)]
    sentinel_master_name: str = "mymaster"
    password: str = "abc123"


class Settings(BaseSettings):
    app_name: str = "home_web"
    redis: RedisSettings = RedisSettings()

@lru_cache()
def get_settings():
    return Settings()