import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, StrictInt, StrictStr
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FormSubmission(Base):
    """
    Represents a form submission stored in the 'submissions' table.

    Attributes:
        id: Primary key, auto-incremented.
        destination: The destination selected in the form.
        duration: The duration of the trip.
        budget: The budget for the trip.
        option1: The first option chosen.
        option2: The second option chosen.
        option3: The third option chosen.
    """
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String)
    duration = Column(Integer)
    budget = Column(Integer)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)

Base.metadata.create_all(bind=engine)

class FormData(BaseModel):
    """
    Pydantic model for form data validation.

    Attributes:
        destination: The destination of the form, must be a strict string.
        duration: The duration of the trip, must be a strict integer.
        budget: The budget for the trip, must be a strict integer.
        options: List of three options, each must be a strict string.
    """
    destination: StrictStr
    duration: StrictInt  
    budget: StrictInt
    options: list[StrictStr]

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/submit")
async def submit_form(data: FormData, db: Session = Depends(get_db)):
    """
    Endpoint to handle form submission.

    Args:
        data: The validated form data.
        db: The database session.

    Returns:
        A success message upon successful form submission.
    """
    new_submission = FormSubmission(
        destination=data.destination,
        duration=data.duration,
        budget=data.budget,
        option1=data.options[0],
        option2=data.options[1],
        option3=data.options[2],
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return {"message": "Form submitted successfully!"}