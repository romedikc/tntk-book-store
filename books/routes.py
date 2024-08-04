from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from books import crud
from books.schemas import ProductCreate, Product
from root.database import get_db

router = APIRouter(prefix="/books", tags=["books"])

db_dependency = Depends(get_db)


def process_order(message):
    product_id = message.get("product_id")
    quantity = message.get("quantity")

    crud.update_product_stock(db_dependency, product_id, quantity)


@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = db_dependency):
    return crud.create_product(db=db,
                               name=product.name,
                               description=product.description,
                               price=product.price,
                               picture=product.picture,
                               stock=product.stock,
                               )


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = db_dependency):
    task = crud.read_product(db=db, product_id=product_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Book is not found")
    return task


# @router.put("/{task_id}", response_model=schemas.Task)
# def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = db_dependency):
#     task = crud.get_task(db=db, task_id=task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return crud.update_task(db=db, db_task=task, task_update=task_update)
#
#
# @router.delete("/{task_id}")
# def delete_task(task_id: int, db: Session = db_dependency):
#     if not crud.delete_task(db=db, task_id=task_id):
#         raise HTTPException(status_code=404, detail="Task not found")
#     return {"detail": "Task deleted"}


@router.get("/", response_model=List[Product])
def read_products(db: Session = db_dependency):
    products = crud.read_products(db=db)
    return products
