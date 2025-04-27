from datetime import datetime

def generate_itinerary(user_trip_details, flights, hotels, weather_details, daywise_activities):
    itinerary = []

    # Trip Overview
    itinerary.append(f"🌍 **Trip Overview:**")
    itinerary.append(f"📍 **Departure Location:** {user_trip_details['departure_id']}")
    itinerary.append(f"📍 **Destination:** {user_trip_details['destination_city']}")
    itinerary.append(f"📅 **Outbound Date:** {user_trip_details['outbound_date']}")
    itinerary.append(f"📅 **Return Date:** {user_trip_details['return_date']}")
    itinerary.append(f"👨‍👩‍👧‍👦 **Number of Adults:** {user_trip_details['no_adults']}")
    itinerary.append(f"👶 **Number of Children:** {user_trip_details['no_children']}")
    if user_trip_details["no_children"] > 0:
        itinerary.append(f"🧒 **Children's Ages:** {user_trip_details['children_ages']}")
    itinerary.append("\n" + "🛫" * 25)

    # Weather Details
    itinerary.append("🌤️ **Weather Forecast:**")
    itinerary.append(f"📝 {weather_details}")
    itinerary.append("\n" + "☀️" * 25)

    # Flight Details
    itinerary.append("✈️ **Flight Information:**")
    if flights:
        for flight in flights:
            itinerary.append(f"💰 **Price:** {flight['price']}")
            itinerary.append(f"⏳ **Total Duration:** {flight['total_duration']}")
            itinerary.append("📍 **Flight Details:**")
            for f in flight["flights"]:
                itinerary.append(f"  ✈️ **{f['airline']} {f['flight_number']}** | **{f['departure_airport']}** ({f['departure_time']}) → **{f['arrival_airport']}** ({f['arrival_time']}) | ⏳ **{f['duration']}**")
            if flight["layovers"]:
                itinerary.append("🔄 **Layovers:**")
                for layover in flight["layovers"]:
                    itinerary.append(f"  🏢 **{layover['name']}** | ⏳ **{layover['duration']}**")
            itinerary.append("-" * 50)
    else:
        itinerary.append(f"❌ No flights found for the selected dates.")
    itinerary.append("\n" + "🛬" * 25)

    # Hotel Details
    itinerary.append("🏨 **Hotel Information:**")
    if hotels:
        for hotel in hotels:
            itinerary.append(f"🏨 **{hotel['name']}**")
            itinerary.append(f"💰 **Price per night:** {hotel['price']}")
            itinerary.append(f"🛋️ **Amenities:** {', '.join(hotel['amenities'])}")
            itinerary.append("-" * 50)
    else:
        itinerary.append(f"❌ No hotels found for the selected destination.")
    itinerary.append("\n" + "🏩" * 25)

    # Suggested Activities
    itinerary.append("🎉 **Suggested Activities:**")
    itinerary.append(f"🗺️ Explore the local attractions in **{user_trip_details['destination_city']}**.")
    itinerary.append(f"🍴 Try the local cuisine and street food.")
    itinerary.append(f"🛍️ Visit popular shopping areas for souvenirs.")
    itinerary.append("\n" + "🎊" * 25)

    # Day-wise Activities
    itinerary.append("🗓️ **Day-wise Itinerary with Activities:**")
    if daywise_activities:
        for day in daywise_activities:
            itinerary.append(f"📅 **{day['date']}:**")
            for activity in day["activities"]:
                if isinstance(activity, dict):  # Handle structured activity data
                    itinerary.append(f"  🏛️ **{activity['name']}**")
                    itinerary.append(f"    📖 {activity['description']}")
                    itinerary.append(f"    🕒 Best Time to Visit: {activity['best_time_to_visit']}")
                    itinerary.append(f"    🛋️ Rest Period: {activity['rest_period']}")
                else:  # Handle plain text activity data (e.g., rest days)
                    itinerary.append(f"  {activity}")
            itinerary.append("-" * 50)
    else:
        itinerary.append("❌ No activities found for the selected dates.")
    itinerary.append("\n" + "🌟" * 25)

    # Return the complete itinerary as a formatted string
    return "\n".join(itinerary)

def create_daywise_itinerary(destination, num_days):
    """
    Generate a simple day-wise itinerary for the given destination and number of days.
    """
    itinerary = []
    for day in range(1, num_days + 1):
        itinerary.append(f"📅 **Day {day}:** 🌟 Explore the attractions of **{destination}**. Don't forget to capture some memories!")
        itinerary.append(f"  🗺️ Suggested Activities: Visit landmarks, enjoy local cuisine, and shop for souvenirs.")
    return itinerary
