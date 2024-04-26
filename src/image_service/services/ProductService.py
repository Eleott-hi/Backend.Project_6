from uuid import UUID
import httpx
from config import STORE_SERVICE, STORE_SERVICE_VERSION
from schemas.Product import Product
from fastapi import status
from fastapi.exceptions import HTTPException


class ProductService:
    @classmethod
    async def get_product(product_id: UUID):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{STORE_SERVICE}/api/{STORE_SERVICE_VERSION}/products/{id}"
            )

            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status_code, detail=response.text
                )

            product = Product(**response.json())
            return product

    @classmethod
    async def set_image_id_to_product(product_id: UUID, image_id: UUID):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://{STORE_SERVICE}/api/{STORE_SERVICE_VERSION}/products/{product_id}",
                json={"image_id": image_id},
            )

        if response.status_code != status.HTTP_204_NO_CONTENT:
            raise HTTPException(status_code=response.status_code, detail=response.text)
