# -*- coding: utf-8 -*-

'''
File Name: cdc.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

CDCInfo class scrapes data from CDC website about vaccines, process it and then return the data.

Files imported by this class: matchCountry.py

Files importing this class: travelpalControl.py
'''

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests
import pandas as pd
from matchCountry import MatchCountry
from dash import html


class CDCInfo:

    def setCountry(self, country):
        '''
        Retrieves data from CDC website
        
        Gets list of three types of vaccination guidelines recommend by CDC-
        -> Covid Vaccine Guidelines
        -> General Vaccination Guidelines
        -> Other Vaccination
        
        Parameters
        ----------
        country : str
            Country for which to retrieve data.
        '''
        self.unformattedCountry = country
        
        # Set country name to lowercase and replace space ' ' with '-'
        self.country = country.lower().replace(' ', '-') if (pd.isnull(MatchCountry.countries['cdc'][country])) else MatchCountry.countries['cdc'][country]
        self.url = "https://wwwnc.cdc.gov/travel/destinations/traveler/none/" + self.country
        
        html = urlopen(self.url)
        self.bsyc = BeautifulSoup(html.read(), "lxml")
        
        tbl_list = pd.read_html(self.url, index_col=0)
        tbl_list = tbl_list[0]
        del tbl_list['Clinical Guidance for Healthcare providers']
        self.vaccine_df = tbl_list

    def getCovidLevelLabel(self):
        '''
        Returns Covid level label
        
        Finds label for covid-19, extract level and returns it
        '''
        try:
            header_notice_list = self.bsyc.find_all('h4', attrs={"class": re.compile("notice-typename notice-typename*")})
            header_notice = header_notice_list[0]
            covid_level_label = header_notice.contents
            covid_level_label = covid_level_label[0]
            return covid_level_label  # str ex. 'Level 4: COVID-19 Very High'
        except:
            pass

        return None

    def getCovidLevelNumber(self):
        '''
        Returns Covid level number
        
        Finds level number for covid-19, extract level and returns it
        '''
        try:
            covid_level_number = int(re.findall(r'([0-9]):', self.getCovidLevelLabel())[0])
            return covid_level_number  # int
        except:
            pass

        return None

    def getCovidVaccineInfo(self):
        '''
        Returns Covid Recommendation
        
        Finds recommendation for covid-19, extract it and returns it
        '''
        try:
            covid_vaccine_df = self.vaccine_df.copy(deep=True)
            return covid_vaccine_df.loc['COVID-19']['Recommendations']
        except:
            pass

        return None

    def getOtherVaccineInfo(self):
        '''
        Returns Other Recommendation Dataframe
        
        Create a deep copy of extracted information, delete 
        Covid-19 column and then return its
        '''
        try:
            other_vaccines_df = self.vaccine_df.copy(deep=True)
            other_vaccines_df = other_vaccines_df.drop('COVID-19')
            return other_vaccines_df['Recommendations'].to_dict()
        except:
            pass

        return None
    
    def getVaccineSummary(self):
        '''
        Returns a List of three types of guidelines
        
        Create a list with 3 empty strings, replaces them with 
        appropriate information if available and returns it 
        '''
        result = ["", "", ""]
        covidInfo = self.getCovidVaccineInfo()
        if covidInfo != None:
            result[0] = "Covid Vaccine Guidelines: " + covidInfo + "\n\n"
            
        info = self.getOtherVaccineInfo()

        if info != None:
            
            # First read general vaccination information
            if 'Routine vaccines' in info:
                result[1] = "General Vaccine Guideline: " + info['Routine vaccines'] + "\n\n"
                del info['Routine vaccines']
        
            # Remaining list contains the vaccination disease names. So create a 
            # list of the same and return it 
            if len(info) > 0:
                temp = "Other Important Vaccines include-\n"
                keys = list(info.keys())
                for key in range(len(keys)):
                    temp += str(key+1) + ". " + keys[key] + "\n"
                result[2] = temp
        
        return result
    
    def getImage(self):
        '''
        Retrieve country image from CDC website
        
        Returns the image HTML tag with alternate text in case image 
        loading fails
        '''
        image = "https://wwwnc.cdc.gov/travel/images/map-" + self.country + ".png"
        text = "Unable to fetch country map for " + self.country
        return html.Img(
            alt=text,
            src=image, 
            style={'width':'100%', 'height':'100%','border-radius':'25px', 'background-color': '#000000'}
        )
    
    

if __name__ == '__main__':
    cdc = CDCInfo('United Kingdom')
    #print(cdc.getCovidLevelLabel())
    #print(cdc.getCovidLevelNumber())
    print(cdc.getCovidVaccineInfo())
    print(cdc.getOtherVaccineInfo())
