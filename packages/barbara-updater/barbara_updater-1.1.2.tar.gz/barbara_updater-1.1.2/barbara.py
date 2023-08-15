#!/usr/bin/env python3
# Ran from 5/11 - 6/17/23. Error unknown, so added many print error statements, add specifics 6/26/23
# comment out code that produces url and pushes to google drive
# Check why Lincoln IL didnt work for a radiosonde choice
# timestamp on display
# national radar and satellite
# when NWS forecast page doesn't lead to 3-letter code, can leave radiosonde option w/o/ choice
# different scenarios when radiosonde stations not found
# On 7-26-23 this code is the same as 7-18-23.py which I'm prerparing to share

import smbus
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import time #allows the sleep commands
from time import strftime
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from matplotlib import pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
import pandas as pd
import json
import io
from io import BytesIO
from PIL import Image
import matplotlib.image as mpimg
import traceback
from PIL import Image, ImageDraw, ImageFont
import re
import imageio
from matplotlib.animation import FuncAnimation
import os
#from google.oauth2 import service_account
#from google.oauth2.credentials import Credentials
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from googleapiclient.http import MediaIoBaseUpload
from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import urllib.parse
from geopy.exc import GeocoderUnavailable
import subprocess

rcParams['figure.figsize'] = 12,6

# Create a figure for plotting
light_blue = (0.8, 0.9, 1.0)
fig = plt.figure(facecolor=light_blue)
ax = fig.add_subplot(1, 1, 1)
bx = fig.add_subplot(1, 1, 1, label="unique_label")

#shut off Thonny navigation toolbar
if fig.canvas.toolbar:
    fig.canvas.toolbar.pack_forget()

plt.axis('off')

xs = []
ys = []

#global sonde_letter_identifier 
global radar_identifier
global day
global hourmin_str

now = datetime.now()
current_year = float(now.strftime("%Y"))

def get_location():
    try:
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        if data['status'] == 'success':
            lat = data['lat']
            lon = data['lon']
            return float(lat), float(lon)
    except requests.exceptions.RequestException:
        pass
    return None

def get_aobs_site(latitude, longitude):
    global baro_input
    aobs_url = generate_aobs_url(latitude, longitude)
    nearest_html = requests.get(aobs_url)
    nearest_soup = BeautifulSoup(nearest_html.content, 'html.parser')
    panel_title = nearest_soup.find('h2', class_='panel-title')
    
    if panel_title:
        aobs_site = panel_title.text.strip()
        current_conditions = nearest_soup.find(id='current_conditions_detail')
        
        if current_conditions and isinstance(current_conditions, Tag):
            tds = current_conditions.find_all('td')
            
            if len(tds) > 5 and tds[5].string is not None:
                baro_input = tds[5].string.strip()
                
                try:
                    baro_input = float(baro_input[:5])
                    return aobs_site
                except ValueError:
                    print("This site doesn't have a barometric pressure reading we can use.")
                    print("Please choose an alternate site when given the chance.")
        else:
            print("The barometric reading at this site is not available for use.")
    else:
        print("Observation site not found.")
    
    return None

def get_standard_radar_site_url(latitude, longitude):
    global radar_site, radar_site_url
    aobs_url = generate_aobs_url(latitude, longitude)
    nws_html = requests.get(aobs_url)
    nws_soup = BeautifulSoup(nws_html.content, 'html.parser')
    radar_img = nws_soup.find('img', src=lambda src: src and 'radar.weather.gov/ridge/standard' in src)
    if radar_img:
        radar_src = radar_img['src']
        radar_site_url = radar_src.split('"')[0]
        radar_site = radar_src.split("standard/")[1][:4]
        radar_site_url = radar_site_url.replace('_0.gif', '_loop.gif')
        return radar_site_url
    return "Standard Radar site URL not found"

def generate_aobs_url(latitude, longitude, aobs_site=''):
    aobs_url = f"https://forecast.weather.gov/MapClick.php?lon={longitude}&lat={latitude}"
    if aobs_site:
        aobs_url += f"&site={aobs_site}"
    return aobs_url

# station_list_url is list of radiosonde sites
station_list_url = "https://www1.ncdc.noaa.gov/pub/data/igra/igra2-station-list.txt"

def get_nearest_radiosonde_station(latitude, longitude):
    response = requests.get(station_list_url)
    station_data = response.text.splitlines()[2:]  # Skip header lines

    min_distance = float('inf')
    nearest_station = None

    for station in station_data:
        station_info = station.split()

        try:
            station_lat = float(station_info[1])
            station_lon = float(station_info[2])
            sonde_town = " ".join(station_info[5:-3])  # Join town name with spaces
            sonde_state = station_info[4]
            station_year = station_info[-2]  # Second column from the right

            if station_year.isdigit() and int(station_year) in {current_year, current_year - 1}:
                distance = calculate_distance(latitude, longitude, station_lat, station_lon)
                if distance < min_distance:
                    min_distance = distance
                    nearest_station = sonde_town + ", " + sonde_state
        except (ValueError, IndexError):
            continue  # Skip station if there are errors in extracting data

    return nearest_station

