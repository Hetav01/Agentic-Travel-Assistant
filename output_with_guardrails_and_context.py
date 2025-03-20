import asyncio
from typing import Optional, List
from pydantic import BaseModel, Field
from agents import Agent, RunContextWrapper, Runner, function_tool, ModelSettings, InputGuardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from dotenv import load_dotenv


import logfire

from tools import get_weather_forecast, search_flights, search_hotels
from context import UserContext

import os

load_dotenv()

# setting up logging using logfire
logfire.configure(send_to_logfire= "if-token-present")
logfire.instrument_openai_agents()

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
    
# -- Guardrails Agent output --

class BudgetAnalysis(BaseModel):
    is_realistic: bool
    reasoning: str
    suggested_budget: Optional[float] = None


# --- Guardrail Agent ---

budget_analysis_agent = Agent(
    name="Budget Analyzer",
    instructions="""
    You analyze travel budgets to determine if they are realistic for the destination and duration.
    Consider factors like:
    - Average hotel costs in the destination
    - Flight costs
    - Food and entertainment expenses
    - Local transportation
    
    Provide a clear analysis of whether the budget is realistic and why.
    If the budget is not realistic, suggest a more appropriate budget.
    Don't be harsh at all, lean towards it being realistic unless it's really crazy.
    If no budget was mentioned, just assume it is realistic.
    """,
    output_type=BudgetAnalysis,
    model=model
) 

# -- Guardrail --

async def budget_guardrail(ctx, agent, input_data):
    """Check if the user's travel budget is realistic."""
    # Parse the input to extract destination, duration and budget
    
    try:
        analysis_prompt = f"The user is planning a trip and said: {input_data}.\nAnalyze if their budget is realistic for a trip to their destination for the length they mentioned."
        result = await Runner.run(budget_analysis_agent, analysis_prompt, context= ctx.context)
        final_output = result.final_output_as(BudgetAnalysis)
        
        if not final_output.is_realistic:
            print(f"Your budget may not be realistic: {final_output.reasoning}")

        print("Your budget seems realistic!")
        
        return GuardrailFunctionOutput(
            output_info= final_output,
            tripwire_triggered= not final_output.is_realistic
        ) 
    except Exception as e:
        return GuardrailFunctionOutput(
            output_info= BudgetAnalysis(is_realistic=True, reasoning=f"Error analyzing budget: {str(e)}"),
            tripwire_triggered= False
        )       

# -- Main agents ---

flight_agent = Agent[UserContext](
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

hotel_agent = Agent[UserContext](
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

travel_agent = Agent[UserContext](
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
    input_guardrails= [InputGuardrail(guardrail_function=budget_guardrail)],
    output_type= TravelPlan
)

conversational_agent = Agent[UserContext](
    name="General Conversation Specialist",
    handoff_description="Specialist agent for giving basic responses to the user to carry out a normal conversation as opposed to structured output.",
    instructions="""
    You are a trip planning expert who answers basic user questions about their trip and offers any suggestions.
    Act as a helpful assistant and be helpful in any way you can be.
    """,
    model=model
)



# --- Main Function ---

async def main():
    # create a user context
    user_context = UserContext(
        user_id = "hp9902",
        preferred_airlines= ["SkyWays", "OceanAir"],
        hotel_amenities= ["WiFi", "Pool"],
        budget_level= "mid-range"
    )
    
    
    # Example queries to test different aspects of the system
    queries = [
        "I'm planning a trip to Miami for 5 days with a budget of $2000. What should I do there?",
        "I'm planning a trip to Tokyo for a week, looking to spend under $5,000. Suggestions?",
        "I need a flight from New York to Chicago tomorrow",
        "Find me a hotel in Paris with a pool for under $400 per night",
        "I want to go to Dubai for a week with only $300"  # This should trigger the budget guardrail
    ]
    
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        print("="*50)
        
        try:
            result = await Runner.run(travel_agent, query, context=user_context)
            
            print("\nFINAL RESPONSE:")
        
            # Format the output based on the type of response
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
                
                # Show user preferences that influenced this recommendation
                airlines = user_context.preferred_airlines
                if airlines and flight.airline in airlines:
                    print(f"\n👤 NOTE: This matches your preferred airline: {flight.airline}")
                
            elif hasattr(result.final_output, "name") and hasattr(result.final_output, "amenities"):  # Hotel recommendation
                hotel = result.final_output
                print("\n🏨 HOTEL RECOMMENDATION 🏨")
                print(f"Name: {hotel.name}")
                print(f"Location: {hotel.location}")
                print(f"Price per night: ${hotel.price_per_night}")
                
                print("\nAmenities:")
                for i, amenity in enumerate(hotel.amenities, 1):
                    print(f"  {i}. {amenity}")
                
                # Highlight matching amenities from user preferences
                preferred_amenities = user_context.hotel_amenities
                if preferred_amenities:
                    matching = [a for a in hotel.amenities if a in preferred_amenities]
                    if matching:
                        print("\n👤 MATCHING PREFERRED AMENITIES:")
                        for amenity in matching:
                            print(f"  ✓ {amenity}")
                
                print(f"\nWhy this hotel: {hotel.recommendation_reason}")
                
            elif hasattr(result.final_output, "destination"):  # Travel plan
                travel_plan = result.final_output
                print(f"\n🌍 TRAVEL PLAN FOR {travel_plan.destination.upper()} 🌍")
                print(f"Duration: {travel_plan.duration_days} days")
                print(f"Budget: ${travel_plan.budget}")
                
                # Show budget level context
                budget_level = user_context.budget_level
                if budget_level:
                    print(f"Budget Category: {budget_level.title()}")
                
                print("\n🎯 RECOMMENDED ACTIVITIES:")
                for i, activity in enumerate(travel_plan.activities, 1):
                    print(f"  {i}. {activity}")
                
                print(f"\n📝 NOTES: {travel_plan.notes}")
            
            else:  # Generic response
                print(result.final_output)
        
        except InputGuardrailTripwireTriggered as e:
            print(f"\n🚨 GUARDRAIL TRIGGERED!!!:\n\n {e}")
        
if __name__ == "__main__":
    asyncio.run(main())
    
