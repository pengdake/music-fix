from fastapi import FastAPI
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field, SecretStr
from functools import lru_cache

class RedisSettings(BaseModel):
    sentinel_hosts: list[tuple[str, int]] = [("redis.default.svc", 26379)]
    sentinel_master_name: str = "mymaster"
    password: str = "abc123"

class DatabaseSettings(BaseModel):
    user = "YXBw"
    password = "yX1GEbvyGRT3O6kW7Qhx8Wiznc4OFE2kKSuufJqbgDugXwi4c4tCaCkzUvKIsw2x"
    db = "YXBw"
    write_svc = "cloudnative-postgresql-cluster-rw.default.svc.cluster.local"
    read_svc = "cloudnative-postgresql-cluster-ro.default.svc.cluster.local"
    write_url: str = f"postgresql+asyncpg://{{user}}:{{password}}@{{write_svc}}/{{db}}"
    read_url: str = f"postgresql+asyncpg://{{user}}:{{password}}@{{read_svc}}/{{db}}"

class Settings(BaseSettings):
    app_name: str = "home_web"
    redis: RedisSettings = RedisSettings()
    database: DatabaseSettings = DatabaseSettings()

@lru_cache()
def get_settings():
    return Settings()