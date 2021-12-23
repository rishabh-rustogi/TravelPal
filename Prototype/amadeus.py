# -*- coding: utf-8 -*-
import requests
from requests.structures import CaseInsensitiveDict
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


# Amadeus API testing client ID and Secret key
client_id = "xxx"
client_secret = "xxx"

# Retrieving access token with client_id and client_secret as authenticator
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://test.api.amadeus.com/v1/security/oauth2/token', client_id=client_id,
        client_secret=client_secret)


try:
    
    # Choosing the country (E.g. Egypt)
    country = "EG"
    
    # Creating the desired url
    url = "https://test.api.amadeus.com/v1/duty-of-care/diseases/covid19-area-report?countryCode=" + country
    
    # Setting up the appropriate header for request
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + token["access_token"]
    
    # Retreive the Covid related details for <country>
    resp = requests.get(url, headers=headers)
    print(resp.text)
except:
    
    # In case an error occurs
    print("cant find Covid Details")