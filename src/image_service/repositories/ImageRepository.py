from database.database import get_session, AsyncSession, select, update, delete
from uuid import UUID, uuid4
from fastapi.exceptions import HTTPException
from fastapi import status
from database.models.image import Image
from fastapi import Depends


class ImageRepository:
    async def one(id: UUID) -> Image:
        async with get_session(id=id) as session:
            query = select(Image).where(Image.id == id)
            image: Image | None = (await session.exec(query)).first()

            if image is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Image not found {id}",
                )

            return image

    async def create(image: bytes):
        image = Image(id=uuid4(), image=image)

        async with get_session(id=image.id) as session:
            session.add(image)
            await session.commit()

        return image

    async def update(id: UUID, image_data: bytes):
        async with get_session(id=id) as session:
            query = (
                update(Image)
                .where(Image.id == id)
                .values(image=image_data)
                .execution_options(synchronize_session="fetch")
                .where(Image.id == id)
            )
            result = await session.exec(query)

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Image not found: {id}",
                )

            await session.commit()

    async def delete(id: UUID):
        async with get_session(id=id) as session:
            query = (
                delete(Image)
                .where(Image.id == id)
                .execution_options(synchronize_session="fetch")
                .where(Image.id == id)
            )

            result = await session.exec(query)

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Image not found: {id}",
                )

            await session.commit()
