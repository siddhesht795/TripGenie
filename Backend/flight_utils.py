import requests
from config import SERP_API_KEY

# Convert minutes to "X hrs Y mins" format
def convert_minutes_to_hr_min(mins):
    try:
        mins = int(mins)
        hours = mins // 60
        minutes = mins % 60
        parts = []
        if hours > 0:
            parts.append(f"{hours} hr{'s' if hours != 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
        return ' '.join(parts) if parts else "0 mins"
    except:
        return str(mins) + " mins"

def get_flight_data(user_trip_details):
    params = {
        "engine": "google_flights",
        "departure_id": user_trip_details["departure_id"],
        "arrival_id": user_trip_details["arrival_id"],
        "outbound_date": user_trip_details["outbound_date"],
        "return_date": user_trip_details["return_date"],
        "type": user_trip_details["type"],
        "currency": user_trip_details["currency"],
        "api_key": SERP_API_KEY
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        if "error" in data:
            print(f"❌ API Error: {data['error']}")
            return []

        flights_data = []

        if "best_flights" in data and isinstance(data["best_flights"], list):
            for flight in data["best_flights"][:5]:
                flight_details = {
                    "price": flight.get("price", "N/A"),
                    "total_duration": convert_minutes_to_hr_min(flight.get("total_duration", 0)),
                    "flights": [],
                    "layovers": []
                }

                for leg in flight.get("flights", []):
                    flight_details["flights"].append({
                        "airline": leg.get("airline", "Unknown"),
                        "flight_number": leg.get("flight_number", "N/A"),
                        "departure_airport": leg.get("departure_airport", {}).get("name", "N/A"),
                        "departure_time": leg.get("departure_airport", {}).get("time", "N/A"),
                        "arrival_airport": leg.get("arrival_airport", {}).get("name", "N/A"),
                        "arrival_time": leg.get("arrival_airport", {}).get("time", "N/A"),
                        "duration": convert_minutes_to_hr_min(leg.get("duration", 0))
                    })

                for layover in flight.get("layovers", []):
                    flight_details["layovers"].append({
                        "name": layover.get("name", "Unknown"),
                        "duration": convert_minutes_to_hr_min(layover.get("duration", 0))
                    })

                flights_data.append(flight_details)

        return flights_data

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []
    except ValueError:
        print("❌ Error decoding JSON response!")
        return []
