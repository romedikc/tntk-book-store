from sqlalchemy.orm import Session

from services.books.schemas import ProductCreate
from services.models import Product


def create_product(db: Session, product_create: ProductCreate):
    db_task = Product(**product_create.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


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