def calculate_distance(latitude1, longitude1, latitude2, longitude2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [latitude1, longitude1, latitude2, longitude2])

    # Haversine formula for distance calculation
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Earth radius in kilometers

    return distance

# Example usage
location = get_location()
if location:
    latitude, longitude = location
    aobs_site = get_aobs_site(latitude, longitude)
    standard_radar_site_url = get_standard_radar_site_url(latitude, longitude)

    if aobs_site:
        print("Welcome to The Weather Observer!")
        print("In order to begin, your new instrument needs to be calibrated,")
        print("and you need to make choices about which weather to observe.")
        print(" ")
        print("The nearest NWS Observation site found is:", aobs_site)
        print("This site will be used to calibrate the first barometric pressure reading.")
        print("The current barometric pressure reading there is: {:.2f} inches".format(baro_input))
        print(" ")
        print("The nearest radar site is:", radar_site)
        print("This site will be used to display local radar.")
        nearest_radiosonde_station = get_nearest_radiosonde_station(latitude, longitude)
        print(" ")
        print("The nearest radiosonde site is:", nearest_radiosonde_station)
        print("This site will be used to show a skew t log p diagram.")
        print(" ")
    else:
        print("Default observation site not found.")

# Suppress the error message by redirecting standard error output to /dev/null
os.system("onboard 2>/dev/null &")

valid_choices = ['y', 'n']

try:
    change_site = input("Do you want to change the site used for calibration? (y/n): ")
    while change_site.lower() not in valid_choices:
        print("Invalid input. Please enter 'y' or 'n'.")
        change_site = input("Do you want to change the site used for calibration? (y/n): ")

except KeyboardInterrupt:
    # Perform cleanup tasks or handle interruption during input prompt
    print("\nKeyboardInterrupt occurred. Opening terminal window...")

    # Open a new terminal window
    subprocess.run(["lxterminal"])

if change_site.lower() == "y":
    while True:
        alternative_town = input("Please enter the town name: ")
        alternative_state = input("Please enter the 2-letter ID for the state: ").upper()

        try:
            # Geocode the alternative town to get the latitude and longitude
            geolocator = Nominatim(user_agent="geocoder_app")
            location = geolocator.geocode(f"{alternative_town}, {alternative_state}", country_codes="us")

            if location is not None:
                alternative_latitude = location.latitude
                alternative_longitude = location.longitude

                # Generate the NWS URL for the alternative site
                aobs_url = generate_aobs_url(alternative_latitude, alternative_longitude)
                alternative_html = requests.get(aobs_url)
                alternative_soup = BeautifulSoup(alternative_html.content, 'html.parser')

                current_conditions_detail = alternative_soup.find(id='current_conditions_detail')
                if current_conditions_detail is not None:
                    nearest_baro = current_conditions_detail.find_all('td')[5]

                    if nearest_baro is not None:
                        baro_string = nearest_baro.string.strip()
                        baro_match = re.search(r'\d+\.\d+', baro_string)
                        if baro_match:
                            baro_input = float(baro_match.group())
                            observation_site = alternative_soup.find("h2", class_="panel-title").text.strip()
                            print("Closest observation site to", alternative_town + ", " + alternative_state,
                                  "is:", observation_site)
                            print("The barometric pressure reading there is: {:.2f} inches".format(baro_input))
                            confirm_site = input("Is this the observation site you want to use? (y/n): ")
                            if confirm_site.lower() == "y":
                                break  # Exit the loop and continue with the selected observation site
                        else:
                            print("This site doesn't have a barometric pressure reading that can be used.")
                else:
                    print("Failed to retrieve barometric pressure data for the alternative observation site.")
            else:
                print("Failed to retrieve latitude and longitude for the specified town and state.")
        except GeocoderUnavailable:
            print("Geocoding service is unavailable. Please try again later.")

else:
    print("Using default calibration site.")

print(" ")
radar_identifier = radar_site[-3:]
change_radar_site = input("Do you want to change the radar site? (y/n): ")
while change_radar_site.lower() not in ["y", "n"]:
    print("Invalid input. Please enter 'y' or 'n'.")
    change_radar_site = input("Do you want to change the radar site? (y/n): ")

if change_radar_site.lower() == "y":
    confirmed = False
    while not confirmed:
        radar_identifier = input("Please enter the 3-letter identifier of the radar site: ").upper()
        radar_url = f"https://radar.weather.gov/ridge/standard/K{radar_identifier}_loop.gif"

        response = requests.head(radar_url)
        if response.status_code == 200:
            radar_site_url = radar_url
            print("The local radar site has been updated to:", radar_identifier)
            confirm_choice = input("Is this the radar site you want? (y/n): ")
            while confirm_choice.lower() not in ["y", "n"]:
                print("Invalid input. Please enter 'y' or 'n'.")
                confirm_choice = input("Is this the radar site you want? (y/n): ")
            if confirm_choice.lower() == "y":
                confirmed = True
            else:
                print("Please choose another radar site.")
        else:
            print("Invalid radar site. Please choose another radar site.")
