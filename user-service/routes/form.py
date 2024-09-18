import httpx
import json
import numpy as np

from google.cloud import pubsub_v1
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
from typing import Dict, List

# from core.db import get_db
from schemas import FormData
from core.config import settings

router = APIRouter()

GOOGLE_PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"

# no of results will be decided by the caller function
async def fetch_places(preferences: Dict, destination: str, budget: str, no_of_results: int = 10) -> List[Dict]:
    # Need to add a appropriate docstring
    # OR duration can be something that can be computed by a function inside of this function

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

    results = []
    next_page_token = None

    match budget:
        case "PRICE_LEVEL_VERY_EXPENSIVE":
            price_level = "Very Expensively"
        case "PRICE_LEVEL_EXPENSIVE":
            price_level = "Expensively"
        case "PRICE_LEVEL_MODERATE":
            price_level = "Moderately"
        case "PRICE_LEVEL_INEXPENSIVE":
            price_level = "Cheaply"

    while len(results) < no_of_results:
        payload = {
            "textQuery": f"{price_level} priced restaurants in {destination}",
            'pageToken': next_page_token if next_page_token else None
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
            data = response.json()
            print(data)
            
            if 'error_message' in data:
                raise ValueError(f"Error from Google Places API: {data['error_message']}")
            
            places = data.get('places', [])
            next_page_token = data.get('nextPageToken', None)
            
            for place in places:
                # if all(place.get(key) == value for key, value in preferences.items() if key in place) and place.get("priceLevel") == budget:
                if place.get("priceLevel") == budget:
                    results.append(place)
                
                if len(results) >= no_of_results:
                    break
            
            if not next_page_token:
                break

    return results[:no_of_results]


# function that decides the no of places to fetch and the logic for that.

async def get_restaurants_by_price_level(location: str, budget: str):
    """
    Fetch place details from Google Places API based on the query string and budget.

    Args:
        query: The search term to query places.

    Returns:
        The response from the Google Places API.
    """

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

    match budget:
        case "PRICE_LEVEL_VERY_EXPENSIVE":
            price_level = "Very Expensively"
        case "PRICE_LEVEL_EXPENSIVE":
            price_level = "Expensively"
        case "PRICE_LEVEL_MODERATE":
            price_level = "Moderately"
        case "PRICE_LEVEL_INEXPENSIVE":
            price_level = "Cheaply"

    payload = {
        "textQuery": f"{price_level} priced restaurants in {location}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
        data = response.json()

        restaurants_list = []
        if "places" in data:
            for place in data['places']:
                restaurant_details = {
                    'display_name': place.get('displayName', {}).get('text'),
                    'formatted_address': place.get('formattedAddress'),
                    'google_maps_uri': place.get('googleMapsUri'),
                    'location': {
                        'latitude': place.get('location', {}).get('latitude'),
                        'longitude': place.get('location', {}).get('longitude')
                    },
                    'primary_type': place.get('primaryType'),
                    'primary_type_display_name': place.get('primaryTypeDisplayName', {}).get('text'),
                    'current_opening_hours': place.get('currentOpeningHours', {}).get('openNow'),
                    'international_phone_number': place.get('internationalPhoneNumber'),
                    'national_phone_number': place.get('nationalPhoneNumber'),
                    'price_level': place.get('priceLevel'),
                    'rating': place.get('rating'),
                    'user_rating_count': place.get('userRatingCount'),
                    'website_uri': place.get('websiteUri'),
                    'editorial_summary': place.get('editorialSummary', {}).get('text'),
                    'dine_in': place.get('dineIn', False),
                    'good_for_groups': place.get('goodForGroups', False),
                    'live_music': place.get('liveMusic', False),
                    'reservable': place.get('reservable', False),
                    'serves_breakfast': place.get('servesBreakfast', False),
                    'serves_cocktails': place.get('servesCocktails', False),
                    'serves_dessert': place.get('servesDessert', False),
                    'serves_dinner': place.get('servesDinner', False),
                    'serves_lunch': place.get('servesLunch', False),
                    'serves_wine': place.get('servesWine', False)
                }
                restaurants_list.append(restaurant_details)

    return restaurants_list
    
async def get_attractions_details(location: str):
    """
    Fetch place details from Google Places API based on the query string.

    Args:
        query: The search term to query places.

    Returns:
        The response from the Google Places API.
    """
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': (
            'places.displayName,places.formattedAddress,places.googleMapsUri,places.location,places.primaryType,'
            'places.primaryTypeDisplayName,places.currentOpeningHours,places.internationalPhoneNumber,'
            'places.nationalPhoneNumber,places.priceLevel,places.rating,places.userRatingCount,places.websiteUri,'
            'places.editorialSummary,places.goodForGroups'
        )
    }

    payload = {
        "textQuery": f"Top Attractions in {location}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
        data = response.json()

    attractions_list = []
    if "places" in data:
        for place in data['places']:
            attraction_details = {
                'display_name': place.get('displayName', {}).get('text'),
                'formatted_address': place.get('formattedAddress'),
                'google_maps_uri': place.get('googleMapsUri'),
                'location': {
                        'latitude': place.get('location', {}).get('latitude'),
                        'longitude': place.get('location', {}).get('longitude')
                    },
                'primary_type': place.get('primaryType'),
                'primary_type_display_name': place.get('primaryTypeDisplayName', {}).get('text'),
                'current_opening_hours': place.get('currentOpeningHours', {}).get('openNow'),
                'international_phone_number': place.get('internationalPhoneNumber'),
                'national_phone_number': place.get('nationalPhoneNumber'),
                'rating': place.get('rating'),
                'user_rating_count': place.get('userRatingCount'),
                'website_uri': place.get('websiteUri'),
                'editorial_summary': place.get('editorialSummary', {}).get('text')
            }
            attractions_list.append(attraction_details)

    return attractions_list

from typing import List, Dict

def sort_list_using_bayesian_average(places: List[Dict]) -> List[Dict]:
    """
    Sorts the list of places using the Bayesian Average formula.
    
    Args:
        places: A list of dictionaries, each representing a place with 'rating' and 'user_rating_count'.
        m: The minimum number of ratings to consider for Bayesian Average.

    Returns:
        The list sorted in descending order based on the Bayesian Average score.
    """
    total_rating_sum = sum(place.get('rating', 0) * place.get('user_rating_count', 0) for place in places)
    total_ratings = sum(place.get('user_rating_count', 0) for place in places)
    
    C = total_rating_sum / total_ratings if total_ratings > 0 else 0
    m = 100

    for place in places:
        R = place.get('rating', 0)
        V = place.get('user_rating_count', 0)
        bayesian_average = ((V * R) + (m * C)) / (V + m)
        place['bayesian_average'] = bayesian_average

    return sorted(places, key=lambda x: x['bayesian_average'], reverse=True)

def filter_restaurants_by_budget(top_restaurants: List[Dict], budget: str) -> List[Dict]:
    """
    Filters top restaurants based on the provided budget level.
    
    Args:
        top_restaurants: List of top restaurants with price level information.
        budget: The budget level provided by the user. Options are:
            'PRICE_LEVEL_VERY_EXPENSIVE', 'PRICE_LEVEL_EXPENSIVE', 
            'PRICE_LEVEL_MODERATE', 'PRICE_LEVEL_INEXPENSIVE'.
    
    Returns:
        A list of restaurants that adhere to the user's budget.
    """
    budget_levels = {
        'PRICE_LEVEL_VERY_EXPENSIVE': 4,
        'PRICE_LEVEL_EXPENSIVE': 3,
        'PRICE_LEVEL_MODERATE': 2,
        'PRICE_LEVEL_INEXPENSIVE': 1
    }

    budget_level = budget_levels.get(budget)
    
    filtered_restaurants = [
        restaurant for restaurant in top_restaurants 
        if restaurant.get('priceLevel') is not None and restaurant['priceLevel'] <= budget_level
    ]
    
    return filtered_restaurants

def publish_to_pubsub(message: dict):
    project_id = "natural-aria-435207-e6"
    topic_id = "my-topic"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data)

    print(f"Published message ID: {future.result()}")

