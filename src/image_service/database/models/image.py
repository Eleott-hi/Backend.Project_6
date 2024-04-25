from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime
from enum import Enum

from pydantic_extra_types.phone_numbers import PhoneNumber

class Image(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    image: bytes

    # product: Optional["Product"] = Relationship(back_populates="image")