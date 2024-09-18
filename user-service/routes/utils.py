from fastapi import APIRouter, status

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def healthcheck():
    """
    Health check endpoint.
    """
    return {"status": "OK"}
