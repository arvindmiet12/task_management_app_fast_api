from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils.settings import settings

Base = declarative_base()

engine = create_engine(url=settings.DB_CONNECTION)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()