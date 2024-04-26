from database.database import get_session, Session
from uuid import UUID
from fastapi.exceptions import HTTPException
from fastapi import status
from database.models.image import Image
from fastapi import Depends


async def get_image(id: UUID, session: Session = Depends(get_session)) -> Image:
    try:
        image = await session.get(Image, id)
        return image
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )


