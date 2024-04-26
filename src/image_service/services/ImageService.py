from uuid import UUID
import httpx
from shemas import Product
from fastapi import status
from fastapi.exceptions import HTTPException
from services.ProductService import ProductService
from services.RedisCacheService import RedisCacheService
from repositories.ImageRepository import ImageRepository

async def get_image_id_from_product(product_id: UUID):
    product = await ProductService.get_product(product_id)
    return product.image_id

class ImageService():

    @classmethod
    async def get_image(cls, image_id: UUID):
       if image := RedisCacheService().get_data(image_id):
           return image
       
       image = ImageRepository.get_image(image_id)
        