def cluster_places(top_restaurants: List[Dict], top_attractions: List[Dict], duration: int) -> List[Dict[str, List[Dict]]]:
    """
    Cluster top attractions and restaurants into groups for daily itineraries.
    
    Args:
        top_restaurants: List of top restaurants with latitude and longitude.
        top_attractions: List of top attractions with latitude and longitude.
        duration: The number of days to plan the itinerary.
    
    Returns:
        A list of dictionaries, each representing a cluster with attractions and restaurants for a day.
    """
    places = top_restaurants + top_attractions
    coordinates = np.array([(place['location']['latitude'], place['location']['longitude']) for place in places])

    num_clusters = duration
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(coordinates)
    
    clusters = [[] for _ in range(num_clusters)]
    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(places[idx])

    daily_itineraries = []
    for cluster in clusters:
        attractions = [place for place in cluster if place in top_attractions][:2]
        restaurants = [place for place in cluster if place in top_restaurants][:3]

        if len(attractions) < 2:
            attractions += [place for place in top_attractions if place not in attractions][:2-len(attractions)]
        if len(restaurants) < 3:
            restaurants += [place for place in top_restaurants if place not in restaurants][:3-len(restaurants)]

        daily_itineraries.append({
            "attractions": attractions,
            "restaurants": restaurants
        })
    
    # publish_to_pubsub(daily_itineraries)

    return daily_itineraries

@router.post("/submit")
# async def submit_form(data: FormData, db: Session = Depends(get_db)):
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

    # restaurants_list = await get_restaurants_by_price_level(data.destination, budget)
    # attractions_list = await get_attractions_details(data.destination)

    # sorted_restaurants_list = sort_list_using_bayesian_average(restaurants_list)
    # sorted_attractions_list = sort_list_using_bayesian_average(attractions_list)
    # duration = data.duration

    # daily_itineraries = cluster_places(sorted_restaurants_list, sorted_attractions_list, duration)

    daily_itineraries = await fetch_places({}, destination, budget, 10)

    return {
        "daily_itineraries": daily_itineraries
    }
