from datetime import datetime

def generate_itinerary(user_trip_details, flights, hotels, weather_details):
    itinerary = []

    # Trip Overview
    itinerary.append(f"🌍 **Trip Overview:**")
    itinerary.append(f"Departure Location: {user_trip_details['departure_id']}")
    itinerary.append(f"Destination: {user_trip_details['destination_city']}")
    itinerary.append(f"Outbound Date: {user_trip_details['outbound_date']}")
    itinerary.append(f"Return Date: {user_trip_details['return_date']}")
    itinerary.append(f"Number of Adults: {user_trip_details['no_adults']}")
    itinerary.append(f"Number of Children: {user_trip_details['no_children']}")
    if user_trip_details["no_children"] > 0:
        itinerary.append(f"Children's Ages: {user_trip_details['children_ages']}")
    itinerary.append("\n" + "="*50)

    # Weather Details
    itinerary.append("🌤️ **Weather Forecast:**")
    itinerary.append(weather_details)
    itinerary.append("\n" + "="*50)

    # Flight Details
    itinerary.append("✈️ **Flight Information:**")
    if flights:
        for flight in flights:
            itinerary.append(f"💰 Price: {flight['price']}")
            itinerary.append(f"⏳ Total Duration: {flight['total_duration']}")
            itinerary.append("📍 Flight Details:")
            for f in flight["flights"]:
                itinerary.append(f" ✈️ {f['airline']} {f['flight_number']} | {f['departure_airport']} ({f['departure_time']}) → {f['arrival_airport']} ({f['arrival_time']}) | ⏳ {f['duration']}")
            if flight["layovers"]:
                itinerary.append("🔄 Layovers:")
                for layover in flight["layovers"]:
                    itinerary.append(f" 🏢 {layover['name']} | ⏳ {layover['duration']}")
            itinerary.append("-" * 50)
    else:
        itinerary.append(f"❌ No flights found for the selected dates.")
    itinerary.append("\n" + "="*50)

    # Hotel Details
    itinerary.append("🏨 **Hotel Information:**")
    if hotels:
        for hotel in hotels:
            itinerary.append(f"🏨 {hotel['name']}")
            itinerary.append(f"💰 Price per night: {hotel['price']}")
            itinerary.append(f"🛋️ Amenities: {', '.join(hotel['amenities'])}")
            itinerary.append("-" * 50)
    else:
        itinerary.append(f"❌ No hotels found for the selected destination.")
    itinerary.append("\n" + "="*50)

    # Return the complete itinerary as a formatted string
    return "\n".join(itinerary)
