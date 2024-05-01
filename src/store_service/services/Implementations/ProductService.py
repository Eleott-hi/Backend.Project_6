import httpx

from typing import List
from database.models.models import Product
from routers.schemas import ProductRequest
from uuid import UUID
from services.Interfaces.IProductService import IProductService
from repositories.Interfaces.IProductRepository import IProductRepository
from config import IMAGE_SERVICE, IMAGE_SERVICE_API
from services.utils import get_upstream_fastapi_http_exception


class ProductService(IProductService):
    def __init__(self, repository: IProductRepository):
        self.repository = repository
        self.image_service = f"http://{IMAGE_SERVICE}/api/{IMAGE_SERVICE_API}/images"

    async def __delete_image(self, id: UUID):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(f"{self.image_service}/{id}")

            if response.is_client_error or response.is_server_error:
                raise get_upstream_fastapi_http_exception(response)

    async def all(self, offset: int, limit: int) -> List[Product]:
        res = await self.repository.all(offset, limit)
        return res

    async def one(self, id: UUID):
        res = await self.repository.one(id)
        return res

    async def create(self, product: ProductRequest):
        product = Product.model_validate(product)
        res = await self.repository.create(product)
        return res

    async def delete(self, id: UUID):
        res = await self.repository.one(id)

        if res.image_id:
            await self.__delete_image(id=res.image_id)

        res = await self.repository.delete(id)
        return res

    async def update_stock_and_price(self, id: UUID, price: float, stock: int):
        res = await self.repository.update_stock_and_price(id, price, stock)
        return res
