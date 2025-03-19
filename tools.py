from agents import function_tool, RunContextWrapper
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Optional, List
import json

from context import UserContext

# -- Weather tool --

# We'll work with dummy data first and then after testing replace it with a real API call.

# --- Tools ---

@function_tool
async def get_weather_forecast(city: str, date: str) -> str:
    """Get the weather forecast for a city on a specific date."""
    # In a real implementation, this would call a weather API
    weather_data = {
        "New York": {"sunny": 0.3, "rainy": 0.4, "cloudy": 0.3},
        "Los Angeles": {"sunny": 0.8, "rainy": 0.1, "cloudy": 0.1},
        "Chicago": {"sunny": 0.4, "rainy": 0.3, "cloudy": 0.3},
        "Miami": {"sunny": 0.7, "rainy": 0.2, "cloudy": 0.1},
        "London": {"sunny": 0.2, "rainy": 0.5, "cloudy": 0.3},
        "Paris": {"sunny": 0.4, "rainy": 0.3, "cloudy": 0.3},
        "Tokyo": {"sunny": 0.5, "rainy": 0.3, "cloudy": 0.2},
    }
    
    if city in weather_data:
        conditions = weather_data[city]
        # Simple simulation based on probabilities
        highest_prob = max(conditions, key=conditions.get)
        temp_range = {
            "New York": "15-25°C",
            "Los Angeles": "20-30°C",
            "Chicago": "10-20°C",
            "Miami": "25-35°C",
            "London": "10-18°C",
            "Paris": "12-22°C",
            "Tokyo": "15-25°C",
        }
        return f"The weather in {city} on {date} is forecasted to be {highest_prob} with temperatures around {temp_range.get(city, '15-25°C')}."
    else:
        return f"Weather forecast for {city} is not available."
    
    
@function_tool
def search_flights(wrapper: RunContextWrapper[UserContext], origin: str, destination: str, date: str) -> str:
    """Search for flights from origin to destination on a specific date."""
    # In a real implementation, this would call a flight API
    # for now using mock data
    
    flight_options = [
        {
            "airline": "SkyWays",
            "departure_time": "08:00",
            "arrival_time": "10:30",
            "price": 350.00,
            "direct": True
        },
        {
            "airline": "OceanAir",
            "departure_time": "12:45",
            "arrival_time": "15:15",
            "price": 275.50,
            "direct": True
        },
        {
            "airline": "MountainJet",
            "departure_time": "16:30",
            "arrival_time": "21:45",
            "price": 225.75,
            "direct": False
        }
    ]
    
    # apply user preferences if available
    if wrapper and wrapper.context:
        preferred_airlines = wrapper.context.preferred_airlines
        if preferred_airlines:
            # Move the preferred airlines to the top of the list
            flight_options.sort(key= lambda x: x["airline"] not in preferred_airlines)

            for flight in flight_options:
                if flight["airline"] in preferred_airlines:
                    flight["preferred"] = True
    
    return json.dumps(flight_options)    

@function_tool
def search_hotels(wrapper: RunContextWrapper[UserContext], city: str, check_in: str, check_out:str, max_price: Optional[float] = None) -> str:
    """Search for hotels in a city for specific dates within a price range."""
    # In a real implementation, this would call a hotel search API
    hotel_options = [
        {
            "name": "City Center Hotel",
            "location": "Downtown",
            "price_per_night": 199.99,
            "amenities": ["WiFi", "Pool", "Gym", "Restaurant"]
        },
        {
            "name": "Riverside Inn",
            "location": "Riverside District",
            "price_per_night": 149.50,
            "amenities": ["WiFi", "Free Breakfast", "Parking"]
        },
        {
            "name": "Luxury Palace",
            "location": "Historic District",
            "price_per_night": 349.99,
            "amenities": ["WiFi", "Pool", "Spa", "Fine Dining", "Concierge"]
        }
    ]
    
    # Filter by max_price if provided
    if max_price is not None:
        filtered_hotels = [hotel for hotel in hotel_options if hotel["price_per_night"] <= max_price]
    else: 
        filtered_hotels = hotel_options
        
    if wrapper and wrapper.context:
        preferred_amenities = wrapper.context.hotel_amenities
        budget_level = wrapper.context.budget_level
        
        # Sort hotels by preference match
        if preferred_amenities:
            # Calculate a score based on how many preferred amenities each hotel has
            for hotel in filtered_hotels:
                matching_amenities = [a for a in preferred_amenities if a in hotel["amenities"]]
                hotel["matching_amenities"] = matching_amenities    # add a new key to the hotel dict
                hotel["preference_score"] = len(matching_amenities)
                
        # sort by preference score
        filtered_hotels.sort(key = lambda x: x["preference_score"], reverse=True)
        
        # Apply budget filter if available
        if budget_level:
            if budget_level == "budget":
                filtered_hotels.sort(key = lambda x: x["price_per_night"])
            elif budget_level == "luxury":
                filtered_hotels.sort(key = lambda x: x["price_per_night"], reverse=True)
    
    return json.dumps(filtered_hotels)