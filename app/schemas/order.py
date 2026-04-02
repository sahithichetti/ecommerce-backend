from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.product import ProductResponse


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    shipping_address: str
    payment_method: str = "cod"


class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    shipping_address: str
    payment_method: str
    created_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
