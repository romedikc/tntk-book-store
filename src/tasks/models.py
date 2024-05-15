from datetime import datetime

from sqlalchemy import Integer, Column, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from src.database import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks")
