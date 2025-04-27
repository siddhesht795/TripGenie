import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_weather_details(destination, outbound_date, return_date):
    """
    Get weather forecast for a destination using Google's Gemini AI.
    Returns formatted weather information suitable for an itinerary.
    """
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create a detailed prompt
    prompt = f"""
    You are a travel weather assistant. Provide a detailed weather forecast for {destination} 
    between {outbound_date} and {return_date}. Include:

    1. Typical weather conditions for this period (temperature ranges, precipitation)
    2. Recommended clothing/packing suggestions
    3. Any seasonal considerations (monsoon, extreme heat, etc.)
    4. Special weather-related travel tips

    Just give a paragraph of about 50-60 words and see to it that it contains all the information mentioned above
    I want to put it in a pdf so there must not be any unnecessary * or any other symbols
    """
    
    try:
        # Generate the weather forecast
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content.parts:
            weather_details = response.candidates[0].content.parts[0].text
            return weather_details.strip()
        else:
            return "Could not generate weather forecast. Please check back later."
            
    except Exception as e:
        print(f"❌ Weather forecast request failed: {e}")
        return "Weather forecast unavailable at this time."