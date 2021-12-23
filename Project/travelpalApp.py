# -*- coding: utf-8 -*-

'''
File Name: travelpalApp.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

This file initiate the dash app to seperate appfrom application layout and controller

Files importing this file: travelpal.py, travelpalAppLayout.py
'''

import dash

'''
Create the Dash app object
'''
app = dash.Dash(__name__)
app.title = 'TravelPal'