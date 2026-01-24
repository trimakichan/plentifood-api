import os
from flask import make_response, abort
import requests


LOCATIONIQ_PATH = "https://us1.locationiq.com/v1/search.php"


def get_coordinates(data):

    address_line1 = data["address_line1"]
    address_line2 = data.get("address_line2")
    city = data["city"]
    state = data["state"]
    postal_code = data["postal_code"]

    if address_line2:
        address = f"{address_line1}, {city}, {state} {postal_code}"
    else:
        address = f"{address_line1}, {address_line2}, {city}, {state} {postal_code}"

    query_params = {
        "key": os.environ.get("LOCATIONIQ_API_KEY"),
        "q": address.strip(),
        "format": "json",
        "limit": 1,
    }

    try:
        response = requests.get(LOCATIONIQ_PATH, params=query_params)
        response.raise_for_status()
        data = response.json()
    except requests.HTTPError as e:
        raise ValueError("Geocoding service failed") from e
    
    if not data:
        raise ValueError("Address not found")
    
    return {
        "latitude": float(data[0]["lat"]),
        "longitude": float(data[0]["lon"]),
    }



