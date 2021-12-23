# -*- coding: utf-8 -*-

'''
File Name: travelpal.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

ReadAPIKEYS class reads data from API_KEYS.txt, process it and then return the the API keys.

Files imported by this file: travelpalApp.py, travelpalAppLayout.py
'''

from travelpalApp import app
from travelpalAppLayout import constructApp

print("--------------------<< RUNNING SERVER NOW >>--------------------")

if __name__ == '__main__':
    '''
    Constructs the TravelPal app and runs it
    
    Main TravelPal application python file
    '''
    app.layout = constructApp()
    app.run_server(debug=True)