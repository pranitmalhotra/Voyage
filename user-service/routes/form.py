import logging
import httpx
from fastapi import APIRouter
from typing import Dict, List
from geopy.distance import geodesic
from schemas import FormData
from core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

GOOGLE_PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"

async def fetch_non_breakfast_restaurants(preferences: Dict, attraction: str, budget: str, destination: str) -> Dict:
    """
    Fetch the first restaurant from Google Places API based on given preferences, destination, and budget.
    """
    logger.info(f"Fetching non-breakfast restaurants near {attraction}, {destination} with budget: {budget}")
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': (
            'places.displayName,places.formattedAddress,places.googleMapsUri,places.location,places.primaryType,' 
            'places.primaryTypeDisplayName,places.currentOpeningHours,places.internationalPhoneNumber,places.nationalPhoneNumber,' 
            'places.priceLevel,places.rating,places.userRatingCount,places.websiteUri,places.editorialSummary,places.dineIn,' 
            'places.goodForGroups,places.liveMusic,places.reservable,places.servesBreakfast,places.servesCocktails,places.servesDessert,' 
            'places.servesDinner,places.servesLunch,places.servesWine,nextPageToken'
        )
    }

    next_page_token = None
    first_restaurant = None

    match budget:
        case "PRICE_LEVEL_VERY_EXPENSIVE":
            price_level_text = "Very Expensively"
        case "PRICE_LEVEL_EXPENSIVE":
            price_level_text = "Expensively"
        case "PRICE_LEVEL_MODERATE":
            price_level_text = "Moderately"
        case "PRICE_LEVEL_INEXPENSIVE":
            price_level_text = "Cheaply"

    while True:
        payload = {
            "textQuery": f"Show the best {price_level_text} priced restaurants near {attraction}, {destination}",
            'pageToken': next_page_token if next_page_token else None
        }

        try:
            async with httpx.AsyncClient() as client:
                logger.info("Sending request to Google Places API...")
                response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
                data = response.json()
                logger.info("Received response from Google Places API.")
                logger.info(data)
                
                if 'error_message' in data:
                    logger.error(f"Error from Google Places API: {data['error_message']}")
                    raise ValueError(f"Error from Google Places API: {data['error_message']}")
                
                places = data.get('places', [])
                next_page_token = data.get('nextPageToken', None)

                if places:
                    first_restaurant = places[0]
                
                for place in places:
                    if (
                        place.get("priceLevel") == budget and
                        all(pref in place and place.get(pref) == val for pref, val in preferences.items())
                    ):
                        logger.info(f"Found matching restaurant: {place['displayName']}")
                        return place

                if not next_page_token:
                    logger.info("No more pages to fetch.")
                    break
        except Exception as e:
            logger.exception(f"Failed to fetch non-breakfast restaurants: {str(e)}")
            raise

    logger.warning("No matching restaurant found. Returning the first fetched restaurant.")
    return first_restaurant

async def fetch_attractions(destination: str, duration: int) -> List[Dict]:
    logger.info(f"Fetching top attractions in {destination} for duration: {duration} days")
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': (
            'places.displayName,places.formattedAddress,places.googleMapsUri,places.location,places.primaryType,' 
            'places.primaryTypeDisplayName,places.currentOpeningHours,places.internationalPhoneNumber,places.nationalPhoneNumber,' 
            'places.rating,places.userRatingCount,places.websiteUri,places.editorialSummary,places.goodForGroups,nextPageToken'
        )
    }

    results = []
    next_page_token = None

    while len(results) < (duration * 3):
        payload = {
            "textQuery": f"Top Attractions in {destination}",
            'pageToken': next_page_token if next_page_token else None
        }

        try:
            async with httpx.AsyncClient() as client:
                logger.info("Sending request to Google Places API for attractions...")
                response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
                data = response.json()
                logger.info("Received response from Google Places API for attractions.")
                logger.info(data)
                
                if 'error_message' in data:
                    logger.error(f"Error from Google Places API: {data['error_message']}")
                    raise ValueError(f"Error from Google Places API: {data['error_message']}")
                
                places = data.get('places', [])
                next_page_token = data.get('nextPageToken', None)

                for place in places:
                    results.append(place)
                    if len(results) >= (duration * 3):
                        break
                
                if not next_page_token:
                    logger.info("No more pages to fetch for attractions.")
                    break
        except Exception as e:
            logger.exception(f"Failed to fetch attractions: {str(e)}")
            raise

    logger.info(f"Returning {len(results)} attractions.")
    return results[:(duration * 3)]

