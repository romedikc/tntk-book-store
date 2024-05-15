from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    is_completed: bool = False
    user_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
