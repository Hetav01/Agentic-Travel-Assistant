import asyncio
from typing import List
from pydantic import BaseModel, Field
from agents import Agent, Runner
from dotenv import load_dotenv
from tools import get_weather_forecast, search_flights, search_hotels
import os

load_dotenv()

model = "gpt-4o-mini"

# -- Models for structured output --

class FlightRecommendation(BaseModel):
    airline: str
    departure_time: str
    arrival_time: str
    price: float
    direct_flight: bool
    recommendation_reason: str
    
class HotelRecommendation(BaseModel):
    name: str
    location: str
    price_per_night: float
    amenities: List[str]
    recommendation_reason: str
    
class TravelPlan(BaseModel):
    destination: str
    duration_days: int
    budget: float
    activities: List[str] = Field(description="List of recommended activities")
    notes: str = Field(description="Additional notes or recommendations")
    

# -- Main agents ---

flight_agent = Agent(
    name= "Flight Specialist",
    handoff_description= "Specialist agent for finding and recommending flights.",
    instructions="""
    You are a flight specialist who helps users find the best flights for their trips.
    
    Use the search_flights tool to find flight options, and then provide personalized recommendations
    based on the user's preferences (price, time, direct vs. connecting).
    
    Always explain the reasoning behind your recommendations.
    
    Format your response in a clear, organized way with flight details and prices.
    """,
    model= model,
    tools= [search_flights],
    output_type= FlightRecommendation
)

hotel_agent = Agent(
    name="Hotel Specialist",
    handoff_description="Specialist agent for finding and recommending hotels and accommodations",
    instructions="""
    You are a hotel specialist who helps users find the best accommodations for their trips.
    
    Use the search_hotels tool to find hotel options, and then provide personalized recommendations
    based on the user's preferences (location, price, amenities).
    
    Always explain the reasoning behind your recommendations.
    
    Format your response in a clear, organized way with hotel details, amenities, and prices.
    """,
    model=model,
    tools=[search_hotels],
    output_type=HotelRecommendation
)

travel_agent = Agent(
    name= "Travel Planner",
    instructions="""
    You are a comprehensive travel planning assistant that helps users plan their perfect trip.
    
    You can create personalized travel itineraries based on the user's interests and preferences.
    
    Always be helpful, informative, and enthusiastic about travel. Provide specific recommendations
    based on the user's interests and preferences.
    
    When creating travel plans, consider:
    - Local attractions and activities
    - Budget constraints
    - Travel duration
    """,
    model= model,
    tools= [get_weather_forecast],
    handoffs= [flight_agent, hotel_agent],
    output_type= TravelPlan
)

# --- Main Function ---

async def main():
    # Example queries to test the system
    queries = [
        "I need a flight from New York to Chicago tomorrow",
        "Find me a hotel in Paris with a pool for under $300 per night"
    ]
    
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        
        result = await Runner.run(travel_agent, query)
        
        print("\nFINAL RESPONSE:")
        
        # Format the output based on the type of response
        if hasattr(result.final_output, "airline"):  # Flight recommendation
            flight = result.final_output
            print("\n✈️ FLIGHT RECOMMENDATION ✈️")
            print(f"Airline: {flight.airline}")
            print(f"Departure: {flight.departure_time}")
            print(f"Arrival: {flight.arrival_time}")
            print(f"Price: ${flight.price}")
            print(f"Direct Flight: {'Yes' if flight.direct_flight else 'No'}")
            print(f"\nWhy this flight: {flight.recommendation_reason}")
            
        elif hasattr(result.final_output, "name") and hasattr(result.final_output, "amenities"):  # Hotel recommendation
            hotel = result.final_output
            print("\n🏨 HOTEL RECOMMENDATION 🏨")
            print(f"Name: {hotel.name}")
            print(f"Location: {hotel.location}")
            print(f"Price per night: ${hotel.price_per_night}")
            
            print("\nAmenities:")
            for i, amenity in enumerate(hotel.amenities, 1):
                print(f"  {i}. {amenity}")
                
            print(f"\nWhy this hotel: {hotel.recommendation_reason}")
            
        elif hasattr(result.final_output, "destination"):  # Travel plan
            travel_plan = result.final_output
            print(f"\n🌍 TRAVEL PLAN FOR {travel_plan.destination.upper()} 🌍")
            print(f"Duration: {travel_plan.duration_days} days")
            print(f"Budget: ${travel_plan.budget}")
            
            print("\n🎯 RECOMMENDED ACTIVITIES:")
            for i, activity in enumerate(travel_plan.activities, 1):
                print(f"  {i}. {activity}")
            
            print(f"\n📝 NOTES: {travel_plan.notes}")
        
        else:  # Generic response
            print(result.final_output)
        
if __name__ == "__main__":
    asyncio.run(main())
    
