from typing import Any
from database.models.image import Image
from uuid import UUID
import redis.asyncio as redis
from config import REDIS_SERVICE_HOST, REDIS_SERVICE_PORT
from py_singleton import singleton


@singleton
class RedisCacheService:
    def __init__(self) -> None:
        self.redis = redis.Redis(
            host=REDIS_SERVICE_HOST, port=REDIS_SERVICE_PORT, db="Cache"
        )

    async def get_data(self, key: str) -> Any:
        if await self.redis.exists(str(id)):
            return await self.redis.get(str(id))

        return None

    async def set_data(self, key: str, data: Any) -> None:
        await self.redis.set(str(id), data)


    