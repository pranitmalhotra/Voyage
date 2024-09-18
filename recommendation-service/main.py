from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from google.cloud import pubsub_v1
import json
import logging
import base64

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a Pydantic model to validate incoming messages
class PubSubMessage(BaseModel):
    message: dict

@app.post("/pubsub")
async def pubsub_endpoint(request: Request):
    try:
        # Parse the incoming request body
        body = await request.json()
        pubsub_message = PubSubMessage(message=body.get('message', {}))
        
        # Extract message data
        data = pubsub_message.message.get('data', '')
        data_decoded = base64.b64decode(data).decode('utf-8')
        logging.info(f"Received message: {data_decoded}")
        
        # Process message
        process_message(data_decoded)
        
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Failed to process message: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def process_message(data):
    try:
        # Implement your message processing logic here
        print(f"Processing message: {data}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")
