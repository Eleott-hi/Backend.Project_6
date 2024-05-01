from fastapi import APIRouter, status, File, Form, Response, Depends
from services.JWTBearer import JWTBearer
from uuid import UUID
from services.Interfaces.IImageService import IImageService


class ImageRouter:
    def __init__(self, service: IImageService):
        self.router = APIRouter(
            prefix="/images",
            tags=["Image"],
            # dependencies=[Depends(JWTBearer())]
        )
        self.service = service

        @self.router.get(
            "/{id}",
            status_code=status.HTTP_200_OK,
            responses={404: {"description": "Item not found"}},
        )
        async def get_image_by_id(id: UUID) -> Response:
            """
            Retrieve an image by its ID.

            - `id`: UUID. ID of the image to retrieve.

            Returns:
            - Response object with the image content.
            """
            res: bytes = await self.service.one(id)
            return Response(content=res, media_type="application/octet-stream")

        @self.router.get(
            "/by-product/{product_id}",
            status_code=status.HTTP_200_OK,
            responses={404: {"description": "Item not found"}},
        )
        async def get_image_by_product_id(product_id: UUID) -> Response:
            """
            Retrieve an image by product ID.

            - `product_id`: UUID. ID of the product associated with the image.

            Returns:
            - Response object with the image content.
            """
            res = await self.service.one_by_product_id(product_id)
            return Response(content=res, media_type="application/octet-stream")

        @self.router.post(
            "/",
            status_code=status.HTTP_201_CREATED,
            responses={404: {"description": "Item not found"}},
        )
        async def upload_image(
            image: bytes = File(...), product_id: UUID = Form(...)
        ) -> UUID:
            """
            Upload an image.

            - `image`: Bytes. Binary data of the image file.
            - `product_id`: UUID. ID of the product associated with the image.

            Returns:
            - UUID of the uploaded image.
            """
            res: UUID = await self.service.create(image, product_id)
            return res

        @self.router.put(
            "/{id}",
            status_code=status.HTTP_204_NO_CONTENT,
            responses={404: {"description": "Item not found"}},
        )
        async def update_image(id: UUID, image: bytes = File(...)):
            """
            Update an existing image.

            - `id`: UUID. ID of the image to update.
            - `image`: Bytes. Binary data of the updated image file.

            Returns:
            - Success message.
            """
            await self.service.update(id, image)

        @self.router.delete(
            "/{id}",
            status_code=status.HTTP_204_NO_CONTENT,
            responses={404: {"description": "Item not found"}},
        )
        async def delete_image(id: UUID):
            """
            Delete an image by its ID.

            - `id`: UUID. ID of the image to delete.

            Returns:
            - Success message.
            """
            await self.service.delete(id)
