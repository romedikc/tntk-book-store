from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    picture: str = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    picture: Optional[str] = None

    class Config:
        orm_mode: True