else:
    pass

# using this website to keep track of radiosonde sites
# https://www1.ncdc.noaa.gov/pub/data/igra/igra2-station-list.txt
# will write to them and ask when master list is updated upon change of year

print("")
global sonde_letter_identifier

sonde_letter_identifier = nearest_radiosonde_station

change_radiosonde_site = input("Do you want to change the radiosonde site? (y/n): ")

while change_radiosonde_site.lower() not in valid_choices:
    print("Invalid input. Please enter 'y' or 'n'.")
    change_radiosonde_site = input("Do you want to change the radiosonde site? (y/n): ")

if change_radiosonde_site.lower() == "y":
    radiosonde_state = input("Please enter the 2-letter ID of the state: ").upper()

    # Check if the entered value is a 2-letter state ID
    while len(radiosonde_state) != 2 or not radiosonde_state.isalpha():
        print("Invalid state ID. Please enter a 2-letter state ID.")
        radiosonde_state = input("Please enter the 2-letter ID of the state: ").upper()

    response = requests.get(station_list_url)
    station_data = response.text.splitlines()[2:]  # Skip header lines

    active_radiosonde_sites = []

    for station in station_data:
        station_info = station.split()
        sonde_state = station_info[4]
        sonde_town = " ".join(station_info[5:-3])  # Join town name with spaces
        station_year = station_info[-2]  # Second column from the right

        if station_year.isdigit() and int(station_year) in {current_year, current_year - 1}:
            if sonde_state == radiosonde_state:
                active_radiosonde_sites.append(sonde_town)

    while not active_radiosonde_sites:
        print("No active radiosonde sites found in", radiosonde_state)
        radiosonde_state = input("Please enter another 2-letter ID of the state: ").upper()

        # Check if the entered value is a 2-letter state ID
        while len(radiosonde_state) != 2 or not radiosonde_state.isalpha():
            print("Invalid state ID. Please enter a 2-letter state ID.")
            radiosonde_state = input("Please enter the 2-letter ID of the state: ").upper()

        active_radiosonde_sites = []

        for station in station_data:
            station_info = station.split()
            sonde_state = station_info[4]
            sonde_town = " ".join(station_info[5:-3])  # Join town name with spaces
            station_year = station_info[-2]  # Second column from the right

            if station_year.isdigit() and int(station_year) in {current_year, current_year - 1}:
                if sonde_state == radiosonde_state:
                    active_radiosonde_sites.append(sonde_town)

    if active_radiosonde_sites:
        print("Available Radiosonde Sites in", radiosonde_state + ":")
        for site in active_radiosonde_sites:
            print(site)

        alternative_town = input("Please enter the town from the above list: ").upper()

        selected_radiosonde_station = None

        for station in station_data:
            station_info = station.split()
            sonde_state = station_info[4]
            sonde_town = " ".join(station_info[5:-3])  # Join town name with spaces
            if sonde_state == radiosonde_state and sonde_town == alternative_town:
                selected_radiosonde_station = sonde_town + ", " + sonde_state
                break

        if selected_radiosonde_station is not None:
            print("New radiosonde site:", selected_radiosonde_station)

            while True:
                try:
                    # Use geopy to get the latitude and longitude of the town
                    geolocator = Nominatim(user_agent="my_app")
                    location = geolocator.geocode(f"{sonde_town}, {sonde_state}, USA")

                    if location is None:
                        print("Location not found.")
                    else:
                        latitude = location.latitude
                        longitude = location.longitude

                        # Build the URL for the NWS office based on latitude and longitude
                        nws_url = f"https://forecast.weather.gov/MapClick.php?lat={latitude}&lon={longitude}"

                        try:
                            # Fetch the HTML content of the NWS office page
                            response = requests.get(nws_url)
                            response.raise_for_status()

                            # Parse the HTML content
                            soup = BeautifulSoup(response.content, "html.parser")

                            # Find the Local Forecast Office link and extract the 3-letter code
                            local_forecast_link = soup.find("a", id="localWFO")

                            if local_forecast_link:
                                local_forecast_url = local_forecast_link["href"]

                                # Extract the NWS 3-letter code from the Local Forecast Office URL
                                code_match = re.search(r"https://www.weather.gov/([A-Za-z]{3})/", local_forecast_url)
                                if code_match:
                                    sonde_letter_identifier = code_match.group(1).upper()  # Convert to uppercase
                                    #print(f"NWS 3-Letter Code for {sonde_town}, {sonde_state}: {sonde_letter_identifier}")
                                else:
                                    print("NWS 3-Letter Code not found in the Local Forecast Office URL.")
                            else:
                                print("Could not match site with its 3-letter code.")
                        except requests.RequestException as e:
                            print("Error occurred during API request:", str(e))
                        break
                except requests.RequestException as e:
                    print("Error occurred during API request:", str(e))
