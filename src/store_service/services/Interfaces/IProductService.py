
from typing import List
from database.models.models import Product
from routers.schemas import ProductRequest
from uuid import UUID
import abc


class IProductService(abc.ABC):

    @abc.abstractmethod
    async def all(offset: int, limit: int) -> List[Product]:
        raise NotImplementedError

    @abc.abstractmethod
    async def one(id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def create(product: ProductRequest):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def update_stock_and_price(id: UUID, price: float, stock: int):
        raise NotImplementedError
