from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from .config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency to get the database session.
    
    Yields:
        db: A database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()