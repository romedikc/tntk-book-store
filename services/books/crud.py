import os
import shutil

from fastapi import UploadFile, File
from sqlalchemy.orm import Session

from services.books.schemas import ProductCreate
from services.database import UPLOAD_DIR
from services.models import Product


def create_product(db: Session,
                   name: str,
                   description: str,
                   price: float,
                   picture: UploadFile = File(None),
                   ):
    picture_path = None
    if picture:
        picture_path = os.path.join(UPLOAD_DIR, picture.filename)
        with open(picture_path, "wb") as buffer:
            shutil.copyfileobj(picture.file, buffer)
    db_product = Product(name=name,
                         description=description,
                         price=price,
                         picture=picture_path)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def read_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


# def update_task(db: Session, db_task: models.Task, task_update: TaskUpdate):
#     for field, value in task_update.dict(exclude_unset=True).items():
#         setattr(db_task, field, value)
#     db.commit()
#     db.refresh(db_task)
#     return db_task


# def delete_task(db: Session, task_id: int):
#     db_task = get_task(db, task_id)
#     if db_task:
#         db.delete(db_task)
#         db.commit()
#         return True
#     return False


def read_products(db: Session):
    return db.query(Product).all()
