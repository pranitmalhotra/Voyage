# Voyage

## Reasons for choosing Microservices Architecture
- Copy from Google docs

## Architecture
![Architecture](https://github.com/pranitmalhotra/Voyage/blob/main/assets/arch.png)

1. **user-service**: The only service exposed to the client. It handles validating the client's input and pushes the client's request into **pubsub 1**.
2. **pubsub 1**: Manages two topics to facilitate communication between services. In one topic, the publisher is the **user-service**, while in the other, the **recommendation-worker** acts as the publisher.
3. **recommendation-worker**: Responsible for generating itineraries. Once generated, it publishes the itineraries to one of **pubsub 1**'s topics and stores them in **mongodb 1**.
4. **mongodb 1**: Stores pre-generated itineraries.
5. **cron job 1**: Periodically fetches the most popular itineraries from **mongodb 1** and stores them in **redis**.
6. **redis**: Used by the **user-service** to check if an itinerary matching the user's preferences already exists.
7. **email-service**: Listens to **pubsub 1** and pulls events as they are available. It processes these events and schedules emails to be sent to users on specific days.
8. **mongodb 2**: Stores emails, waiting to be read by **cron job 2**.
9. **cron job 2**: Periodically reads emails from **mongodb 2** and adds them to a queue for the **email-send-worker** to process.
10. **pubsub 2**: Facilitates communication between the **email-send-worker** and **cron job 2**.
11. **email-send-worker**: Pulls events from **pubsub 2** and sends the emails.

## Why a Microservices architecture?
Microservices architecture was chosen because of three main reasons:
- **Production-First Design**: The project needed to be built with deployment and maintenance in mind, making microservices an ideal choice for creating a system that is easy to manage in production environments.
- **Scalability**: Each microservice component can be scaled independently. For instance, the number of instances required for the user-service may differ significantly from those needed for the recommendation-worker, allowing for more efficient resource management.
- **Event-Driven Architecture**: Microservices facilitate the use of event-driven architecture. In this setup, a single publisher (recommendation-worker) can serve multiple subscribers (user-service and email-service), eliminating the need for redundant API calls.

## Deployment
The complete project has been hosted on Google Cloud using the following services:
- Google Cloud Run
- Google Cloud Run Functions
- Google Cloud Build
- Google PubSub
- Google Cloud Run Jobs

## Things That Can Be Improved
1. **Implementing Long Polling**: This can enhance the user experience by displaying a progress bar while the itinerary is being generated. In the background, the frontend can periodically poll the backend to check for updates.
2. **Adding a Signup/Signin Flow**: This would be valuable if we plan to implement user-specific personalization in the future.
3. **Setting Up a Reverse Proxy Server**: This adds security by exposing only a single port and enabling features like rate limiting.
4. **Using a Load Balancer**: A load balancer would distribute traffic between multiple instances, improving scalability and performance.

## Links

Writeup: [Link to Writeup](https://docs.google.com/document/d/1ddGqoxPCg2mGAPmAHVdBwyy3xyzsbPpAmj71BWF22qE/edit#heading=h.mf7baygpiz8t)

Video: [Link to Video](https://vimeo.com/1001941117)
