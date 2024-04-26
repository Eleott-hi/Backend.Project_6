from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class Image(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    image: bytes
