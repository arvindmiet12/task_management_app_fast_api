from sqlalchemy import Column, Integer, String, Text, DateTime
from src.utils.db import Base


class TaskModel(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

