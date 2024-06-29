from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    picture: Optional[UploadFile] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    picture: Optional[str] = None

    class Config:
        orm_mode: True
