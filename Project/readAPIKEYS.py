# -*- coding: utf-8 -*-

'''
File Name: readAPIKEYS.py

Team Member Name:
Ayush Khandelwal
Daniel Deniger
Rishabh Rustogi
Kelly McManus

ReadAPIKEYS class reads data from API_KEYS.txt, process it and then return the the API keys.

Files importing this class: travelpalControl.py
'''

class ReadAPIKEYS:
    def __init__(self, filename):
        '''
        Reads API keys from a file
        
        Parameters
        ----------
        filename : str
            Filename containing API keys.
        '''
        # API keys
        self.API_KEYS = {}
        
        # Total keys
        self.notPresentAPIs = {"API_KEY_OPEN_WEATHER", "API_KEY_AMADEUS", "API_SECRET_AMADEUS", "API_KEY_GOOGLEMAP"}
        
        try:
            with open(filename, "r") as f:
                for line in f.readlines()[:]:
                    line  = line.split(" = ")
                    self.API_KEYS[line[0]] = line[1][:len(line[1])-1]
                    if line[0] in self.API_KEYS:
                        self.notPresentAPIs.remove(line[0])
                        
        except:
            print("[readAPIKEYS] Unable to process " + filename)
            exit()
        
        if len(self.notPresentAPIs) > 0:
            print("[readAPIKEYS] API keys not found: " + str(self.notPresentAPIs))
            
    def getAPIKEY(self, API):
        '''
        Return key for the requested API
        
        Parameters
        ----------
        API : str
            Name of the API.
        '''
        if API in self.API_KEYS:
            return self.API_KEYS[API]
        else:
            return None
            
        
        
        
            