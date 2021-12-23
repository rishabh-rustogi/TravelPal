# -*- coding: utf-8 -*-

'''
File Name: travelpalController.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

TravelpalController control the data flow from all the class to the app and from the app to all the classes

Files imported by this file: openWeather.py, readAPIKEYS.py, covidInfo.py, usds,py, cdc.py, googleNews.py,
                             googleMaps.py, covidCases.py, covidWorldMap.py, location.py

Files importing this class: travelpalAppLayout.py
'''

from openWeather import OpenWeather
from readAPIKEYS import ReadAPIKEYS
from covidInfo import CovidInfo
from usds import USDSInfo
from cdc import CDCInfo
from googleNews import News
from googleMaps import GoogleMaps
from covidCases import COVIDCases
from covidWorldMap import WorldMap
from location import Location
from dash import html
import traceback
import logging

class TravelpalController:
    def __init__(self):
        '''
        Initialize the logging file and all the Data Source objects
        
        Defines and generate logging file, objects for each Data 
        Source, read the API keys and log error if any 
        '''
        logging.basicConfig(filename="travelpalLogs",
                            filemode='a',
                            format='%(asctime)s: %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.ERROR)
        logging.info("Running Urban Planning")
        self.logger = logging.getLogger()
        
        
        try:
            self.map = WorldMap()
        except:
            self.logger.error("[WorldMap] Unable to create an instace of WorldMap\n" + traceback.format_exc())
            
        try:
            self.api = ReadAPIKEYS("API_KEYS.txt")
        except:
            self.logger.error("[ReadAPIKEYS] Unable to create an instace of ReadAPIKEYS\n" + traceback.format_exc())
            
        try:
            self.weather = OpenWeather(self.api.getAPIKEY("API_KEY_OPEN_WEATHER"))
        except:
            self.logger.error("[OpenWeather] Unable to create an instace of OpenWeather\n" + traceback.format_exc())
         
        try:
            self.covidDetails = CovidInfo(self.api.getAPIKEY("API_KEY_AMADEUS"), self.api.getAPIKEY("API_SECRET_AMADEUS"))
        except:
            self.logger.error("[CovidInfo] Unable to create an instace of CovidInfo\n" + traceback.format_exc())
         
        try:
            self.visa = USDSInfo()
        except:
            self.logger.error("[USDSInfo] Unable to create an instace of USDSInfo\n" + traceback.format_exc())
           
        try:
            self.vaccines = CDCInfo()
        except:
            self.logger.error("[CDCInfo] Unable to create an instace of CDCInfo\n" + traceback.format_exc())
            
        try:
            self.news = News()
        except:
            self.logger.error("[News] Unable to create an instace of News\n" + traceback.format_exc())
            
        try:
            self.poi = GoogleMaps(self.api.getAPIKEY("API_KEY_GOOGLEMAP"))
        except:
            self.logger.error("[GoogleMaps] Unable to create an instace of GoogleMaps\n" + traceback.format_exc())
        
        try:
            self.cases = COVIDCases()
        except:
            self.logger.error("[COVIDCases] Unable to create an instace of COVIDCases\n" + traceback.format_exc())
        
        try:
            self.location = Location("files/countries.csv", "files/regions.csv")
        except:
            self.logger.error("[Location] Unable to create an instace of Location\n" + traceback.format_exc())

    
    def getReturnInformation(self, region, country):
        '''
        Returns the application data
        
        Set the region and country for retrieving information and return the data
        in appropriate format
        
        Parameters
        ----------
        region : str
            Region name to search for information.
        country : str
            Country name to search for information.
        '''
        if country is None or region is None:
            try:
                maps = self.map.getMap()
            except:
                maps = {}
                self.logger.error("[WorldMap] Unable to fetch map\n" + traceback.format_exc())
                
            # Return all the information in correct order
            return maps, {'display': 'block'}, {'display': 'none'}, 0, "", html.P(children="Summary"), "", "", "", html.P(children="Currently no maps available"), "", html.P(children="Covid related info:"), html.P(children="Currently no news available"), {}, html.P(children="Currently no POIs available"), {}
        
        print("Location selected by user: " + region + ", " + country)
        self.logger.error("For location: " + region + ", " + country)
        
        
        
        # Set Country and Region for retrieving Points of Interests for that 
        # location. Get a summary in appropriate format or generate one in 
        # case an error occurs.
        try:
            self.poi.setLocation(country, region)
            summary = html.P(children="Summary for " + region + ", " + country)
            
        except:
            summary = html.P(children="Summary")
            self.logger.error("[GoogleMaps] Unable to set loaction to google maps API\n" + traceback.format_exc())
            
        try:
            poiSummary = self.poi.getFormattedPOISummary()
            
        except:
            poiSummary = html.P("Unable to fetch Points of Intersets for " + region + ", " + country)
            self.logger.error("[GoogleMaps] Unable to retrieve points of interest\n" + traceback.format_exc())
        
        
        
        # Set Longitude and Latitude for retrieving weather information for that 
        # location. Get a line graph in appropriate format or generate one in 
        # case an error occurs.    
        try:
            self.weather.setLocation(self.poi.getLocationLng(), self.poi.getLocationLat())
        except:
            self.logger.error("[OpenWeather] Unable to retrieve information from OpenWeather API\n" + traceback.format_exc())
        
        try:
            weatherMap = self.weather.getWeatherMap()
        except:
            weatherMap = {}
            self.logger.error("[OpenWeather] Unable to retrieve weather map\n" + traceback.format_exc())
        
        
        
        # Set Country retrieving all the covid related information and 
        # guidelines. Get a summaries in appropriate format or generate one in 
        # case an error occurs.
        try:
            self.covidDetails.getDetails(self.location.getISO(country))
        except:
            self.logger.error("[CovidInfo] Unable to retrieve information from Amadeus API\n" + traceback.format_exc())
            
        try:
            covidRiskLevel = self.covidDetails.getCovidRiskLevel()
        except:
            covidRiskLevel = 100
            self.logger.error("[CovidInfo] Unable to retrieve covid risk level\n" + traceback.format_exc())
            
        try:
            covidSeverity  = self.covidDetails.getCovidSeverityLevel()
        except:
            covidSeverity = "Covid Level Extreme"
            self.logger.error("[CovidInfo] Unable to retrieve covid severity level\n" + traceback.format_exc())
        
        try:
            covidSummary = self.covidDetails.getSummary()
        except:
            covidSummary = "Summary currently unavailable"
            self.logger.error("[CovidInfo] Unable to retrieve covid summary\n" + traceback.format_exc())
        
        try:
            hotspots = self.covidDetails.getHotspots()
        except:
            hotspots = "Hostspots currently unavailable"
            self.logger.error("[CovidInfo] Unable to retrieve hotspost\n" + traceback.format_exc())
        
        try:
            covidAllSummary = self.covidDetails.getCovidAllInfo()
        except:
            covidAllSummary = html.P(children="Currently no covid information available")
            self.logger.error("[CovidInfo] Unable to retrieve any covid information\n" + traceback.format_exc())
        
        
        
        # Set Country retrieving visa related information. Get a summary in 
        # appropriate format or generate one in case an error occurs.
        try:
            self.visa.setCountry(country)
        except:
            self.logger.error("[USDSInfo] Unable to retrieve information from USDS website\n" + traceback.format_exc())
            
        try:
            visaSummary = self.visa.getFormattedVisaSummary()
        except:
            visaSummary = "Visa related information currently unavailable"
            self.logger.error("[USDSInfo] Unable to retrieve information about visa\n" + traceback.format_exc())
        
        
        
        # Set Country for retrieving vaccine related guidelines. Get a 
        # summary and country image in appropriate format or generate 
        # one in case an error occurs.
        try:
            self.vaccines.setCountry(country)
        except:
            self.logger.error("[CDCInfo] Unable to retrieve information from CDC website\n" + traceback.format_exc())

        try:
            countryImage = self.vaccines.getImage()
        except:
            countryImage = html.Img(
                alt="Unable to fetch country map for " + country,
                style={'width':'100%', 'height':'100%','border-radius':'25px', 'background-color': '#000000'}
            )
            self.logger.error("[CDCInfo] Unable to get country image from CDC website\n" + traceback.format_exc())
        
        try:
            vaccineSummary = self.vaccines.getVaccineSummary()
            vaccineSummaryTemp = ""
            if vaccineSummary[0] == "":
                vaccineSummaryTemp += "Covid Vaccine Guidelines: No specific covid vaccination guidelines exist for " + country + "\n\n"
                self.logger.error("[CDCInfo] Unable to retrieve covid specific vaccine information from CDC website\n" + traceback.format_exc())
            else:
                vaccineSummaryTemp += vaccineSummary[0]
                
            if vaccineSummary[1] == "":
                vaccineSummaryTemp += "General Vaccine Guideline: No specific vaccination guidelines exist for " + country + "\n\n"
                self.logger.error("[CDCInfo] Unable to retrieve general vaccine information from CDC website\n" + traceback.format_exc())
            else:
                vaccineSummaryTemp += vaccineSummary[1]
                
            if vaccineSummary[2] == "":
                pass
            else:
                vaccineSummaryTemp += vaccineSummary[2]
            vaccineSummary = vaccineSummaryTemp     
        except:
            vaccineSummary = "Vaccine related information currently Unavailable"
            self.logger.error("[CDCInfo] Unable to retrieve any vaccine information\n" + traceback.format_exc())
        
        
        
        # Set Country and Region for retrieving covid realted news articles 
        # for that location. Get a summary in appropriate format or generate 
        # one in case an error occurs.
        try:
            self.news.setLocation(country=country, city=region)
        except:
            self.logger.error("[News] Unable to retrieve information from google news\n" + traceback.format_exc())
            
        try:
            newsSummary = self.news.getFormattedNewsSummary()
        except:
            newsSummary = "Currently no news available for " + region + ", " + country
            self.logger.error("[News] Unable to retrieve news\n" + traceback.format_exc())
            
            
        
        # Set Country for retrieving past week covid cases for the location 
        # Get a bar chart in appropriate format or generate one in case an 
        # error occurs.    
        try:
            self.cases.setCountry(country)
        except:
            self.logger.error("[COVIDCases] Unable to retrieve information from Johns Hopkins University Center\n" + traceback.format_exc())
        
        try:
            covidGraph = self.cases.getCovidGraph()
        except:
            covidGraph = {}
            self.logger.error("[COVIDCases] Unable to retrieve covid bar chart\n" + traceback.format_exc())
            
        
        # Return all the information in correct order
        return {}, {'display': 'none'}, {'display': 'block'}, covidRiskLevel, covidSeverity, summary, covidSummary, hotspots, countryImage, vaccineSummary, visaSummary, covidAllSummary, newsSummary, weatherMap, poiSummary, covidGraph
    
    def getCountries(self):
        '''
        Return all the country names
        '''
        return self.location.getAllCountry()
    
    def getRegions(self, country):
        '''
        Returns a list of regions for a country
        
        Parameters
        ----------
        country : str
            Country name for which to retrieve the regions.
        '''
        return self.location.getRegions(country)