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
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/trip', methods=['POST'])
def process_trip():
    data = request.json
    current_location = data.get('source')
    destination_location = data.get('destination')
    trip_days = int(data.get('days'))
    no_adults = int(data.get('adults'))
    no_children = int(data.get('children'))
    children_ages = data.get('childAges', [])
    start_date = data.get('startDate')

    # Calculate return date based on start date and trip days
    outbound_date = start_date
    return_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=trip_days)).strftime('%Y-%m-%d')

    # Get IATA Codes
    departure_id = get_iata_code_from_serpapi(current_location)
    arrival_id = get_iata_code_from_serpapi(destination_location)

    user_trip_details = {
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "type": TRIP_TYPE,
        "currency": CURRENCY,
        "no_adults": no_adults,
        "no_children": no_children,
        "children_ages": ",".join(children_ages),
        "destination_city": destination_location
    }

    print("Fetching flight details...")
    try:
        flights = get_flight_data(user_trip_details)
        if not flights:
            print("❌ No flight details found.")
            flights = []
    except Exception as e:
        print(f"Error fetching flight details: {e}")
        flights = []

    print("Fetching hotel details...")
    hotels = get_hotel_details(user_trip_details["destination_city"], no_adults, no_children, ",".join(children_ages))
    if not hotels:
        print("❌ No hotel details found.")

    print("Fetching weather details...")
    weather_details = get_weather_details(user_trip_details["destination_city"], outbound_date, return_date)
    if not weather_details:
        print("❌ No weather details found.")
        weather_details = ""

    print("Fetching day-wise activities...")
    daywise_activities = get_daywise_activities(destination_location, outbound_date, return_date)
    if not daywise_activities:
        print("❌ No day-wise activities found.")
    else:
        print("✅ Day-wise activities fetched successfully.")

    print("Generating itinerary...")
    itinerary = generate_itinerary(user_trip_details, flights, hotels, weather_details, daywise_activities)
    print(itinerary)

    return jsonify({
        "flights": flights,
        "hotels": hotels,
        "weather": weather_details,
        "activities": daywise_activities,
        "itinerary": itinerary
    })

@app.route('/api/trip/pdf', methods=['GET'])
def download_itinerary_pdf_get():
    pdf_filename = request.args.get('filename')
    if not pdf_filename:
        return "PDF filename not provided", 400
    return send_file(pdf_filename, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')

@app.route('/api/trip/pdf', methods=['POST'])
def download_itinerary_pdf_post():
    data = request.json
    current_location = data.get('source')
    destination_location = data.get('destination')
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    trip_days = data.get('days')
    if trip_days is None:
        if start_date and end_date:
            trip_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
        else:
            trip_days = 1
    else:
        trip_days = int(trip_days)

    no_adults = int(data.get('adults', 1))
    no_children = int(data.get('children', 0))
    children_ages = data.get('childAges', [])
    if not isinstance(children_ages, list):
        children_ages = []

    outbound_date = start_date
    return_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=trip_days)).strftime('%Y-%m-%d')

    departure_id = get_iata_code_from_serpapi(current_location)
    arrival_id = get_iata_code_from_serpapi(destination_location)

    user_trip_details = {
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "type": TRIP_TYPE,
        "currency": CURRENCY,
        "no_adults": no_adults,
        "no_children": no_children,
        "children_ages": ",".join(children_ages),
        "destination_city": destination_location
    }

    try:
        flights = get_flight_data(user_trip_details)
    except Exception as e:
        flights = []

    hotels = get_hotel_details(user_trip_details["destination_city"], no_adults, no_children, ",".join(children_ages))
    weather_details = get_weather_details(user_trip_details["destination_city"], outbound_date, return_date)
    daywise_activities = get_daywise_activities(destination_location, outbound_date, return_date)

    pdf_path = generate_itinerary_pdf(user_trip_details, flights, hotels, weather_details, daywise_activities)
    return send_file(pdf_path, as_attachment=True, download_name=pdf_path, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
