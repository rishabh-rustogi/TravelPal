# -*- coding: utf-8 -*-

'''
File Name: openWeatherc.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

OpenWeather class retrieves data from Open Weather API, process it and then return the temperature line chart.
This class gets longitude and latitude data from googleMaps.py

Files imported by this class: readAPIKEYS.py

Files importing this class: travelpalControl.py
'''

import requests
import geocoder
import json
from datetime import datetime
from readAPIKEYS import ReadAPIKEYS
import pandas as pd
import plotly.express as px

class OpenWeather:
    def __init__(self, key):
        '''
        Set the OpenWeather API key
        
        Parameters
        ----------
        key : str
            OpenWeather API key.
        '''
        self.API_KEY = key
        
    def setLocation(self, long, lat):
        '''
        Retrieves weather forcast for the next 7 days
        
        Parameters
        ----------
        long : float
            Longitude of a location.
        lat : float
            Latitude of a location.
        '''
        try:
            url = "https://api.openweathermap.org/data/2.5/onecall?lat="+str(lat)+"&lon="+str(long)+"&appid=" + self.API_KEY
            resp = requests.get(url)
            resp = json.loads(resp.text)
            
            forcast = []
            
            for day in resp["daily"]:
                date = datetime.fromtimestamp(day["dt"]).strftime("%B %d, %Y")
                currTemp = day["temp"]["day"]
                currMin = day["temp"]["min"]
                currMax = day["temp"]["max"]
                forcast.append([date, ((currMin - 273.15) * (9/5)) + 32, 'Minimum'])
                forcast.append([date, ((currTemp - 273.15) * (9/5)) + 32, 'Average'])
                forcast.append([date, ((currMax - 273.15) * (9/5)) + 32, 'Maximum'])
            
            df = pd.DataFrame(forcast, columns = ['Date', 'Temperature (°F)', 'Type'])
            
        except:
            df = pd.DataFrame([], columns = ['Date', 'Temperature (°F)', 'Type'])
        
        self.df = df
    
    def getWeatherMap(self):
        '''
        Return weather forcast line chart for maximum. average and minimum temperature
        '''
        return px.line(self.df, x="Date", y="Temperature (°F)", color='Type', markers=True, symbol='Type')
    
if __name__ == '__main__':
    api = ReadAPIKEYS("API_KEYS.txt")
    weather = OpenWeather(api.getAPIKEY("API_KEY_OPEN_WEATHER"))
    
    # Retrieving current geo location (Sample)
    g = geocoder.ip('me')
    print(weather.getWeatherForcast(g.lng, g.lat))
    
            
    
            
        