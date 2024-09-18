FROM python:3.11-slim

WORKDIR /app

RUN pip install google-cloud-pubsub

COPY main.py .

CMD ["python", "main.py"]