else:
    # Use default town and state to generate the sonde_letter_identifier
    sonde_town, sonde_state = nearest_radiosonde_station.split(", ")

    try:
        # Use geopy to get the latitude and longitude of the town
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.geocode(f"{sonde_town}, {sonde_state}, USA")

        if location is None:
            print("Location not found.")
        else:
            latitude = location.latitude
            longitude = location.longitude

            # Build the URL for the NWS office based on latitude and longitude
            nws_url = f"https://forecast.weather.gov/MapClick.php?lat={latitude}&lon={longitude}"

            try:
                # Fetch the HTML content of the NWS office page
                response = requests.get(nws_url)
                response.raise_for_status()

                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")

                # Find the Local Forecast Office link and extract the 3-letter code
                local_forecast_link = soup.find("a", id="localWFO")

                if local_forecast_link:
                    local_forecast_url = local_forecast_link["href"]

                    # Extract the NWS 3-letter code from the Local Forecast Office URL
                    code_match = re.search(r"https://www.weather.gov/([A-Za-z]{3})/", local_forecast_url)
                    if code_match:
                        sonde_letter_identifier = code_match.group(1).upper()  # Convert to uppercase
                        print(f"NWS 3-Letter Code for {sonde_town}, {sonde_state}: {sonde_letter_identifier}")
                    else:
                        print("NWS 3-Letter Code not found in the Local Forecast Office URL.")
                else:
                    print("Could not match site with its 3-letter code.")
            except requests.RequestException as e:
                print("Error occurred during API request:", str(e))
    except requests.RequestException as e:
        print("Error occurred during API request:", str(e))


valid_choices = ['y', 'n']

# Prompt the user to pick 3 observation sites
print(" ")
print("You will now choose 3 observation sites to be displayed at the top of the display.")

# Observation Site 1
confirmed_site_1 = False
while not confirmed_site_1:
    print(" ")
    alternative_town_1 = input("Please enter the town name for Observation Site 1: ")
    alternative_state_1 = input("Please enter the 2-letter ID for the state for Observation Site 1: ").upper()

    try:
        # Geocode the alternative town to get the latitude and longitude
        geolocator = Nominatim(user_agent="geocoder_app")
        location_1 = geolocator.geocode(f"{alternative_town_1}, {alternative_state_1}", country_codes="us")

        if location_1 is not None:
            alternative_latitude_1 = location_1.latitude
            alternative_longitude_1 = location_1.longitude

            # Generate the NWS URL for the alternative site
            aobs_url = generate_aobs_url(alternative_latitude_1, alternative_longitude_1)
            alternative_html = requests.get(aobs_url)
            alternative_soup = BeautifulSoup(alternative_html.content, 'html.parser')

            extended_forecast = alternative_soup.find("div", id="seven-day-forecast")
            if extended_forecast is not None:
                aobs_town = extended_forecast.find("h2", class_="panel-title").text.strip()
                print("Observation Site 1: " + aobs_town)
                confirm_observation_site_1 = input("Is this the observation site you want? (y/n): ")
                if confirm_observation_site_1.lower() == "y":
                    confirmed_site_1 = True
                else:
                    print("Please choose another observation site for Observation Site 1.")
            else:
                print("Failed to retrieve observation site for Observation Site 1.")
        else:
            print("Failed to retrieve latitude and longitude for the specified town and state for Observation Site 1.")
    except GeocoderUnavailable:
        print("Geocoding service is unavailable. Please try again later.")

# Observation Site 2
confirmed_site_2 = False
while not confirmed_site_2:
    print(" ")
    alternative_town_2 = input("Please enter the town name for Observation Site 2: ")
    alternative_state_2 = input("Please enter the 2-letter ID for the state for Observation Site 2: ").upper()

    try:
        # Geocode the alternative town to get the latitude and longitude
        geolocator = Nominatim(user_agent="geocoder_app")
        location_2 = geolocator.geocode(f"{alternative_town_2}, {alternative_state_2}", country_codes="us")

        if location_2 is not None:
            alternative_latitude_2 = location_2.latitude
            alternative_longitude_2 = location_2.longitude

            # Generate the NWS URL for the alternative site
            bobs_url = generate_aobs_url(alternative_latitude_2, alternative_longitude_2)
            alternative_html = requests.get(bobs_url)
            alternative_soup = BeautifulSoup(alternative_html.content, 'html.parser')

            extended_forecast = alternative_soup.find("div", id="seven-day-forecast")
            if extended_forecast is not None:
                bobs_town = extended_forecast.find("h2", class_="panel-title").text.strip()
                print("Observation Site 2: " + bobs_town)
                confirm_observation_site_2 = input("Is this the observation site you want? (y/n): ")
                if confirm_observation_site_2.lower() == "y":
                    confirmed_site_2 = True
                else:
                    print("Please choose another observation site for Observation Site 2.")
            else:
                print("Failed to retrieve observation site for Observation Site 2.")
        else:
            print("Failed to retrieve latitude and longitude for the specified town and state for Observation Site 2.")
    except GeocoderUnavailable:
        print("Geocoding service is unavailable. Please try again later.")

