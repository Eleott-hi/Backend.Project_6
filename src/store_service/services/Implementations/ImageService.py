from database.models.models import Image
from uuid import UUID
from services.Interfaces.IImageService import IImageService
from repositories.Interfaces.IImageRepository import IImageRepository
import redis.asyncio as redis
from config import REDIS_SERVICE


class ImageService(IImageService):
    def __init__(self, repository: IImageRepository):
        self.repository = repository
        self.redis = redis.Redis(host=REDIS_SERVICE)

    async def one(self, id: UUID) -> bytes:
        if await self.redis.exists(str(id)):
            print("USING CACHE", flush=True)
            data = await self.redis.get(str(id))
            return data

        res = await self.repository.one(id)

        await self.redis.set(str(id), res)

        return res

    async def one_by_product_id(self, product_id: UUID):
        res = await self.repository.one_by_product_id(product_id)
        return res

    async def create(self, image: bytes, product_id: UUID):
        image = Image(image=image)
        res = await self.repository.create(image, product_id)

        self.redis.set(str(res.id), res.image)

        return res.id

    async def update(self, id: UUID, image: bytes):
        res = await self.repository.update(id, image)

        self.redis.set(str(id), res.image)

        return res

    async def delete(self, id: UUID):
        res = await self.repository.delete(id)

        self.redis.delete(str(id))

        return res
