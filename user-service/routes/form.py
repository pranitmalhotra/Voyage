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

async def fetch_non_breakfast_restaurants(preferences: Dict, destination: str, budget: str, duration: int) -> List[Dict]:
    """
    Fetch restaurants from Google Places API based on given preferences, destination, and budget.
    
    Args:
        preferences (Dict): A dictionary containing preferences for filtering restaurants.
        destination (str): The location where the search is performed.
        budget (str): The price level of the restaurant (e.g., PRICE_LEVEL_VERY_EXPENSIVE, PRICE_LEVEL_EXPENSIVE, etc.).
        no_of_results (int): The maximum number of restaurants to fetch (default is 10).
        
    Returns:
        List[Dict]: A list of restaurant details that match the preferences and budget.
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

    results = []
    next_page_token = None

    match budget:
        case "PRICE_LEVEL_VERY_EXPENSIVE":
            price_level_text = "Very Expensively"
        case "PRICE_LEVEL_EXPENSIVE":
            price_level_text = "Expensively"
        case "PRICE_LEVEL_MODERATE":
            price_level_text = "Moderately"
        case "PRICE_LEVEL_INEXPENSIVE":
            price_level_text = "Cheaply"

    while len(results) < (duration * 2):
        payload = {
            "textQuery": f"{price_level_text} priced restaurants in {destination}",
            'pageToken': next_page_token if next_page_token else None
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
            data = response.json()
            
            if 'error_message' in data:
                raise ValueError(f"Error from Google Places API: {data['error_message']}")
            
            places = data.get('places', [])
            next_page_token = data.get('nextPageToken', None)
            
            for place in places:
                if (
                    place.get("priceLevel") == budget and 
                    all(pref in place and place.get(pref) == val for pref, val in preferences.items())
                ):
                    results.append(place)
                
                if len(results) >= (duration * 2):
                    break
            
            if not next_page_token:
                break

    return results[:(duration * 2)]

async def fetch_attractions(destination: str, duration: int) -> List[Dict]:
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': settings.GOOGLE_PLACES_API_KEY,
        'X-Goog-FieldMask': (
            'places.displayName,places.formattedAddress,places.googleMapsUri,places.location,places.primaryType,'
            'places.primaryTypeDisplayName,places.currentOpeningHours,places.internationalPhoneNumber,'
            'places.nationalPhoneNumber,places.rating,places.userRatingCount,places.websiteUri,'
            'places.editorialSummary,places.goodForGroups'
        )
    }

    results = []
    next_page_token = None

    while len(results) < (duration * 3):
        payload = {
            "textQuery": f"Top Attractions in {destination}",
            'pageToken': next_page_token if next_page_token else None
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
            data = response.json()
            
            if 'error_message' in data:
                raise ValueError(f"Error from Google Places API: {data['error_message']}")
            
            places = data.get('places', [])
            next_page_token = data.get('nextPageToken', None)
            
            for place in places:
                results.append(place)
                
                if len(results) >= (duration * 3):
                    break
            
            if not next_page_token:
                break

    return results[:(duration * 3)]

async def fetch_breakfast_restaurants(non_breakfast_restaurants_list:str, destination: str, budget: int, duration: int) -> List[Dict]:
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

    preferences = {"servesBreakfast": True}

    match budget:
        case "PRICE_LEVEL_VERY_EXPENSIVE":
            price_level_text = "Very Expensively"
        case "PRICE_LEVEL_EXPENSIVE":
            price_level_text = "Expensively"
        case "PRICE_LEVEL_MODERATE":
            price_level_text = "Moderately"
        case "PRICE_LEVEL_INEXPENSIVE":
            price_level_text = "Cheaply"

    while len(results) < duration:
        payload = {
            "textQuery": f"{price_level_text} priced restaurants in {destination}",
            'pageToken': next_page_token if next_page_token else None
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GOOGLE_PLACES_API_URL, headers=headers, json=payload)
            data = response.json()
            
            if 'error_message' in data:
                raise ValueError(f"Error from Google Places API: {data['error_message']}")
            
            places = data.get('places', [])
            next_page_token = data.get('nextPageToken', None)
            
            for place in places:
                if (
                    place.get("priceLevel") == budget and 
                    all(pref in place and place.get(pref) == val for pref, val in preferences.items()) and place not in non_breakfast_restaurants_list
                ):
                    results.append(place)
                
                if len(results) >= duration:
                    break
            
            if not next_page_token:
                break

    return results[:duration]

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
    duration = data.duration

    preferences = data.preferences
    preferences["dineIn"] = True

    non_breakfast_restaurants_list = await fetch_non_breakfast_restaurants(preferences, destination, budget, duration)
    attractions_list = await fetch_attractions(destination, duration)

    if (data.breakfast == 'yes'):
        breakfast_restaurants_list = await fetch_breakfast_restaurants(non_breakfast_restaurants_list, destination, budget, duration)
        restaurants_list = breakfast_restaurants_list + non_breakfast_restaurants_list
    else:
        restaurants_list = non_breakfast_restaurants_list

    sorted_restaurants_list = sort_list_using_bayesian_average(restaurants_list)
    sorted_attractions_list = sort_list_using_bayesian_average(attractions_list)

    daily_itineraries = cluster_places(sorted_restaurants_list, sorted_attractions_list, duration)

    return {
        "daily_itineraries": daily_itineraries
    }
