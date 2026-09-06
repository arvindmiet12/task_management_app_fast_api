from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

