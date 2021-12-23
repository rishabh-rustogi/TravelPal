# -*- coding: utf-8 -*-

'''
File Name: googleMaps.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

GoogleMaps class retrieves point of interests from google maps API, process it and then return the data.
This class also returns the estimated longitude and latitude for getting weather data Open Weather API.

Files imported by this class: readAPIKEYS.py

Files importing this class: travelpalControl.py
'''

import requests
import json
from dash import html

class GoogleMaps:
    def __init__(self, key):
        '''
        Set the Google maps API key
        
        Parameters
        ----------
        key : str
            contains Google Maps API key.
        '''
        self.API_KEY = key
    
    def setLocation(self, country, city):
        '''
        Retrieves information from Google Maps for POI
        
        Sets the city and country, retrieves information, and
        convert it to JSON Object
        
        Parameters
        ----------
        country : str
            Country for which to retrieve data.
        city : str
            City for which to retrieve data.
        '''
        self.country = country
        self.city = city
        # Creating the desired URL for searching point of interests in a country
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + self.city + "+" + self.country + "+tourism+point+of+interest&language=en&key=" + self.API_KEY
        
        # Retreive the POI related details for <country>
        resp = requests.get(url)
        resp = json.loads(resp.text)
        
        try:
            self.info = resp['results']
        except:
            pass
        
        self.info = self.getPOI()
        
    def getPOI(self):
        '''
        Returns Points of Interests for 'country' and 'city'
        
        Generate a list of places retrieved not of type travel agencies
        and return it
        '''
        content = []
        
        self.latitude = 0
        self.longitude = 0
        
        for place in self.info:
            
            # Skip any places with type travel_agency
            if "travel_agency" in place['types']:
                continue
            
            link = "https://www.google.com/search?q=" + "+".join(place['name'].split(" "))
            content.append({"name": place['name'], "rating": place['rating'], "link": link, 'address': place['formatted_address']})
            self.latitude += place['geometry']['location']['lat']
            self.longitude += place['geometry']['location']['lng']
        
            
        if len(content) > 0:
            self.latitude = self.latitude/len(content)
            self.longitude = self.longitude/len(content)
            return content
        return None
        
    def getFormattedPOISummary(self):
        '''
        Generate HTML content for POI Summary
        
        Return a list of HTML tags generated from getPOI(),
        with reference link and ratings.
        
        Calculate latitude and longitude for a place using
        it POI
        '''
        content = []
        info = self.info
        if info == None:
            text = "Currently no POI available for " + self.city + ", " + self.country
            return html.P(children=text)
        
        
        for num in range(min(len(info), 5)):
            try:
                text = str(num+1) + ". " + info[num]["name"] + ": " + info[num]["address"] + "\nRating: " + str(info[num]['rating'])
                content.append(
                    html.Div(
                        children=[
                            html.P(children=text),
                            html.A('Get more info here', href=info[num]['link'], target="_blank"),
                            html.P(children="\n")
                        ],
                        style={'font-size':'16', 'whiteSpace': 'pre-wrap'}
                    )
                )
            except:
                pass
            
        if len(content) == 0:
            return html.P("Unable to fetch Points of Intersets for " + self.city + ". " + self.country)
            
        return content

    def getLocationLat(self):
        '''
        Return the Latitude for selected 'city' and 'country'
        '''
        return self.latitude
    
    def getLocationLng(self):
        '''
        Return the Longitude for selected 'city' and 'country'
        '''
        return self.longitude
    