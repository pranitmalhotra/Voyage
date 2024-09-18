from google.cloud import pubsub_v1

def callback(message):
    try:
        data = message.data.decode('utf-8')
        print(f"Received: {data}")
        message.ack()
    except Exception as e:
        print(f"Failed to process message: {e}")

def main():
    project_id = 'natural-aria-435207-e6'
    subscription_id = 'my-subscription'
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...\n")
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

if __name__ == "__main__":
    main()