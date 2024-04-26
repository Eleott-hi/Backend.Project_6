from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Product(BaseModel):
    id: UUID
    name: str
    category: str
    price: float
    available_stock: int
    supplier_id: Optional[UUID] = None
    image_id: Optional[UUID] = None
    last_update_date: datetime

