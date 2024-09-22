import httpx
import logging

from fastapi import APIRouter
from typing import Dict, List
from geopy.distance import geodesic

from schemas import FormData
from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

GOOGLE_PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"

async def fetch_non_breakfast_restaurants(preferences: Dict, attraction: str, budget: str, destination: str) -> Dict:
    """
    Fetch the first restaurant from Google Places API based on given preferences, destination, and budget.
    
    Args:
        preferences (Dict): A dictionary containing preferences for filtering restaurants.
        destination (str): The location where the search is performed.
        budget (str): The price level of the restaurant (e.g., PRICE_LEVEL_VERY_EXPENSIVE, PRICE_LEVEL_EXPENSIVE, etc.).
        
    Returns:
        Dict: The first restaurant details that match the preferences and budget, or the first fetched restaurant if none qualify.
    """
    logger.info("Fetching non-breakfast restaurants for attraction: %s, destination: %s, budget: %s", attraction, destination, budget)

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': (
            'places.displayName,places.formattedAddress,places.googleMapsUri,places.location,places.primaryType,'
            'places.primaryTypeDisplayName,places.currentOpeningHours,places.internationalPhoneNumber,'
            'places.nationalPhoneNumber,places.priceLevel,places.rating,places.userRatingCount,places.websiteUri,'
            'places.editorialSummary,places.dineIn,places.goodForGroups,places.liveMusic,places.reservable,'
            'places.servesBreakfast,places.servesCocktails,places.servesDessert,places.servesDinner,'
            'places.servesLunch,places.servesWine,nextPageToken'
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

        logger.info("Sending request to Google Places API with payload: %s", payload)

        async with httpx.AsyncClient() as client:
            response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
            data = response.json()

            if 'error_message' in data:
                logger.error("Error from Google Places API: %s", data['error_message'])
                raise ValueError(f"Error from Google Places API: {data['error_message']}")
            
            places = data.get('places', [])
            next_page_token = data.get('nextPageToken', None)

            if places:
                first_restaurant = places[0]
                logger.info("Found restaurant: %s", first_restaurant)
            
            for place in places:
                if (
                    place.get("priceLevel") == budget and
                    all(pref in place and place.get(pref) == val for pref, val in preferences.items())
                ):
                    logger.info("Found matching restaurant: %s", place)
                    return place

            if not next_page_token:
                break
    
    logger.info("Returning first restaurant: %s", first_restaurant)
    return first_restaurant

async def fetch_attractions(destination: str, duration: int) -> List[Dict]:
    logger.info("Fetching attractions for destination: %s with duration: %d", destination, duration)
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': (
            'places.displayName,places.formattedAddress,places.googleMapsUri,places.location,places.primaryType,'
            'places.primaryTypeDisplayName,places.currentOpeningHours,places.internationalPhoneNumber,'
            'places.nationalPhoneNumber,places.rating,places.userRatingCount,places.websiteUri,'
            'places.editorialSummary,places.goodForGroups,nextPageToken'
        )
    }

    results = []
    next_page_token = None

    while len(results) < (duration * 3):
        payload = {
            "textQuery": f"Top Attractions in {destination}",
            'pageToken': next_page_token if next_page_token else None
        }

        logger.info("Sending request to Google Places API with payload: %s", payload)

        async with httpx.AsyncClient() as client:
            response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
            data = response.json()
            
            if 'error_message' in data:
                logger.error("Error from Google Places API: %s", data['error_message'])
                raise ValueError(f"Error from Google Places API: {data['error_message']}")
            
            places = data.get('places', [])
            next_page_token = data.get('nextPageToken', None)
            
            for place in places:
                results.append(place)
                logger.info("Added place to results: %s", place)
                
                if len(results) >= (duration * 3):
                    break
            
            if not next_page_token:
                break
    
    logger.info("Returning attractions list with count: %d", len(results))
    return results[:(duration * 3)]

async def fetch_breakfast_restaurants(attraction: str, budget: str, destination: str) -> Dict:
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': (
            'places.displayName,places.formattedAddress,places.googleMapsUri,places.location,places.primaryType,'
            'places.primaryTypeDisplayName,places.currentOpeningHours,places.internationalPhoneNumber,'
            'places.nationalPhoneNumber,places.priceLevel,places.rating,places.userRatingCount,places.websiteUri,'
            'places.editorialSummary,places.dineIn,places.goodForGroups,places.liveMusic,places.reservable,'
            'places.servesBreakfast,places.servesCocktails,places.servesDessert,places.servesDinner,'
            'places.servesLunch,places.servesWine,nextPageToken'
        )
    }

    logger.info("Fetching breakfast restaurants for attraction: %s, destination: %s, budget: %s", attraction, destination, budget)

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

        async with httpx.AsyncClient() as client:
            response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
            data = response.json()

            if 'error_message' in data:
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
                    return place

            if not next_page_token:
                break

    return first_restaurant

async def cluster_attractions(attractions_list: List[Dict], breakfast: str, budget: str, preferences: Dict, destination: str) -> List[Dict]:
    """
    Cluster attractions based on proximity and apply breakfast conditions.

    Args:
        attractions_list: List of places with latitude, longitude, and other details.
        breakfast: Whether breakfast is provided ('yes' or 'no').

    Returns:
        A list of processed restaurants based on the clustering.
    """
    
    def distance(p1, p2):
        return geodesic((p1['location']['latitude'], p1['location']['longitude']),
                        (p2['location']['latitude'], p2['location']['longitude'])).kilometers

    clusters = []
    itinerary = []
    visited = set()
    
    for i in range(len(attractions_list)):
        if i in visited:
            continue
        cluster = [attractions_list[i]]
        visited.add(i)
        
        distances = sorted([(distance(attractions_list[i], attractions_list[j]), j) 
                            for j in range(len(attractions_list)) if j not in visited])
        for dist, j in distances[:2]:
            cluster.append(attractions_list[j])
            visited.add(j)
        
        if len(cluster) == 3:
            clusters.append(cluster)

    for cluster in clusters:
        restaurants = []
        if breakfast == 'yes':
            for attraction in cluster[1:]:
                result_B = await fetch_non_breakfast_restaurants(preferences, attraction["displayName"]["text"], budget, destination)
                restaurants.append(result_B if result_B else None)
        else:
            result_A = await fetch_breakfast_restaurants(cluster[0]["displayName"]["text"], budget, destination)
            restaurants.append(result_A if result_A else None)
            
            for attraction in cluster[1:]:
                result_B = await fetch_non_breakfast_restaurants(preferences, attraction["displayName"]["text"], budget, destination)
                restaurants.append(result_B if result_B else None)

        itinerary_item = {'attractions': cluster, "restaurants": restaurants}
        itinerary.append(itinerary_item)
    
    return itinerary

@router.post("/submit")
async def submit_form(data: FormData):
    """
    Endpoint to handle form submission.

    Args:
        data: The validated form data.
        db: The database session.

    Returns:
        A success message upon successful form submission.
    """

    budget = data.budget
    destination = data.destination
    duration = data.duration

    preferences = data.preferences
    preferences["dineIn"] = True
    breakfast = data.breakfast

    attractions_list = await fetch_attractions(destination, duration)
    daily_itineraries = await cluster_attractions(attractions_list, breakfast, budget, preferences, destination)

    return {
        "daily_itineraries": daily_itineraries
    }
