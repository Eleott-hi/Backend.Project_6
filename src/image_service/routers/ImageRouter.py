from fastapi import APIRouter, status, File, Form, Response, Depends
from services.JWTBearer import JWTBearer
from uuid import UUID
from services.Interfaces.IImageService import IImageService
from database.database import Session, get_session


router = APIRouter(
    prefix="/images",
    tags=["Image"],
    # dependencies=[Depends(JWTBearer())]
)


@router.get("/{id}", responses={404: {"description": "Item not found"}})
async def get_image_by_id(
    id: UUID,
) -> Response:
    """
    Retrieve an image by its ID.

    - `id`: UUID. ID of the image to retrieve.

    Returns:
    - Response object with the image content.
    """
    res: bytes = await service.one(id)
    return Response(content=res, media_type="application/octet-stream")


@router.get(
    "/by-product/{product_id}",
    responses={404: {"description": "Item not found"}},
)
async def get_image_by_product_id(product_id: UUID) -> Response:
    """
    Retrieve an image by product ID.

    - `product_id`: UUID. ID of the product associated with the image.

    Returns:
    - Response object with the image content.
    """
    res = await service.one_by_product_id(product_id)
    return Response(content=res, media_type="application/octet-stream")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_image(image: bytes = File(...), product_id: UUID = Form(...)) -> UUID:
    """
    Upload an image.

    - `image`: Bytes. Binary data of the image file.
    - `product_id`: UUID. ID of the product associated with the image.

    Returns:
    - UUID of the uploaded image.
    """
    res: UUID = await service.create(image, product_id)
    return res


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={404: {"description": "Item not found"}},
)
async def update_image(id: UUID, image: bytes = File(...)) -> str:
    """
    Update an existing image.

    - `id`: UUID. ID of the image to update.
    - `image`: Bytes. Binary data of the updated image file.

    Returns:
    - Success message.
    """
    res = await service.update(id, image)
    return res


@router.delete("/{id}", responses={404: {"description": "Item not found"}})
async def delete_image(id: UUID) -> str:
    """
    Delete an image by its ID.

    - `id`: UUID. ID of the image to delete.

    Returns:
    - Success message.
    """
    res = await service.delete(id)
    return res
