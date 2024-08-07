from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from services.books import crud
from services.books.schemas import Product, ProductCreate, ProductUpdate
from services.database import get_db

router = APIRouter(prefix="/books", tags=["books"])

db_dependency = Depends(get_db)


@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = db_dependency):
    return crud.create_product(db=db,
                               name=product.name,
                               description=product.description,
                               price=product.price,
                               picture=product.picture,
                               )


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = db_dependency):
    task = crud.read_product(db=db, product_id=product_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Book is not found")
    return task


@router.patch("/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate, db: Session = db_dependency):
    updated_product = crud.update_product(db=db, product_id=product_id, product=product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{task_id}")
def delete_product(product_id: int, db: Session = db_dependency):
    if not crud.delete_product(db=db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}


@router.get("/", response_model=List[Product])
def read_products(db: Session = db_dependency):
    products = crud.read_products(db=db)
    return products
