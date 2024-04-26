from database.database import get_session, AsyncSession
from uuid import UUID, uuid4
from fastapi.exceptions import HTTPException
from fastapi import status
from database.models.image import Image
from fastapi import Depends


class ImageRepository:
    async def get_image(id: UUID) -> Image:
        async with get_session(id=id) as session:
            image = await session.get(Image, id)
            return image

    async def create_image(image: bytes) -> Image:
        image = Image(id=uuid4(), image=image)

        async with get_session(id=image.id) as session:
            await session.add(image)
            await session.commit()

        return image

    async def update_image(id: UUID, image: bytes) -> Image:
        try:
            async with get_session(id=image.id) as session:
                image = await session.get(Image, id)
                image.image = image
                await session.add(image)
                await session.commit()

                return image

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Image not found: {e}"
            )

    async def delete_image(id: UUID):
        try:
            async with get_session(id=id) as session:
                await session.delete(Image, id)
                session.commit()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Image not found: {e}"
            )
