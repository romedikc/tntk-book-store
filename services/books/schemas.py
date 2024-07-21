from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    picture: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    picture: Optional[str] = None


class Product(ProductBase):
    id: int

    class Config:
        orm_mode: True
