from pydantic import BaseModel, StrictInt, StrictStr

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
    hotel: StrictStr
    breakfast: StrictStr
    options: list[StrictStr]