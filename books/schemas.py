from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    picture: Optional[UploadFile] = None
    stock: Optional[int] = 0


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode: True
