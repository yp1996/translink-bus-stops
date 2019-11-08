import requests
import json
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import os 
from dotenv import load_dotenv

def scrape_bus_stops(api_key, json_filename, start_range = 50000, end_range = 62000):

	stop_data = []

	with open(json_filename, 'w') as json_file:
	    for i in range(start_range, end_range):
	        response = requests.get(
	            'https://api.translink.ca/rttiapi/v1/stops/' + str(i),
	            params={'ApiKey': api_key})
	        if (response.status_code == 200):
	            root = ET.fromstring(response.text)
	            stop_no = root.find("StopNo").text
	            name = root.find("Name").text
	            lat = root.find("Latitude").text
	            lon = root.find("Longitude").text
	            routes = root.find("Routes").text
	            if (routes != None):
	                routes = routes.strip().replace(" ", ",").split(",")
	            else:
	                routes = -1 
	            json_obj = {
	                "StopNo": stop_no,
	                "Name": name,
	                "Latitude": lat,
	                "Longitude": lon,
	                "Routes": routes
	            }
	            stop_data.append(json_obj)
	    json.dump(stop_data, json_file)

if (__name__ == "__main__"):

	APP_ROOT = os.path.dirname(__file__)
	dotenv_path = os.path.join(APP_ROOT, '.env')
	load_dotenv(dotenv_path)
	api_key = os.getenv('API_KEY')
	scrape_bus_stops(api_key, 'stop_data.json', 58000, 58002)