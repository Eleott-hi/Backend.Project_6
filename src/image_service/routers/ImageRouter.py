from fastapi import APIRouter, status, File, Form, Response, Depends
from database.models.image import Image
from schemas.Product import Product
from services.ProductService import ProductService
from fastapi.exceptions import HTTPException

# from services.JWTBearer import JWTBearer
from uuid import UUID

# from database.database import Session, get_session
from repositories.ImageRepository import ImageRepository


router = APIRouter(
    prefix="/images",
    tags=["Image"],
    # dependencies=[Depends(JWTBearer())]
)


@router.get("/{id}", responses={404: {"description": "Item not found"}})
async def get_image_by_id(id: UUID) -> Response:
    """
    Retrieve an image by its ID.

    - `id`: UUID. ID of the image to retrieve.

    Returns:
    - Response object with the image content.
    """
    image: Image = await ImageRepository.get_image(id)
    res: bytes = image.image
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
    product: Product = ProductService.get_product(product_id)

    if product.image_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product has no image"
        )

    image: Image = await ImageRepository.get_image(product.image_id)
    res: bytes = image.image

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
    image: Image = ImageRepository.create_image(image=image)
    ProductService.set_image_id_to_product(product_id, image.id)

    return image.id


@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Item not found"}},
)
async def update_image(id: UUID, image: bytes = File(...)) -> None:
    """
    Update an existing image.

    - `id`: UUID. ID of the image to update.
    - `image`: Bytes. Binary data of the updated image file.

    Returns:
    - NO RETURN
    """

    ImageRepository.update_image(id, image)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Item not found"}},
)
async def delete_image(id: UUID) -> None:
    """
    Delete an image by its ID.

    - `id`: UUID. ID of the image to delete.

    Returns:
    - NO RETURN
    """
    ImageRepository.delete_image(id)
