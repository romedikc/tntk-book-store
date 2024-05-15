from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.tasks import schemas, crud

router = APIRouter(prefix="/tasks", tags=["tasks"])

db_dependency = Depends(get_db)


@router.post("/", response_model=schemas.Task)
def create_task(task_create: schemas.TaskCreate, db: Session = db_dependency):
    return crud.create_task(db=db, task_create=task_create)


@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = db_dependency):
    task = crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = db_dependency):
    task = crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, db_task=task, task_update=task_update)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = db_dependency):
    if not crud.delete_task(db=db, task_id=task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}


@router.get("/user/{user_id}", response_model=List[schemas.Task])
def read_user_tasks(user_id: int, db: Session = db_dependency):
    tasks = crud.get_user_tasks(db=db, user_id=user_id)
    return tasks
