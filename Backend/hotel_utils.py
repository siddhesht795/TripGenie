import requests
from datetime import datetime, timedelta
from config import SERP_API_KEY

def get_hotel_details(destination_city, no_adults="2", no_children="0", children_ages=""):
    check_in_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    check_out_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    query = f"{destination_city} resorts"

    params = {
        "engine": "google_hotels",
        "q": query,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": no_adults,
        "children": no_children,
        "children_ages": children_ages,
        "currency": "INR",
        "gl": "in",
        "hl": "en",
        "api_key": SERP_API_KEY
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        if "error" in data:
            print(f"❌ API Error: {data['error']}")
            return []

        hotels_data = []

        if "properties" in data and isinstance(data["properties"], list):
            for hotel in data["properties"]:
                hotel_details = {
                    "name": hotel.get("name", "N/A"),
                    "price": hotel.get("rate_per_night", {}).get("lowest", "N/A"),
                    "amenities": hotel.get("amenities", [])[:5]
                }
                hotels_data.append(hotel_details)

        return hotels_data

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []
    except ValueError:
        print("❌ Error decoding JSON response!")
        return []
