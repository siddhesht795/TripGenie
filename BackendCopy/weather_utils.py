import requests

def get_weather_details(destination, outbound_date, return_date):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

    headers = {
        "Authorization": "Bearer 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"
    }

    input_string = f'''How will the weather be when the user is visiting {destination} during {outbound_date} and {return_date}? Please give an assumption of how the weather will be during that time based on previous years. Provide this information in a format suitable for an itinerary under the suitable clothes and weather conditions section.'''

    data = {
        "inputs": input_string
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            weather_details = result[0]["generated_text"][len(input_string):].lstrip()
            return weather_details
        else:
            print("Error fetching weather details:", response.status_code, response.text)
            return "Sorry, we couldn't fetch the weather details at the moment."
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return "Sorry, we couldn't fetch the weather details due to a request error."