async def fetch_breakfast_restaurants(attraction: str, budget: str, destination: str) -> Dict:
    logger.info(f"Fetching breakfast restaurants near {attraction}, {destination} with budget: {budget}")
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': (
            'places.displayName,places.formattedAddress,places.googleMapsUri,places.location,places.primaryType,' 
            'places.primaryTypeDisplayName,places.currentOpeningHours,places.internationalPhoneNumber,places.nationalPhoneNumber,' 
            'places.priceLevel,places.rating,places.userRatingCount,places.websiteUri,places.editorialSummary,places.dineIn,' 
            'places.goodForGroups,places.liveMusic,places.reservable,places.servesBreakfast,places.servesCocktails,' 
            'places.servesDessert,places.servesDinner,places.servesLunch,places.servesWine,nextPageToken'
        )
    }

    next_page_token = None
    preferences = {"servesBreakfast": True}
    first_restaurant = None

    match budget:
        case "PRICE_LEVEL_VERY_EXPENSIVE":
            price_level_text = "Very Expensively"
        case "PRICE_LEVEL_EXPENSIVE":
            price_level_text = "Expensively"
        case "PRICE_LEVEL_MODERATE":
            price_level_text = "Moderately"
        case "PRICE_LEVEL_INEXPENSIVE":
            price_level_text = "Cheaply"

    while True:
        payload = {
            "textQuery": f"Show {price_level_text} priced breakfast spots near {attraction}, {destination}",
            'pageToken': next_page_token if next_page_token else None
        }

        try:
            async with httpx.AsyncClient() as client:
                logger.info("Sending request to Google Places API for breakfast spots...")
                response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
                data = response.json()
                logger.info("Received response from Google Places API for breakfast spots.")
                logger.info(data)
                
                if 'error_message' in data:
                    logger.error(f"Error from Google Places API: {data['error_message']}")
                    raise ValueError(f"Error from Google Places API: {data['error_message']}")
                
                places = data.get('places', [])
                next_page_token = data.get('nextPageToken', None)

                if places:
                    first_restaurant = places[0]
                
                for place in places:
                    if (
                        place.get("priceLevel") == budget and
                        all(pref in place and place.get(pref) == val for pref, val in preferences.items())
                    ):
                        logger.info(f"Found matching breakfast restaurant: {place['displayName']}")
                        return place

                if not next_page_token:
                    logger.info("No more pages to fetch for breakfast spots.")
                    break
        except Exception as e:
            logger.exception(f"Failed to fetch breakfast restaurants: {str(e)}")
            raise

    logger.warning("No matching breakfast restaurant found. Returning the first fetched restaurant.")
    return first_restaurant

async def cluster_attractions(attractions_list: List[Dict], breakfast: str, budget: str, preferences: Dict, destination: str) -> List[Dict]:
    logger.info("Clustering attractions for the itinerary.")
    
    def distance(p1, p2):
        return geodesic((p1['location']['latitude'], p1['location']['longitude']),
                        (p2['location']['latitude'], p2['location']['longitude'])).km

    itineraries = []

    while len(attractions_list) >= 2:
        attraction1 = attractions_list.pop(0)
        distances = [(distance(attraction1, attraction2), attraction2) for attraction2 in attractions_list]
        closest_attraction = min(distances, key=lambda x: x[0])[1]
        attractions_list.remove(closest_attraction)

        logger.info(f"Selected attractions: {attraction1['displayName']} and {closest_attraction['displayName']}")

        if breakfast == "yes":
            breakfast_restaurant = await fetch_breakfast_restaurants(attraction1['displayName'], budget, destination)
            non_breakfast_restaurant = await fetch_non_breakfast_restaurants(preferences, attraction1['displayName'], budget, destination)
            logger.info(f"Found breakfast restaurant: {breakfast_restaurant['displayName']} and non-breakfast restaurant: {non_breakfast_restaurant['displayName']}")
            
            itineraries.append({
                "attraction1": attraction1,
                "attraction2": closest_attraction,
                "breakfast_restaurant": breakfast_restaurant,
                "non_breakfast_restaurant": non_breakfast_restaurant
            })
        else:
            non_breakfast_restaurant1 = await fetch_non_breakfast_restaurants(preferences, attraction1['displayName'], budget, destination)
            non_breakfast_restaurant2 = await fetch_non_breakfast_restaurants(preferences, closest_attraction['displayName'], budget, destination)
            logger.info(f"Found non-breakfast restaurants: {non_breakfast_restaurant1['displayName']} and {non_breakfast_restaurant2['displayName']}")
            
            itineraries.append({
                "attraction1": attraction1,
                "attraction2": closest_attraction,
                "non_breakfast_restaurant1": non_breakfast_restaurant1,
                "non_breakfast_restaurant2": non_breakfast_restaurant2
            })

    logger.info("Finished clustering attractions.")
    return itineraries

@router.post("/submit")
async def submit(form_data: FormData):
    logger.info(f"Received form data for generating itinerary: {form_data}")
    destination = form_data.destination
    duration = int(form_data.duration)
    breakfast = form_data.breakfast
    budget = form_data.budget
    preferences = form_data.preferences

    attractions_list = await fetch_attractions(destination, duration)
    logger.info(f"Fetched {len(attractions_list)} attractions.")

    itinerary = await cluster_attractions(attractions_list, breakfast, budget, preferences, destination)
    logger.info(f"Generated itinerary: {itinerary}")

    return itinerary