# Observation Site 3
confirmed_site_3 = False
while not confirmed_site_3:
    print(" ")
    alternative_town_3 = input("Please enter the town name for Observation Site 3: ")
    alternative_state_3 = input("Please enter the 2-letter ID for the state for Observation Site 3: ").upper()

    try:
        # Geocode the alternative town to get the latitude and longitude
        geolocator = Nominatim(user_agent="geocoder_app")
        location_3 = geolocator.geocode(f"{alternative_town_3}, {alternative_state_3}", country_codes="us")

        if location_3 is not None:
            alternative_latitude_3 = location_3.latitude
            alternative_longitude_3 = location_3.longitude

            # Generate the NWS URL for the alternative site
            cobs_url = generate_aobs_url(alternative_latitude_3, alternative_longitude_3)
            alternative_html = requests.get(cobs_url)
            alternative_soup = BeautifulSoup(alternative_html.content, 'html.parser')

            extended_forecast = alternative_soup.find("div", id="seven-day-forecast")
            if extended_forecast is not None:
                cobs_town = extended_forecast.find("h2", class_="panel-title").text.strip()
                print("Observation Site 3: " + cobs_town)
                confirm_observation_site_3 = input("Is this the observation site you want? (y/n): ")
                if confirm_observation_site_3.lower() == "y":
                    confirmed_site_3 = True
                else:
                    print("Please choose another observation site for Observation Site 3.")
            else:
                print("Failed to retrieve observation site for Observation Site 3.")
        else:
            print("Failed to retrieve latitude and longitude for the specified town and state for Observation Site 3.")
    except GeocoderUnavailable:
        print("Geocoding service is unavailable. Please try again later.")

