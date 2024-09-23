import os
import logging
import json
from fastapi import FastAPI, APIRouter
import httpx
from google.cloud import pubsub_v1
from typing import Dict
from core.config import settings
from redis import Redis
from schemas import FormData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
router = APIRouter()

publisher_client = pubsub_v1.PublisherClient()
topic_name = f"projects/{settings.GOOGLE_PROJECT_ID}/topics/{settings.GOOGLE_PUBSUB_TOPIC}"

redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@router.post("/submit")
async def submit_form(data: FormData):
    """
    Receives form data, checks the Redis cache for an existing itinerary,
    and publishes a message to Google Pub/Sub for itinerary generation.

    Parameters:
        data (FormData): The form data containing budget, destination, 
                         duration, preferences, and breakfast option.

    Returns:
        dict: A response indicating the status of the request.
    """
    budget = data.budget
    destination = data.destination
    duration = data.duration
    preferences = data.preferences
    preferences["dineIn"] = True
    breakfast = data.breakfast

    cache_key = f"itinerary:{destination}:{duration}:{json.dumps(preferences)}"
    cached_response = redis_client.get(cache_key)

    if cached_response:
        logger.info("Cache hit: Returning cached response.")
        return json.loads(cached_response)

    message_data = {
        "budget": budget,
        "destination": destination,
        "duration": duration,
        "preferences": preferences,
        "breakfast": breakfast
    }

    future = publisher_client.publish(topic_name, json.dumps(message_data).encode("utf-8"))
    logger.info(f"Published message to Pub/Sub: {message_data}")

    return {"status": "Request is being processed."}

app.include_router(router)