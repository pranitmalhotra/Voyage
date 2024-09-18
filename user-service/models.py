from backend.app.core.db import Base
from sqlalchemy import Column, Integer, String

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