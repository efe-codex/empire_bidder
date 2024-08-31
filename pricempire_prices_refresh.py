import json
import requests
import time

def refresh_prices(pricempire_api,sources):
    print("Starting price refresh process...")
    try:
        params = {
            "sources": sources,
            "api_key": pricempire_api
        }
        response = requests.get("https://api.pricempire.com/v3/items/prices", params=params)
        response.raise_for_status()  # Check for HTTP errors
        prices = response.json()

        with open("prices.json", "w") as outfile:
            json.dump(prices, outfile, indent=4)  # Save with indentation for readability

        print("Prices successfully updated.")
        return True
    except requests.exceptions.RequestException as req_err:
        print(f"HTTP error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON: {json_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

if __name__ == "__main__":
    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
        
        if refresh_prices(config.get("pricempire_api"),config.get("pricempire_sources")):
            print("Price refresh completed successfully.")
        else:
            print("Price refresh failed.")
    except FileNotFoundError:
        print("config.json not found. Please ensure the file exists and is in the correct location.")
    except json.JSONDecodeError:
        print("Error reading config.json. Please ensure it is formatted correctly.")
    
    time.sleep(5)
