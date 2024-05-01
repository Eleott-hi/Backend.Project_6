from fastapi import APIRouter, status, File, Form, Response, Depends, Body
from database.models.image import Image
from fastapi.exceptions import HTTPException

# from services.JWTBearer import JWTBearer
from uuid import UUID

# from database.database import Session, get_session
from repositories.ImageRepository import ImageRepository


router = APIRouter(prefix="/images", tags=["Image"])


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Image not found"}},
)
async def get_image_by_id(id: UUID) -> Response:
    image: Image = await ImageRepository.one(id)
    res: bytes = image.image
    return Response(content=res, media_type="application/octet-stream")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_image(image: bytes = Body(..., media_type="application/octet-stream")) -> UUID:
    image: Image = await ImageRepository.create(image=image)
    return image.id


@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Image not found"}},
)
async def update_image(id: UUID, image: bytes = Body(..., media_type="application/octet-stream")) -> None:
    await ImageRepository.update(id, image)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Image not found"}},
)
async def delete_image(id: UUID) -> None:
    await ImageRepository.delete(id)
