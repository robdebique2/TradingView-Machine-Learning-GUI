import json
import os
import pandas as pd
from binance.spot import Spot
from binance.client import Client

# Function to import settings from settings.json
def get_project_settings(importFilepath):
    # Test the filepath to sure it exists
    if os.path.exists(importFilepath):
        # Open the file
        f = open(importFilepath, "r")
        # Get the information from file
        project_settings = json.load(f)
        # Close the file
        f.close()
        # Return project settings to program
        return project_settings
    else:
        return ImportError

def get_spot_client():
    return get_keys("TestSpotKeys")

def get_futures_client():
    return get_keys("TestFuturesKeys")

def get_keys(testKeys):
    project_settings = get_project_settings("settings.json")
    api_key = project_settings[testKeys]['Test_API_Key']
    secret_key = project_settings[testKeys]['Test_Secret_Key']
    base_url = project_settings[testKeys]['Base_URL']
    # print(api_key, "    ", secret_key, "   ", base_url)
    if testKeys == "TestSpotKeys":
        return Spot(base_url=base_url, key=api_key, secret=secret_key)
    if testKeys == "TestFuturesKeys":
        return Client(api_key=api_key, api_secret=secret_key, testnet=True)
