import httpx
import numpy as np

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans

from core.db import get_db
from schemas import FormData
from core.config import settings

router = APIRouter()

GOOGLE_PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"

async def get_restaurants_details(location: str):
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
            'places.editorialSummary,places.dineIn,places.goodForGroups,places.liveMusic,places.reservable,'
            'places.servesBreakfast,places.servesCocktails,places.servesDessert,places.servesDinner,'
            'places.servesLunch,places.servesWine'
        )
    }

    payload = {
        "textQuery": f"Top Restaurants in {location}"
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

def select_top_places(sorted_restaurants: List[Dict], sorted_attractions: List[Dict], duration: int) -> Dict[str, List[Dict]]:
    """
    Selects top-rated places based on the duration.
    
    Args:
        sorted_restaurants: List of sorted restaurants in descending order of ratings.
        sorted_attractions: List of sorted attractions in descending order of ratings.
        duration: The number of days to plan the itinerary.

    Returns:
        A dictionary with top restaurants and attractions for the trip duration.
    """
    # top_attractions = sorted_attractions[:2 * duration]
    # top_restaurants = sorted_restaurants[:3 * duration]

    top_attractions = sorted_attractions
    top_restaurants = sorted_restaurants
    
    return {
        "top_attractions": top_attractions,
        "top_restaurants": top_restaurants
    }

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
        daily_itineraries.append({
            "attractions": attractions,
            "restaurants": restaurants
        })

    return daily_itineraries

@router.post("/submit")
async def submit_form(data: FormData, db: Session = Depends(get_db)):
    """
    Endpoint to handle form submission.

    Args:
        data: The validated form data.
        db: The database session.

    Returns:
        A success message upon successful form submission.
    """

    restaurants_list = await get_restaurants_details(data.destination)
    attractions_list = await get_attractions_details(data.destination)

    sorted_restaurants_list = sort_list_using_bayesian_average(restaurants_list)
    sorted_attractions_list = sort_list_using_bayesian_average(attractions_list)
    duration = data.duration

    daily_itineraries = cluster_places(sorted_restaurants_list, sorted_attractions_list, duration)

    return {
        "daily_itineraries": daily_itineraries
    }
