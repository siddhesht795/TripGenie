import requests
from config import SERP_API_KEY

def get_iata_code_from_serpapi(city_name):
    query = f"Give the IATA Code for airport in {city_name}"
    url = "https://serpapi.com/search"
    params = {"q": query, "api_key": SERP_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "answer_box" in data and "answer" in data["answer_box"]:
            return data["answer_box"]["answer"]
        else:
            print(f"No IATA code found for {city_name}")
            return "N/A"
    else:
        print(f"Error: {response.status_code}")
        return "N/A"
