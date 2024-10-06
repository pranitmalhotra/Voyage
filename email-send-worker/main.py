import os
import json
import logging
from google.cloud import pubsub_v1
from pymongo import MongoClient
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def process_event(message: pubsub_v1.subscriber.message.Message) -> None:
    """
    Processes a message received from Google Pub/Sub.

    Parameters:
    - message: The Pub/Sub message received.

    Returns:
    None
    """
    event_data = json.loads(message.data.decode("utf-8"))
    start_date = event_data.get('startDate')
    itinerary = event_data.get('itinerary', {})
    
    formatted_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%y')
    subject = f"Your Itinerary for {formatted_date}"

    body_parts = []
    for meal, details in itinerary.items():
        body_parts.append(f"{meal.capitalize()}: {details['name']}")
        body_parts.append(f"- Address: {details['address']}")
        body_parts.append(f"- Google Maps: {details['google_maps']}")
        body_parts.append(f"- Phone: {details['phone']}")
        body_parts.append(f"- Rating: {details['rating']} ({details['reviews']} reviews)")
        if 'website' in details:
            body_parts.append(f"- Website: {details['website']}")
        body_parts.append("")

    body = "\n".join(body_parts)

    event_record = {
        "itinerary": itinerary,
        "start_date": start_date,
        "created_at": datetime.now(pytz.utc)
    }
    
    collection.insert_one(event_record)
    logging.info(f"Inserted event into MongoDB: {event_record}")

    message.ack()
    logging.info(f"Message acknowledged for itinerary starting on: {start_date}")

def main() -> None:
    """
    Main function that sets up the Pub/Sub subscriber and starts listening for messages.

    Returns:
    None
    """
    project_id = os.getenv('PUBSUB_PROJECT_ID')
    subscription_id = os.getenv('PUBSUB_SUBSCRIPTION_ID')

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    logging.info(f"Listening for messages on {subscription_path}...\n")

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_event)

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        logging.info("Subscriber stopped.")

if __name__ == "__main__":
    main()