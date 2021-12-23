# -*- coding: utf-8 -*-

'''
File Name: covidInfo.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

CovidInfo class retrieves data from Amadeus API about covid realted information, process it and then return the data.
This class also create two regression model to estimate the cases

Files imported by this class: readAPIKEYS.py

Files importing this class: travelpalControl.py
'''

import requests
from requests.structures import CaseInsensitiveDict
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from readAPIKEYS import ReadAPIKEYS
import json
from dash import html
import lxml.html


class CovidInfo:
    def __init__(self, client_id, client_secret):
        '''
        Generate token from Client Key and Secret_ID
        
        Send a request to Amadeus API, generate a token and stores it
        for further calls
        
        Parameters
        ----------
        client_id : str
            contains the client Key.
        client_secret: str
            contains the client Secret Key.
        '''
        self.API_CLIENT_ID = client_id
        self.API_CLIENT_SECRET = client_secret
        self.country = ""
        
    def getDetails(self, country):
        '''
        Retrieves all covid related restriction for 'country'
        
        Parameters
        ----------
        country : str
            Country for which to retrieve data.
        '''
        client = BackendApplicationClient(client_id=self.API_CLIENT_ID)
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(token_url='https://test.api.amadeus.com/v1/security/oauth2/token', client_id=self.API_CLIENT_ID,
                client_secret=self.API_CLIENT_SECRET)
        
        if (country == self.country):
            return
        
        self.country = country
        
        # Creating the desired url
        url = "https://test.api.amadeus.com/v1/duty-of-care/diseases/covid19-area-report?countryCode=" + self.country
        
        # Setting up the appropriate header for request
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + self.token["access_token"]
        
        # Retreive the Covid related details for <country>
        resp = requests.get(url, headers=headers)
        resp = resp.text.replace("<p>","").replace("</p>","")
        self.resp = json.loads(resp)['data']
        self.getAreaRestrictionsInfo()
            
    def getSummary(self):
        '''
        Returns covid related summary for a country
        '''
        return self.resp['summary']


    def getCovidSeverityLevel(self):
        '''
        Returns covid security level
        '''
        return "Covid Level " + self.resp['diseaseRiskLevel']

    def getCovidRiskLevel(self):
        '''
        Returns covid risk level number
        '''
        level = {"Extreme":5, "High":4, "Medium":3, "Moderate":2, "Low":1}
        percent = 100-(((len(level)-level[self.resp['diseaseRiskLevel']])/len(level))*100)
        return int(percent)
        
    def getHotspots(self):
        '''
        Returns hotspot areas for the country
        '''
        return self.resp['hotspots']
    
    def getMoreInfoLink(self):
        '''
        Returns official health department site link if any
        '''
        try:
            return self.resp['dataSources']['healthDepartementSiteLink']
            
        except:
            try:
                return self.resp['diseaseTesting']['rules']
                
            except:
                return "More info link Unavailable"
        
    def getAreaRestrictionsInfo(self):
        '''
        Generate are restrcitions guidelines list
        '''
        try:
            self.areaRestrictions = {}
            for info in self.resp['areaRestrictions']:
                self.areaRestrictions[info['restrictionType']] = info['text']                
        except:
            pass
    
    def getDomesticTravelRestrictions(self):
        '''
        return domestic travel information without HTML tags
        '''
        try:
            return lxml.html.fromstring(self.areaRestrictions['Domestic Travel']).text_content()
            
        except:
            return "Domestic travel info unavailable"
        
    def getFlightInfo(self):
        '''
        return flight travel information without HTML tags
        '''
        try:
            return lxml.html.fromstring(self.resp['areaAccessRestriction']['transportation']['text']).text_content()
        except:
            return "International travel info unavailable"
        
    def getDeclarationDocumentsInfo(self):
        '''
        return a list of documents to be declared before and after arrival
        without HTML tags
        '''
        try:
            docinfo = ""
            try:
                docinfo += self.resp['areaAccessRestriction']['declarationDocuments']['text']
            except:
                pass
            try:
                docinfo += self.resp['areaAccessRestriction']['declarationDocuments']['text']
            except:
                pass
            return lxml.html.fromstring(docinfo).text_content()
        except:
            return "Document travel info unavailable"
        
    def getTestingInfo(self):
        '''
        return covid testing information if any
        '''
        try:
            return lxml.html.fromstring(self.resp['areaAccessRestriction']['diseaseTesting']['text']).text_content()
            
        except:
            return "Testing info unavailable"
    
    def getMoreArrivalInfoLink(self):
        '''
        return official link for more arrival information if any
        '''
        try:
            return self.resp['areaAccessRestriction']['diseaseTesting']['rules']
            
        except:
            return "Arrival info unavailable"
        
    def getQuarintineInfo(self):
        '''
        return information about quarintine guidelines if any without HTML tags
        '''
        try:
            return lxml.html.fromstring(self.resp['areaAccessRestriction']['quarantineModality']['text']).text_content()
            
        except:
            return "Quarantine info unavailable"
        
    def getGeneralCovidInfo(self):
        '''
        return official covid related general link
        '''
        try:
            return self.resp['areaPolicy']['referenceLink']
            
        except:
            return "Quarantine info unavailable" 
    
    def getCovidAllInfo(self):
        '''
        return a list of HTML components with all the information required
        by an international traveller in Covid-19 for a 'country'
        '''
        content = [
                    html.Div(
                        children=html.P(children="Covid related information:"),
                        style={'font-size':'18px', 'font-weight':'bold'}
                    )
                ]
        
        text = "Info Link: " + self.getMoreInfoLink()
        content.append(
            html.Div(
                    children=html.P(children=text),
                    style={'font-size':'16px'}
                )
        )
        
        text = "Domestic Travel Restriction: " + self.getDomesticTravelRestrictions()
        content.append(
            html.Div(
                    children=html.P(children=text),
                    style={'font-size':'16px'}
                )
        )
        
        text = "Flight Info: " + self.getFlightInfo()
        content.append(
            html.Div(
                    children=html.P(children=text),
                    style={'font-size':'16px'}
                )
        )
        
        text = "Declaration Documents: " + self.getDeclarationDocumentsInfo()
        content.append(
            html.Div(
                    children=html.P(children=text),
                    style={'font-size':'16px'}
                )
        )
        
        text = "Testing Info: " + self.getTestingInfo()
        content.append(
            html.Div(
                    children=html.P(children=text),
                    style={'font-size':'16px'}
                )
        )
        
        text = "Arriving Info Link: " + self.getMoreArrivalInfoLink()
        content.append(
            html.Div(
                    children=html.P(children=text),
                    style={'font-size':'16px'}
                )
        )
        
        text = "Quarintine Info: " + self.getQuarintineInfo()
        content.append(
            html.Div(
                    children=html.P(children=text),
                    style={'font-size':'16px'}
                )
        )
        
        text = "General Covid Info: " + self.getGeneralCovidInfo()
        content.append(
            html.Div(
                    children=html.P(children=text),
                    style={'font-size':'16px'}
                )
        )
        

        return content
            

if __name__ == '__main__':
    api = ReadAPIKEYS("API_KEYS.txt")
    covidDetails = CovidInfo(api.getAPIKEY("API_KEY_AMADEUS"), api.getAPIKEY("API_SECRET_AMADEUS"))
    
    # Retrieving covid Info for Egypt
    covidDetails.getDetails("EG")
    #print(covidDetails.getSummary())
    print(covidDetails.getFlightInfo())
    #print(covidDetails.getDomesticTravelRestrictions())
    #print(covidDetails.getMoreArrivalInfoLink())
    #print(covidDetails.getGeneralCovidInfo())
    
        

        
        
        