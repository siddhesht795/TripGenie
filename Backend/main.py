import requests
from datetime import datetime, timedelta
from config import CURRENCY, TRIP_TYPE, SERP_API_KEY
from iata_utils import get_iata_code_from_serpapi
from flight_utils import get_flight_data
from hotel_utils import get_hotel_details
from weather_utils import get_weather_details
from itinerary_utils import generate_itinerary  # Import the itinerary generation function
from generate_itinerary import generate_itinerary_pdf  # Import the PDF generation function
from activity_utils import get_daywise_activities  # Ensure this import is correct

# Get user input
current_location = input("Enter your current location: ")
destination_location = input("Enter your destination: ")
trip_days = int(input("Enter the number of days for your trip: "))
no_adults = int(input("Enter the number of adults: "))
no_children = int(input("Enter the number of children: "))

children_ages = []
if no_children > 0:
    for i in range(no_children):
        age = int(input(f"Enter the age of child {i+1}: "))
        children_ages.append(str(age))

children_ages_str = ",".join(children_ages) if children_ages else ""

# Dates
tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
return_date = (datetime.now() + timedelta(days=1 + trip_days)).strftime('%Y-%m-%d')

# Get IATA Codes
departure_id = get_iata_code_from_serpapi(current_location)
arrival_id = get_iata_code_from_serpapi(destination_location)

# Construct trip details
user_trip_details = {
    "departure_id": departure_id,
    "arrival_id": arrival_id,
    "outbound_date": tomorrow_date,
    "return_date": return_date,
    "type": TRIP_TYPE,
    "currency": CURRENCY,
    "no_adults": no_adults,
    "no_children": no_children,
    "children_ages": children_ages_str,
    "destination_city": destination_location
}

# Fetch and display flights
print("Fetching flight details...")
flights = get_flight_data(user_trip_details)
if not flights:
    print("❌ No flight details found.")

# Fetch and display hotels
print("Fetching hotel details...")
hotels = get_hotel_details(user_trip_details["destination_city"], user_trip_details["no_adults"], user_trip_details["no_children"], user_trip_details["children_ages"])
if not hotels:
    print("❌ No hotel details found.")

# Get Weather Details
print("Fetching weather details...")
weather_details = get_weather_details(user_trip_details["destination_city"], user_trip_details["outbound_date"], user_trip_details["return_date"])
if not weather_details:
    print("❌ No weather details found.")

# Fetch day-wise activities
print("Fetching day-wise activities...")
daywise_activities = get_daywise_activities(
    user_trip_details["destination_city"],
    user_trip_details["outbound_date"],
    user_trip_details["return_date"]
)
if not daywise_activities:
    print("❌ No day-wise activities found.")
else:
    print("✅ Day-wise activities fetched successfully.")
    for day in daywise_activities:
        print(f"📅 {day['date']}:")
        for activity in day["activities"]:
            if isinstance(activity, dict):
                print(f"  🏛️ {activity['name']} - {activity['description']}")
            else:
                print(f"  {activity}")

# Generate and print the itinerary
print("Generating itinerary...")
itinerary = generate_itinerary(
    user_trip_details, flights, hotels, weather_details, daywise_activities
)
print(itinerary)

# Ask the user if they want to download the itinerary as a PDF
download_pdf = input("Do you want to download the itinerary as a PDF? (yes/no): ").strip().lower()
if download_pdf == "yes":
    print("Generating PDF...")
    pdf_filename = generate_itinerary_pdf(
        user_trip_details, flights, hotels, weather_details, daywise_activities
    )
    print(f"PDF downloaded successfully: {pdf_filename}")
else:
    print("PDF download skipped.")
