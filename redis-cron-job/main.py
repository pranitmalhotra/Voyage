import os
import json
import logging
import schedule
import time
from pymongo import MongoClient
import redis

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def map_itinerary_to_preferences(itinerary: dict, user_preferences: dict) -> bool:
    """
    Maps an itinerary to user preferences.

    Parameters:
    - itinerary (dict): The itinerary JSON object.
    - user_preferences (dict): The user preferences JSON object.

    Returns:
    bool: True if the itinerary matches the user preferences, False otherwise.
    """
    preferred_tags = user_preferences.get('preferred_tags', [])
    itinerary_tags = itinerary.get('tags', [])
    
    return any(tag in itinerary_tags for tag in preferred_tags)

def fetch_popular_itineraries() -> None:
    """
    Fetches popular itineraries from MongoDB and stores them in Redis.

    Returns:
    None
    """

    popular_itineraries = collection.find().sort("no_of_calls", -1).limit(10)

    user_preferences = {
        "preferred_tags": ["goodForGroups", "outdoorMusic"]
    }

    for itinerary in popular_itineraries:
        if map_itinerary_to_preferences(itinerary, user_preferences):
            redis_key = f"itinerary:{itinerary['_id']}"
            redis_client.set(redis_key, json.dumps(itinerary))
            logging.info(f"Stored itinerary in Redis: {redis_key}")

def schedule_itinerary_fetch() -> None:
    """
    Schedules the fetch_popular_itineraries function to run periodically.

    Returns:
    None
    """
    schedule.every(1).hour.do(fetch_popular_itineraries)
    logging.info("Scheduled itinerary fetch every hour.")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_itinerary_fetch()