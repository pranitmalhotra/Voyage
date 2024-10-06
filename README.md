# Voyage

## Architecture
![Architecture](https://github.com/pranitmalhotra/Voyage/blob/main/assets/arch.png)

### Itinerary Generator Section

The Itinerary Generator section is responsible for creating personalized travel itineraries based on user preferences, budget, and duration. 
1. **app service**: When the client service sends a request, the app service generates the itinerary using the Google Places API to fetch relevant attractions and restaurants.
2. The **database** instance has three tables:
   - Locations Table: Stores information about various locations.
   - Attraction Table: Holds details about each attraction.
   - Restaurants Table: Contains data on restaurants located near specific attractions.
3. **Redis** is employed to cache attractions and restaurants based on location. This allows quick querying tailored to the user's preferences and budget.

### Scheduled Email Section

The Scheduled Email section manages the generation and dispatch of itinerary-related emails.
1. **email accept service**: Receives the start date and generated itinerary from the app service. It prepares the content for each scheduled email and pushes it to the email write queue.
2. **email write service**: Writes scheduled emails into the database based on availability. 
3. The **database** is structured to store scheduled emails with an index on the scheduled date, enhancing read speed.
4. **email schedule cron**: Runs daily to add new scheduled emails to the email send queue.
5. **email send worker**: Pulls emails from the queue based on availability and sends them out to users.

## Future Improvements
1. Adding **rate limiting** between the Google Places API and the app service.
2. Implementing a **load balancer** for reverse proxying and balancing load between multiple instances
3. Adding **centralized logging** using the ELK stack

## Links

Writeup: [Link to Writeup](https://docs.google.com/document/d/1ddGqoxPCg2mGAPmAHVdBwyy3xyzsbPpAmj71BWF22qE/edit#heading=h.mf7baygpiz8t)
