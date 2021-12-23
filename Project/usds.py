# -*- coding: utf-8 -*-

'''
File Name: usds.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

USDSInfo class scrapes data from USDS website about visa realted information, process it and then return the data.

Files importing this class: travelpalControl.py
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
from matchCountry import MatchCountry
import pandas as pd


class USDSInfo:
    def setCountry(self, country):
        '''
        Set Country for retrieving visa related information
        from United States of America
        
        Parameters
        ----------
        country : str
            Country name for which to retrieve the regions.
        '''
        self.country = country.title().replace(' ', '') if (pd.isnull(MatchCountry.countries['usds'][country])) else MatchCountry.countries['usds'][country]
        self.url = "https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages/" + self.country + ".html"

    def getVisaInfo(self):
        '''
        Retrieve all the visa infromation from USDS website
        
        Generate a dictionary of all the visa realted information that
        can be gathers for any country.
        '''
        html = urlopen(self.url)
        bsyc = BeautifulSoup(html.read(), "lxml")

        # Builds two lists: quick facts titles and quick facts contents
        qf_title_list = bsyc.find_all('div', {"class": "tsg-rwd-qf-box-title"})
        qf_titles = []
        for i in qf_title_list:
            qf_titles.append(i.text)  # Need to clean further
        qf_content_list = bsyc.find_all('div', {"class": "tsg-rwd-qf-box-data"})
        qf_content = []
        for i in qf_content_list:
            qf_content.append(i.find('p').text)

        qf_titles_clean = []
        for t in qf_titles:
            qf_titles_split = t.split()
            title = ""
            for t in qf_titles_split:
                title += t + " "
            qf_titles_clean.append(title.strip().capitalize())

        # Zips dict of key=quick facts title, value= quick facts content
        visa_qf_dict = dict(zip(qf_titles_clean, qf_content))

        return visa_qf_dict # Return visa quick facts dict

    
    def getFormattedVisaSummary(self):
        '''
        Generate HTML content for visa related information
        
        Conversts dictionart of information to HTML content using tags
        '''
        info = self.getVisaInfo()
        
        formattedInfo = ""
        for key in info:
            formattedInfo += key + " " + info[key] + "\n\n"
            
        return formattedInfo

if __name__ == '__main__':
    usds = USDSInfo('Turkey')
    print(usds.getVisaInfo())


