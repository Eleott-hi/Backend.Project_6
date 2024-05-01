import httpx

from typing import Optional
from fastapi import status, HTTPException
from uuid import UUID
from services.Interfaces.IImageService import IImageService
from repositories.Interfaces.IProductRepository import IProductRepository
import redis.asyncio as redis
from config import REDIS_SERVICE, IMAGE_SERVICE, IMAGE_SERVICE_API
from services.utils import get_upstream_fastapi_http_exception


class ImageService(IImageService):
    def __init__(self, product_repository: IProductRepository) -> None:
        self.product_repository = product_repository
        self.base_url = f"http://{IMAGE_SERVICE}/api/{IMAGE_SERVICE_API}/images"
        self.redis = redis.Redis(host=REDIS_SERVICE)

    async def __get_image(self, id: UUID) -> bytes:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(f"{self.base_url}/{id}")

            if response.is_client_error or response.is_server_error:
                raise get_upstream_fastapi_http_exception(response)

            image = response.content
            return image

    async def __create_image(self, image: bytes) -> UUID:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            headers = {"Content-Type": "application/octet-stream"}
            response: httpx.Response = await client.post(
                self.base_url, content=image, headers=headers
            )

            if response.is_client_error or response.is_server_error:
                raise get_upstream_fastapi_http_exception(response)

            def dequote(s: str):
                return s[1:-1] if s[0] == s[-1] and s[0] in ("\"'") else s

            image_id = UUID(dequote(response.text))
            return image_id

    async def __update_image(self, id: UUID, image: bytes):
        async with httpx.AsyncClient() as client:
            headers = {"Content-Type": "application/octet-stream"}
            response: httpx.Response = await client.put(
                f"{self.base_url}/{id}", content=image, headers=headers
            )

            if response.is_client_error or response.is_server_error:
                raise get_upstream_fastapi_http_exception(response)

    async def __delete_image(self, id: UUID):
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.delete(f"{self.base_url}/{id}")

            if response.is_client_error or response.is_server_error:
                raise get_upstream_fastapi_http_exception(response)

    async def __get_product_with_image_id(self, image_id: UUID):
        product = await self.product_repository.one_by_image_id(image_id=image_id)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No product with image: {image_id}",
            )

        return product

    async def one(self, id: UUID) -> bytes:
        product = await self.__get_product_with_image_id(image_id=id)

        if (image := await self.redis.get(str(id))) is not None:
            print("USING CACHE", flush=True)
            return image

        image = await self.__get_image(id)
        await self.redis.set(str(id), image, ex=10)

        return image

    async def one_by_product_id(self, product_id: UUID):
        product = await self.product_repository.one(id=product_id)
        image_id: Optional[UUID] = product.image_id

        if image_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
            )

        res = await self.one(image_id)

        return res

    async def create(self, image: bytes, product_id: UUID):
        product = await self.product_repository.one(id=product_id)

        image_id: UUID = await self.__create_image(image)

        if product.image_id is not None:
            await self.__delete_image(product.image_id)

        await self.product_repository.set_image_id(product.id, image_id)
        await self.redis.set(str(image_id), image)

        return image_id

    async def update(self, id: UUID, image: bytes):
        product = await self.__get_product_with_image_id(image_id=id)
        await self.__update_image(id, image)
        await self.redis.set(str(id), image, ex=10)

    async def delete(self, id: UUID):
        product = await self.__get_product_with_image_id(image_id=id)

        await self.__delete_image(id)
        await self.product_repository.set_image_id(product.id, None)

        await self.redis.delete(str(id))
