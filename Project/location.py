# -*- coding: utf-8 -*-

'''
File Name: location.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

Location class retrieves csv file from ourairports.com and pre-processed country and regions csv, process it and then return the data.
This class returns regions for a country, all country, and ISO code

Files importing this class: travelpalControl.py
'''

from collections import defaultdict
import pandas as pd


class Location:
    def __init__(self, countryFileName, regionFileName):
        '''
        Generate lists for countries and their ISO code
        
        Generate list of countries, dictionary of regions within
        the country, list of countries ISO2 codes, dataFrame for munipalities
        
        Parameters
        ----------
        countryFileName : str
            Filename for csv containing all the countries.
        regionFileName : str
            Filename for csv containing all the regions.
        '''
        self.country = defaultdict(list)
        self.countryISO = {}
        self.ISOCountryMap = {}

        airports_df = pd.read_csv('https://davidmegginson.github.io/ourairports-data/airports.csv', header=0)
        self.muni_df = airports_df[['iso_country', 'municipality']].drop_duplicates()

        try:
            with open(countryFileName, "r", encoding="utf-8") as f:
                for line in f.readlines()[1:]:
                    line = line.replace('"', '').split(",")
                    if "unassigned" not in line[2]:
                        self.countryISO[line[2]] = line[1]
                        self.ISOCountryMap[line[1]] = line[2]
        except Exception as e:
            print("[Location] Unable to process country file " + countryFileName)
            exit()
            
        try:
            with open(regionFileName,"r", encoding="utf-8") as f:
                for line in f.readlines()[1:]:
                    line  = line.replace('"','').split(",")
                    if len(line) >= 7 and line[3] != "(unassigned)" and line[5] in self.ISOCountryMap:
                        self.country[self.ISOCountryMap[line[5]]].append(line[3])
        except:
            print("[Location] Unable to process region file " + regionFileName)
            exit()
        
        self.ISOCountryMap.clear()
        
    def getRegions(self, country):
        '''
        Returns a list of regions for a country
        
        Parameters
        ----------
        country : str
            Country name for which to retrieve the regions.
        '''
        if country in self.country:
            return self.country[country]
        return []
    
    def getISO(self, country):
        '''
        Returns ISO2 code for a country
        
        Parameters
        ----------
        country : str
            Country name for which to retrieve the ISO2 code.
        '''
        if country in self.countryISO:
            return self.countryISO[country]
        return ''
    
    def getAllCountry(self):
        '''
        Returns a list of all the countries without 'United States'
        '''
        allCountries = list(self.countryISO.keys())
        allCountries.remove('United States')
        allCountries.remove('United States Minor Outlying Islands')
        allCountries.sort()
        return allCountries

    def getMunicipalities(self, country):
        iso = self.getISO(country)
        return list(self.muni_df.query("iso_country=='{}'".format(iso)).municipality)
    
if __name__ == '__main__':
    country = Location("files/countries.csv", "files/regions.csv")
    print(country.getAllCountry())
    print(country.getRegions("India"))
    print(country.countryISO)
    print(country.getMunicipalities('Afghanistan'))
    

