import json
import os
# Developed libraries
import binance_interaction
import strategy
import environment


# Variable for the location of settings.json
import_filepath = "settings.json"


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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Get client
    client = environment.get_spot_client()
    status = True

    if status:
        # Import project settings

        # Retrieve account information
        account = binance_interaction.query_account(client=client)
        if account['canTrade']:
            print("Let's Do This!")
            strategy.strategy_one(client=client, timeframe="1h", percentage_rise=0.1, quote_asset="ETHBUSD")


