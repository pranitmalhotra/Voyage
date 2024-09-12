import uuid
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from schemas import FormData
from models import FormSubmission

router = APIRouter()

@router.post("/submit")
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