# command to close Onboard keyboard
#os.system("pkill onboard")

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    global correction_factor
    global cycle_counter, frame_index #added while trying to display looping radar
    # Get I2C bus
    bus = smbus.SMBus(1)
    
    # HP203B address, 0x77(118)
    # Send OSR and channel setting command, 0x44(68)
    bus.write_byte(0x77, 0x44 | 0x00)

    time.sleep(0.5)

    # HP203B address, 0x77(118)
    # Read data back from 0x10(16), 6 bytes
    # cTemp MSB, cTemp CSB, cTemp LSB, pressure MSB, pressure CSB, pressure LSB
    data = bus.read_i2c_block_data(0x77, 0x10, 6)

    # Convert the data to 20-bits
    # Correct for 160 feet above sea level
    # cpressure is pressure corrected for elevation
    cTemp = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
    fTemp = (cTemp * 1.8) + 32
    pressure = (((data[3] & 0x0F) * 65536) + (data[4] * 256) + data[5]) / 100.00
    cpressure = (pressure * 1.0058)
    inHg = (cpressure * .029529)
    #print (inHg)
    
    if i < 1:
        
        correction_factor = (baro_input/inHg)
        
    inHg = correction_factor * inHg
    #print (baro_input, correction_factor, inHg)

    # HP203B address, 0x77(118)
    # Send OSR and channel setting command, 0x44(68)
    bus.write_byte(0x77, 0x44 | 0x01)

    time.sleep(0.5)

    # HP203B address, 0x76(118)
    # Read data back from 0x31(49), 3 bytes
    # altitude MSB, altitude CSB, altitude LSB
    data = bus.read_i2c_block_data(0x77, 0x31, 3)

    # Convert the data to 20-bits
    altitude = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
    
    if i == 1:        
        #command to close Onboard keyboard
        os.system("pkill onboard")
    
    if i > 1:
        
        # Specify the file path to your credentials JSON file
        #credentials_path = '/home/pi/Downloads/credentials.json'

        # Define the scopes for accessing Google Drive
        #scopes = ['https://www.googleapis.com/auth/drive.file']

        # Load the saved credentials from the token file
        #credentials = Credentials.from_authorized_user_file('token.json', scopes)

        # Create the drive_service object
        #drive_service = build('drive', 'v3', credentials=credentials)

        # Save the image using plt.savefig()
        plt.savefig('baro_trace.png')

        # Upload the image to Google Drive
        #file_metadata = {'name': 'baro_trace.png'}
        #media_body = MediaIoBaseUpload(open('baro_trace.png', 'rb'), mimetype='image/png')
        #upload_request = drive_service.files().create(body=file_metadata, media_body=media_body)
        #upload_response = upload_request.execute()

        #file_id = upload_response['id']
        #permission = drive_service.permissions().create(fileId=file_id, body={'role': 'reader', 'type': 'anyone'}).execute()
        #image_download_url = f"https://drive.google.com/uc?id={file_id}"
        #print(f"Image URL: {image_download_url}")
       
        # Read the saved image file
        #with open('baro_trace.png', 'rb') as image_file:
            #image_data = image_file.read()

        # Get the file ID of the previous image (assuming you have stored it previously)
        #previous_image_file_id = '1G3d1WDyUcFmEdD3re8oKi45tM8MP7oma'

        # Update the existing file with the latest image data
        #media_body = MediaIoBaseUpload(io.BytesIO(image_data), mimetype='image/png')
        #update_request = drive_service.files().update(fileId=previous_image_file_id, media_body=media_body)
        #update_response = update_request.execute()

        #print("Image updated successfully in Google Drive.")

        ax.clear()
        bx.clear()
        
        now = datetime.now() # current date and time
        day = now.strftime("%A")
        hourmin_str = now.strftime("%H:%M")
        
        # Adjust margins
        
        fig.subplots_adjust(left=0.125, right=0.90, bottom=0, top=0.88)
        
        ax.text(0, 1.09, "The",
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
    
        ax.text(0, 1.05, "Weather",
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
 
        ax.text(0, 1.01, "Observer",
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
        
        ax.text(.11, 1.01, f'Last Updated\n{now.strftime("%A")}\n{now.strftime("%I:%M %P")}', 
            transform=ax.transAxes,
            fontweight='light', fontstyle='italic', horizontalalignment='left', fontsize=6)   
        
        try:
            global atemp, awind, btemp, bwind, ctemp, cwind
            
            ax.text(.80, 1.09, aobs_town,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
    
            ax.text(.80, 1.05, atemp,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
 
            ax.text(.80, 1.01, awind,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
    
        except Exception as e:
            print( "a obs error:", e)
            pass
    
        try:
        
            ax.text(.50, 1.09, bobs_town,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
    
            ax.text(.50, 1.05, btemp,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
 
            ax.text(.50, 1.01, bwind,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
        except Exception as e:
            print("b Obs error:", e)
            pass

        try:
            ax.text(.20, 1.09, cobs_town,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
            ax.text(.20, 1.05, ctemp,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)

            ax.text(.20, 1.01, cwind,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
        except Exception as e:
            print("c obs error:", e)
            pass
               
        # Display the regional composite radar image in the subplot
        try:           
            # Scrape and save the regional composite radar image
            radar_url = 'https://radar.weather.gov/ridge/standard/CONUS_0.gif'
            radar_response = requests.get(radar_url)
            radar_content = radar_response.content
            radar_image = Image.open(BytesIO(radar_content))
            radar_image.save('radar.png', 'PNG')            
            
            if radar_response.status_code == 200:
                radar_image = Image.open('radar.png')
                bx.imshow(radar_image)
                ax.axis('off')
                bx.axis('off')
                plt.draw()
                plt.pause(7)            
            else:            
                pass
        except Exception as e:
            print("Scrape, save and Display regional radar", e)
            pass
        
        # Scrape, Save and Display GYX radar in the subplot
        try:
            global radar_identifier
            radar_loop_url = f"https://radar.weather.gov/ridge/standard/K{radar_identifier}_loop.gif"

            # Scrape and save the radar GIF
            radar_loop_response = requests.get(radar_loop_url)
            if radar_loop_response.status_code == 200:
                with open('radar_loop.gif', 'wb') as f:
                    f.write(radar_loop_response.content)

            # Open the radar GIF and extract frames
            radar_loop_image = Image.open('radar_loop.gif')
            radar_frames = []
            try:
                while True:
                    radar_frames.append(radar_loop_image.copy())
                    radar_loop_image.seek(len(radar_frames))  # Move to the next frame
            except EOFError:
                pass

            # Display the frames in a loop, cycling 2 times
            num_cycles = 2

            plt.ion()  # Turn on interactive mode

            # Pre-load the frames into memory before starting the loop
            preloaded_frames = [radar_frame.copy() for radar_frame in radar_frames]

            for cycle in range(num_cycles):
                for radar_frame in preloaded_frames:
                    bx.imshow(radar_frame)
                    plt.draw()
                    plt.pause(0.01)  # Pause for a short duration between frames

        except Exception as e:
            print("Scrape, Save and Display local radar", e)
            pass
                      
        # Scrape, Save and Display the satellite image in the subplot
        try:
            satellite_url = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/1250x750.jpg'
            satellite_response = requests.get(satellite_url)
            satellite_content = satellite_response.content
            satellite_image = Image.open(BytesIO(satellite_content))
            satellite_image.save('satellite.png', 'PNG')
            
            if satellite_response.status_code == 200:                        
                satellite_image = Image.open('satellite.png')
                bx.imshow(satellite_image, aspect='equal')
                ax.axis('off')
                bx.axis('off')
                plt.draw()
                plt.pause(7)
            else:
                pass
        except Exception as e:
            print("Scrape, Save and Display satellite image", e)
            pass        
        
        # Scrape, Save and Display the surface analysis in the subplot
        try:           
            sfc_url = 'https://www.wpc.ncep.noaa.gov/basicwx/92fndfd.gif'
            sfc_response = requests.get(sfc_url)
            sfc_content = sfc_response.content        
            sfc_image = Image.open(BytesIO(sfc_content))
            sfc_image.save('sfc.png', 'PNG')
        
            if sfc_response.status_code == 200:           
                sfc_image = Image.open('sfc.png')
                bx.imshow(sfc_image)
                ax.axis('off')
                bx.axis('off')
                plt.draw()
                plt.pause(7)
            else:
                pass
        except Exception as e:
            print("Scrape, Save and Display sfc analysis", e)
            pass
        
        # Scrape, Save and Display the GYX sounding in the subplot
        try:
            # Get current UTC time and date
            scrape_now = datetime.utcnow()

            if scrape_now.hour >= 1 and scrape_now.hour < 13:
                # Use 00z for current UTC date
                date_str = scrape_now.strftime("%y%m%d00")
                hour_str = "00Z"
            else:
                # Use 12z for current UTC date
                hour_str = "12Z"
                date_str = scrape_now.strftime("%y%m%d12")
                if scrape_now.hour < 1:
                    # Use previous UTC date for 00z images
                    scrape_now -= timedelta(days=1)
                    date_str = scrape_now.strftime("%y%m%d12")
                    
            month_str = scrape_now.strftime("%b").capitalize()
            day_str = str(scrape_now.day)

            # Construct image URL
            sound_url = f"https://www.spc.noaa.gov/exper/soundings/{date_str}_OBS/{sonde_letter_identifier}.gif"
            
            # Send a GET request to the image URL to get the image content
            sound_response = requests.get(sound_url)

            # Save the image using Pillow
            sound_img = Image.open(BytesIO(sound_response.content))
            
            # Crop the top 50 pixels from the image
            crop_box = (0, 250, sound_img.width, sound_img.height)
            sound_img = sound_img.crop(crop_box)
            
            sound_img.save('sound.png', 'PNG')
        
            # Pause for 2 seconds include this time when showing baro
            plt.pause(2)
        
            if sound_response.status_code == 200:
                sound_img = Image.open('sound.png')
                
                # Calculate the aspect ratio of the image               
                sound_img = sound_img.convert('RGBA')
                aspect_ratio = sound_img.width / sound_img.height

                # Set the size of the displayed image to 8 inches by 8 inches
                display_width = 0.83
                display_height = 1

                # Calculate the extent of the displayed image
                display_extent = [0, display_width, 0, display_height / aspect_ratio]

                # Create a new image with a white background
                sound_img_with_white_bg = Image.new('RGBA', (int(sound_img.width), int(sound_img.height)), (255, 255, 255, 255))
                sound_img_with_white_bg.paste(sound_img, (0, 0), sound_img)

                sound_img_with_white_bg.save('sound_img.png', 'PNG')

                # Display the image with the adjusted extent
                bx.imshow(sound_img_with_white_bg, extent=display_extent)
           
                # Add the text to the subplot
                bx.text(0.28, 0.89, f'{month_str} {day_str} {hour_str}\n{sonde_town} {sonde_state}', ha='left', va='center', fontweight='bold', transform=bx.transAxes)
            
                ax.axis('off')
                bx.axis('off')
                plt.draw()
                plt.pause(13)
            else:
                pass
        except Exception as e:
            print("Scrape, Save and Display sounding", e)
            pass
                   
        bx.clear()
        bx.axis('off')
        
        # Set custom margins
        fig.subplots_adjust(left=0.125, right=0.9, bottom=0.11, top=0.88)

    else:
        pass
    
    #scrape for aobs
    
    aurl = aobs_url
    try:        
        # Send a GET request to the website and store the response in a variable
        ahtml = requests.get(aurl)

        # Parse the HTML content of the website using BeautifulSoup
        asoup = BeautifulSoup(ahtml.content, 'html.parser')

        # Find the current temperature, wind direction, and wind speed
        atemp = asoup.find('p', class_='myforecast-current-lrg').text
        atemp = atemp[:-1]

        awind = asoup.find(id='current_conditions_detail')('td')[3]
        awind = awind.string
        
    except Exception as e:
        print("Scrape PWM data", e)
        pass
   
    #scrape for bobs
    
    burl = bobs_url
    try:        
        # Send a GET request to the website and store the response in a variable
        bhtml = requests.get(burl)

        # Parse the HTML content of the website using BeautifulSoup
        bsoup = BeautifulSoup(bhtml.content, 'html.parser')

        # Find the current temperature, wind direction, and wind speed
        btemp = bsoup.find('p', class_='myforecast-current-lrg').text
        btemp = btemp[:-1]

        bwind = bsoup.find(id='current_conditions_detail')('td')[3]
        bwind = bwind.string
        
    except Exception as e:
        print("Scrape MWN data", e)        
        pass
    
    # scrape for cobs
  
    curl = cobs_url
    try:        
        
        # Send a GET request to the website and store the response in a variable
        chtml = requests.get(curl)

        # Parse the HTML content of the website using BeautifulSoup
        csoup = BeautifulSoup(chtml.content, 'html.parser')

        # Find the current temperature, wind direction, and wind speed
        ctemp = csoup.find('p', class_='myforecast-current-lrg').text
        ctemp = ctemp[:-1]

        cwind = csoup.find(id='current_conditions_detail')('td')[3]
        cwind = cwind.string
                      
    except Exception as e:
        print("Scrape buoy data", e)
        pass   
    
    # Get time stamp
    now = datetime.now() # current date and time
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time_str = now.strftime("%H:%M:%S")
    hourmin_str = now.strftime("%H:%M")
    hms = now.strftime("%H:%M:%S")
    day = now.strftime("%A")
           
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time = pd.to_datetime(date_time) #allows us to label x-axis

    now = datetime.now() # current date and time
    time_delta = dt.timedelta(minutes=4200)
    start_time = now - time_delta

    #sec = now.strftime("%S")
    
    # Set axis limits and labels
    ax.set_xlim(start_time, now)
    
    dtext=date_time
    #Build xs and ys arrays
       
    xs.append(date_time)
    ys.append(inHg)
    
    #Limit x and y lists to 20 items
    xs = xs[-4200:] #Adjust this neg number to how many obs plotted in one window
    ys = ys[-4200:] #At a rate of 1 plot/min for 24 hours change this to 1440
    #Draw x and y lists

    ax.clear() 
    ax.plot(xs, ys, 'r-')
    
    ax.text(0, 1.09, "The",
        transform=ax.transAxes,
        fontweight='bold', horizontalalignment='left', fontsize=12)
    
    ax.text(0, 1.05, "Weather",
        transform=ax.transAxes,
        fontweight='bold', horizontalalignment='left', fontsize=12)
 
    ax.text(0, 1.01, "Observer",
        transform=ax.transAxes,
        fontweight='bold', horizontalalignment='left', fontsize=12)
    
    ax.text(.11, 1.01, f'Last Updated\n{now.strftime("%A")}\n{now.strftime("%I:%M %P")}', 
        transform=ax.transAxes,
        fontweight='light', fontstyle='italic', horizontalalignment='left', fontsize=7)  
    
    try:
        ax.text(.80, 1.09, aobs_town,
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
    
        ax.text(.80, 1.05, atemp,
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
 
        ax.text(.80, 1.01, awind,
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
    
    except Exception as e:
        print("2nd aobs error:", e)
        pass
    
    try:
        
        ax.text(.50, 1.09, bobs_town,
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
    
        ax.text(.50, 1.05, btemp,
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
 
        ax.text(.50, 1.01, bwind,
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
        
    except Exception as e:
        print("2nd bobs error:", e)
        pass

    try:
        ax.text(.20, 1.09, cobs_town,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
        ax.text(.20, 1.05, ctemp,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
        ax.text(.20, 1.01, cwind,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
    except Exception as e:
        print("2nd cobs error:", e)
        pass
 
    #set up background colors
    gold = 30.75
    yellow = 30.35
    white = 30.00
    gainsboro = 29.65
    darkgrey = 29.25
        
    ax.axhline(gold, color='gold', lw=77, alpha=.5)
    ax.axhline(yellow, color='yellow', lw=46, alpha=.2)
    ax.axhline(white, color='white', lw=40, alpha=.2)
    ax.axhline(gainsboro, color='gainsboro', lw=46, alpha=.5)    
    ax.axhline(darkgrey, color='darkgrey', lw=77, alpha=.5)
    
    #Lines on minor ticks
    for t in np.arange(29, 31, 0.05):
        ax.axhline(t, color='black', lw=.5, alpha=.2)
    for u in np.arange(29, 31, 0.25):
        ax.axhline(u, color='black', lw=.7)
        
    ax.tick_params(axis='x', direction='inout', length=5, width=1, color='black')
    
    ax.set_ylim(29, 31)
    
    ax.plot(xs, ys, 'r-')
    plt.grid(True, color='.01',) #Draws default horiz and vert grid lines
    plt.ylabel("Inches of Mercury")
    #plt.title("Barometric Pressure")
      
    ax.yaxis.set_minor_locator(AutoMinorLocator(5)) #Puts small ticks between labeled ticks
    ax.yaxis.set_major_formatter(FormatStrFormatter('%2.2f'))
    # disable removing overlapping locations
    ax.xaxis.remove_overlapping_locs = False
    print(i)
    
    ax.xaxis.set(
    major_locator=mdates.HourLocator((0,4,8,12,16,20)),
    major_formatter=mdates.DateFormatter('%-I%P'),
    minor_locator=mdates.DayLocator(),
    minor_formatter=mdates.DateFormatter("\n%a,%-m/%-d"),
)
    ax.set_xlim(dt.datetime.now() - dt.timedelta(minutes=4200), dt.datetime.now())
    #this line seems responsible for vertical lines
    ax.grid(which='major', axis='both', linestyle='-', linewidth=1, color='black', alpha=1, zorder=10)
    plt.show(block=False)

try:
    
    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=3000, save_count=len(xs))
    ani.save('animation.gif', writer='pillow')
except AttributeError:
    pass
except IndexError:
    pass    