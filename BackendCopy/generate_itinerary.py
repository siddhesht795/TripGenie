from fpdf import FPDF
from itinerary_utils import create_daywise_itinerary

def generate_itinerary_pdf(user_trip_details, flight_details, hotel_details, weather_summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    destination = user_trip_details.get("arrival_id", "Unknown Destination")
    outbound_date = str(user_trip_details.get("outbound_date", ""))
    return_date = str(user_trip_details.get("return_date", ""))
    num_days = (return_date - outbound_date).days if outbound_date and return_date else 5  # fallback to 5

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=f"Trip Itinerary to {destination}", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Travel Dates: {outbound_date} to {return_date}")
    pdf.multi_cell(0, 10, txt=" ")

    # Add flight details
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Flight Details", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=str(flight_details))

    # Add hotel details
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Hotel Details", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=str(hotel_details))

    # Add weather summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Weather Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=weather_summary)

    # Add day-wise itinerary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Day-wise Itinerary", ln=True)
    pdf.set_font("Arial", size=12)
    plans = create_daywise_itinerary(destination, num_days)
    for plan in plans:
        pdf.ln(5)
        pdf.multi_cell(0, 10, txt=plan)

    # Save the PDF
    filename = f"{destination}_itinerary.pdf"
    pdf.output(filename)

    print(f"\n✅ PDF generated: {filename}")
    return filename