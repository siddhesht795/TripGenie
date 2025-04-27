from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
from datetime import datetime

def draw_wrapped_text(pdf, text, x, y, width):
    """
    Wraps and draws text within the specified width.
    """
    lines = simpleSplit(text, pdf._fontObj, pdf._fontSize, width)
    for line in lines:
        if y < 50:  # Check if there's enough space on the page
            pdf.showPage()
            pdf.setFont("Symbola", 12)
            y = letter[1] - 50
        pdf.drawString(x, y, line)
        y -= pdf._leading
    return y

def generate_itinerary_pdf(user_trip_details, flight_details, hotel_details, weather_summary, daywise_activities):
    """
    Generates a PDF itinerary based on the provided details.
    """
    # Register font for emojis and symbols
    pdfmetrics.registerFont(TTFont("Symbola", "fonts/Symbola.ttf"))

    filename = f"{user_trip_details['destination_city']}_itinerary.pdf"
    pdf = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Layout settings
    margin = 50
    y = height - margin
    max_width = width - 2 * margin
    font_title = 16
    font_text = 12
    line_height = 16
    section_spacing = 24

    def add_new_page():
        nonlocal y
        pdf.showPage()
        pdf.setFont("Symbola", font_text)
        y = height - margin

    def check_page_space(lines_needed=1):
        nonlocal y
        if y - (line_height * lines_needed) < margin:
            add_new_page()

    def write_title(title):
        nonlocal y
        check_page_space(2)
        pdf.setFont("Symbola", font_title)
        pdf.drawString(margin, y, title)
        y -= line_height
        pdf.setFont("Symbola", font_text)
        y -= 4  # slight padding

    def write_lines(text, indent=0):
        nonlocal y
        lines = simpleSplit(text, pdf._fontname, pdf._fontsize, max_width - indent)
        for line in lines:
            check_page_space()
            pdf.drawString(margin + indent, y, line)
            y -= line_height

    # ---------- Document Start ----------
    pdf.setFont("Symbola", font_title + 4)
    title = f"🌍 Trip Itinerary to {user_trip_details['destination_city']}"
    pdf.drawCentredString(width / 2, y, title)
    y -= section_spacing

    # Travel Dates
    write_title("📅 Travel Dates")
    write_lines(f"{user_trip_details['outbound_date']} to {user_trip_details['return_date']}")
    y -= section_spacing

    # Flight Details
    write_title("✈️ Flights")
    if (flight_details):
        for i, flight in enumerate(flight_details, 1):
            write_lines(f"Flight Option {i}:", indent=0)
            write_lines(f"Price: {flight['price']}, Duration: {flight['total_duration']}", indent=16)
            for f in flight["flights"]:
                flight_info = f"{f['airline']} {f['flight_number']} | {f['departure_airport']} → {f['arrival_airport']} | Duration: {f['duration']}"
                write_lines(flight_info, indent=32)
            if flight["layovers"]:
                write_lines("Layovers:", indent=32)
                for layover in flight["layovers"]:
                    layover_info = f"{layover['name']} | Duration: {layover['duration']}"
                    write_lines(layover_info, indent=48)
            y -= line_height
    else:
        write_lines("No flight details available.")
    y -= section_spacing

    # Hotel Details
    write_title("🏨 Hotel Options")
    if hotel_details:
        for hotel in hotel_details:
            write_lines(f"{hotel['name']} - {hotel['price']}", indent=0)
            write_lines(f"Amenities: {', '.join(hotel['amenities'])}", indent=16)
            y -= line_height
    else:
        write_lines("No hotel details available.")
    y -= section_spacing

    # Weather
    write_title("🌤️ Weather Summary")
    write_lines(weather_summary)
    y -= section_spacing

    # Day-wise Itinerary with Activities
    write_title("🗓️ Day-wise Itinerary with Activities")
    if daywise_activities:
        for day in daywise_activities:
            # Add a distinct header for each day
            write_title(f"📅 {day['date']}")
            if day.get("is_rest_day", False):
                # Highlight rest days
                write_lines("🛌 Rest Day: Take time to relax and recharge.", indent=16)
            else:
                for activity in day["activities"]:
                    if isinstance(activity, dict):  # Handle structured activity data
                        write_lines(f"  🏛️ {activity['name']}", indent=16)
                        write_lines(f"    📖 Description: {activity['description']}", indent=32)
                        write_lines(f"    🕒 Best Time to Visit: {activity['best_time_to_visit']}", indent=32)
                        write_lines(f"    🛋️ Rest Period: {activity['rest_period']}", indent=32)
                        y -= line_height  # Add spacing between activities
                    else:  # Handle plain text activity data
                        write_lines(f"  {activity}", indent=16)
            y -= section_spacing  # Add spacing between days
    else:
        write_lines("❌ No activities found for the selected dates.")
    y -= section_spacing

    # Save PDF
    pdf.save()
    return filename
