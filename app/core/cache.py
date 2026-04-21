import json
from redis.asyncio import Redis


class Cache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str):
        result = await self.redis.get(key)
        return json.loads(result) if result else None

    async def set(self, key: str, value: str, expire: int = 300):
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()
        await self.redis.connection_pool.disconnect()
    
    async def acquire_lock(self, key: str, ttl: int = 10):
        lock_key = f"lock:{key}"
        if await self.redis.lock(lock_key, timeout=ttl, blocking_timeout=0).acquire():
            return True
        return False
    
    async def release_lock(self, key: str):
        lock_key = f"lock:{key}"
        await self.redis.lock(lock_key).release()

