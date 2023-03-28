import json
import os
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

project_settings = get_project_settings("settings.json")
# Set the keys
api_key = project_settings['TestKeys']['Test_API_Key']
secret_key = project_settings['TestKeys']['Test_Secret_Key']

# create client object
client = Client(api_key, secret_key, testnet=True)

print(client.get_account())

