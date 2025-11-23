import random
from datetime import datetime, timedelta
from crewai.tools import tool
import os
import requests
import json
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults


load_dotenv()

@tool
def search_flights(origin: str, destination: str, date: str):
    """
    A dummy flight search tool that generates flights data.
    """
    airlines = ["ME", "LH", "BA", "AF", "QR", "EK"]
    results = []
    base_date = datetime.strptime(date, "%Y-%m-%d")

    for _ in range(5):
        airline = random.choice(airlines)
        flight_number = f"{airline}{random.randint(1, 9999):04d}"
        dep_hour = random.randint(0, 23)
        dep_min = random.randint(0, 59)
        departure = base_date + timedelta(hours=dep_hour, minutes=dep_min)

        duration_minutes = random.randint(60, 720)  # between 1h and 12h
        arrival = departure + timedelta(minutes=duration_minutes)

        price = round(random.uniform(100.0, 2000.0), 2)

        results.append({
            "flight_number": flight_number,
            "airline": airline,
            "origin": origin,
            "destination": destination,
            "departure_datetime": departure.strftime("%Y-%m-%d %H:%M"),
            "arrival_datetime": arrival.strftime("%Y-%m-%d %H:%M"),
            "duration_minutes": duration_minutes,
            "price_usd": price
        })

    return results





TAVILY=os.getenv("TAVILY_API_KEY")
API_KEY = os.getenv("GOOGLE_API_KEY")
model = "gemini-2.5-flash"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


@tool
def hotel_data(location: str, check_in: str, check_out: str, count: int = 5):
    """Generate dummy hotel listings in the specified location and date range."""
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY must be set in environment")

    prompt = (
        f"Generate {count} dummy hotel listings in {location} between {check_in} and {check_out}. "
        "For each hotel, include: name, star rating (3-5), nightly price in USD (e.g., 120.00), overall guest rating (e.g., 4.3/5), "
        "and a list of 3-5 amenities (e.g., Free WiFi, Pool, Spa). Return the result in JSON format as an array of objects."
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    { "text": prompt }
                ]
            }
        ]
    }

    resp = requests.post(ENDPOINT, headers=headers, json=body)
    resp.raise_for_status()
    data = resp.json()
  
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    try:
        listings = json.loads(text)
    except json.JSONDecodeError:

        listings = None
    return listings

web_search = TavilySearchResults(API=TAVILY,max_results=5)

@tool
def plan_tour(destination: str):
    """Prepare a tourism tour in the destination country using web search."""
    query = f"top tourist attractions and cultural experiences in {destination}"
    search_results = web_search.invoke({"query": query})
    return f"Tourism plan for {destination}:\n{search_results}"