# -*- coding: utf-8 -*-
import requests
import geocoder

# Retrieving current geo location
g = geocoder.ip('me')

# Open weather API key
API_KEY = "xxx"

try:
    
    # Creating the desired URL
    url = "https://api.openweathermap.org/data/2.5/onecall?lat="+str(g.lat)+"&lon="+str(g.lng)+"&appid=" + API_KEY
    
    # Retreive the 7 day weather forcast for current location
    resp = requests.get(url)
    print(resp.text)
except:
    
    # In case an error occurs
    print("cant find weather forcast")