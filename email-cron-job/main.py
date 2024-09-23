import os
import logging
from pymongo import MongoClient
from google.cloud import pubsub_v1
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def push_items_to_pubsub() -> None:
    """
    Fetches all items from MongoDB where the `send_date` is equal to today's date,
    and publishes each item to Google Pub/Sub.

    Parameters:
    None

    Returns:
    None
    """
    
    today = datetime.today().strftime('%Y-%m-%d')
    logging.info(f"Starting to push items for date: {today}")

    mongo_uri: str = os.getenv('MONGO_URI')
    mongo_db: str = os.getenv('MONGO_DB')
    mongo_collection: str = os.getenv('MONGO_COLLECTION')

    pubsub_project: str = os.getenv('PUBSUB_PROJECT')
    pubsub_topic: str = os.getenv('PUBSUB_TOPIC')

    logging.info("Connecting to MongoDB...")
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[mongo_collection]

    items = collection.find({"send_date": today})
    logging.info(f"Found {items.count()} items to publish.")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(pubsub_project, pubsub_topic)

    for item in items:
        item_json: bytes = json.dumps(item, default=str).encode("utf-8")
        publisher.publish(topic_path, data=item_json)
        logging.info(f"Published item: {item}")

    logging.info(f"Completed publishing items to Pub/Sub for date: {today}")


if __name__ == "__main__":
    push_items_to_pubsub()