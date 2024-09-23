import os
import smtplib
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.cloud import pubsub_v1
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAILS_FROM_EMAIL = os.getenv('EMAILS_FROM_EMAIL')

def send_email(to_email: str, subject: str, body: str, timezone: str) -> None:
    """
    Sends an email to the specified recipient.

    Parameters:
    - to_email (str): The recipient's email address.
    - subject (str): The subject of the email.
    - body (str): The body content of the email.
    - timezone (str): The timezone to use for the timestamp.

    Returns:
    None
    """
    msg = MIMEMultipart()
    msg['From'] = EMAILS_FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(EMAILS_FROM_EMAIL, to_email, msg.as_string())
        logging.info(f"Email sent successfully to {to_email} at {datetime.now(pytz.timezone(timezone))}")
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {e}")

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    """
    Callback function that is called when a message is received from Pub/Sub.

    Parameters:
    - message (pubsub_v1.subscriber.message.Message): The Pub/Sub message received.

    Returns:
    None
    """
    event_data = json.loads(message.data.decode("utf-8"))
    to_email = event_data.get('email')
    subject = event_data.get('subject', "Default Subject")
    body = event_data.get('body', "Default email body.")
    timezone = event_data.get('timezone', 'UTC')

    if to_email:
        send_email(to_email, subject, body, timezone)
        message.ack()
        logging.info(f"Message acknowledged for email: {to_email}")
    else:
        logging.warning("No email found in the event data.")

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

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        logging.info("Subscriber stopped.")

if __name__ == "__main__":
    main()