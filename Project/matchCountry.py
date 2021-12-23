# -*- coding: utf-8 -*-

'''
File Name: matchCountrytion.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

MatchCountry class reads match_country.csv and then return the data.

Files importing this class: cdc.py, usds.py
'''

import pandas as pd

class MatchCountry:
    '''
    Reads match_country.csv for converting contry name to correct format
    '''
    countries = pd.read_csv('Files/match_countries.csv', index_col=0, header=0)

if __name__ == "__main__":
    print(MatchCountry.countries)
