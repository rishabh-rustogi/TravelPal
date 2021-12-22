# -*- coding: utf-8 -*-
import requests
import json

# Google maps api key
API_KEY = "xxx"

try:
    
    # Choosing the country (E.g. Egypt)
    country = "egypt"
    country = "".join(country.split( ))
    
    # Creating the desired URL for searching point of interests in a country
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + country + "+tourism+point+of+interest&language=en&key=" + API_KEY
    
    # Retreive the POI related details for <country>
    resp = requests.get(url)
    resp = json.loads(resp.text)
    for info in resp['results']:
        if "travel_agency" in info['types']:
            continue
        print(info)
except:
    
    # In case an error occurs
    print("cant find POI")