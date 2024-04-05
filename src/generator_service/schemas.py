from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Product(BaseModel):
    id: UUID
    name: str
    category: str
    price: float
    available_stock: int
    last_update_date: datetime
    supplier_id: Optional[UUID]
    image_id: Optional[UUID]
