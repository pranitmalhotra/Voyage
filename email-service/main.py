import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime
import pytz

from core.config import settings

to_email = 'pranitmalhotra100@gmail.com'
subject = 'Subject of the Email'
body = 'This is the body of the email.'

timezone = pytz.timezone('Asia/Kolkata')

def send_email():
    msg = MIMEMultipart()
    msg['From'] = settings.EMAILS_FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, msg.as_string())
        print(f"Email sent successfully at {datetime.now(timezone)}")
    except Exception as e:
        print(f"Failed to send email: {e}")

scheduled_time = "2024-09-17 14:40"
def schedule_email():
    now = datetime.now(timezone).strftime('%Y-%m-%d %H:%M')
    if now == scheduled_time:
        send_email()
        return schedule.CancelJob

schedule.every(1).minutes.do(schedule_email)

print(f"Email scheduled for {scheduled_time} ({timezone})")

while True:
    schedule.run_pending()
    time.sleep(1)