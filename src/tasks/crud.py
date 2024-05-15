from sqlalchemy.orm import Session
from src.tasks import models
from src.tasks.schemas import TaskCreate, TaskUpdate


def create_task(db: Session, task_create: TaskCreate):
    db_task = models.Task(**task_create.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, db_task: models.Task, task_update: TaskUpdate):
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False


def get_user_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()
