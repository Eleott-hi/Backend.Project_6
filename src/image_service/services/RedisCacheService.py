from database.models.image import Image
from uuid import UUID
import redis.asyncio as redis
from config import REDIS_SERVICE_HOST, REDIS_SERVICE_PORT
from py_singleton import singleton

@singleton
class RedisCacheService():
    def __init__(self) -> None:
        self.redis = redis.Redis(host=REDIS_SERVICE_HOST, port=REDIS_SERVICE_PORT)

    async def cache_decorator(self, func):
        async def wrapper( *args, **kwargs):
            key = 

            if self.redis.exists(key):
                return self.redis.get(key)
            
            else:
                result = await func(self, *args, **kwargs)
                self.redis.set(key, result)
                return result
            
        return wrapper