from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode: True


class OrderBase(BaseModel):
    user_id: int


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    items: List[OrderItem]
    created_at: datetime

    class Config:
        orm_mode: True


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_method: str


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    status: str
    created_at: Optional[str] = None
    order: Order

    class Config:
        orm_mode: True
