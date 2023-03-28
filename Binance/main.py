import json
import os
# Developed libraries
import binance_interaction
import strategy


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
    # Get the status
    status = binance_interaction.query_binance_status()
    if status:
        # Import project settings
        project_settings = get_project_settings(import_filepath)
        # Set the keys
        api_key = project_settings['BinanceKeys']['Test_API_Key']
        secret_key = project_settings['BinanceKeys']['Test_Secret_Key']
        # Retrieve account information
        account = binance_interaction.query_account(api_key=api_key, secret_key=secret_key)
        if account['canTrade']:
            print("Let's Do This!")
            # strategy.strategy_one(timeframe="1h", percentage_rise=1, quote_asset="BUSD", project_settings=project_settings)


