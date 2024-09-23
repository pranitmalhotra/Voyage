import os
import logging
import json
import httpx
from google.cloud import pubsub_v1
from typing import Dict, List
from core.config import settings
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_client = MongoClient(settings.MONGO_URI)
db = mongo_client[settings.MONGO_DB_NAME]
itineraries_collection = db.itineraries

GOOGLE_PLACES_API_KEY = settings.GOOGLE_PLACES_API_KEY
GOOGLE_PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

subscriber_client = pubsub_v1.SubscriberClient()
subscription_name = f"projects/{settings.GOOGLE_PROJECT_ID}/subscriptions/{settings.GOOGLE_PUBSUB_SUBSCRIPTION}"

async def fetch_places(destination: str, preferences: Dict) -> List[Dict]:
    """
    Fetches places from the Google Places API based on the destination and preferences.

    Parameters:
        destination (str): The geographical location to search for places.
        preferences (Dict): A dictionary of preferences to filter the places.

    Returns:
        List[Dict]: A list of places retrieved from the Google Places API.
    """
    params = {
        "location": destination,
        "radius": 5000,
        "key": GOOGLE_PLACES_API_KEY,
        **preferences
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_PLACES_API_URL, params=params)
        response.raise_for_status()
        return response.json().get("results", [])

async def generate_itinerary(data: Dict) -> Dict:
    """
    Generates an itinerary based on the provided data by fetching places.

    Parameters:
        data (Dict): The input data containing destination and preferences.

    Returns:
        Dict: A dictionary containing the fetched places as itineraries.
    """
    destination = data["destination"]
    preferences = data["preferences"]

    places = await fetch_places(destination, preferences)

    return {"itineraries": places}

async def callback(message):
    """
    Callback function to process incoming messages from Google Pub/Sub.

    Parameters:
        message: The Pub/Sub message containing itinerary request data.
    """
    logger.info(f"Received message: {message.data}")
    data = json.loads(message.data)

    try:
        itinerary_data = await generate_itinerary(data)
        
        itineraries_collection.insert_one(itinerary_data)
        logger.info("Itinerary saved to MongoDB.")
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
    finally:
        message.ack()

def start_consuming():
    """
    Starts listening for messages on the specified Pub/Sub subscription.
    """
    future = subscriber_client.subscribe(subscription_name, callback=callback)
    logger.info(f"Listening for messages on {subscription_name}.")
    try:
        future.result()
    except Exception as e:
        logger.error(f"Listening failed: {e}")

if __name__ == "__main__":
    start_consuming()