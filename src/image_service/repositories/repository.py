from database.database import (
    img_engine_1,
    img_engine_2,
    img_engine_3,
    img_engine_4,
    Session,
)
from uuid import UUID
from fastapi.exceptions import HTTPException
from fastapi.status import HTTP_404_NOT_FOUND


async def get_image_related_session(id: UUID) -> Session:
    letter = str(id)[0]

    if letter in "0123":
        return img_engine_1

    elif letter in "4567":
        return img_engine_2

    elif letter in "89ab":
        return img_engine_3

    elif letter in "cdef":
        return img_engine_4

    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid UUID")
