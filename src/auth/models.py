from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    name = Column(String)
    password = Column(String)

    tasks = relationship("Task", back_populates="user")
