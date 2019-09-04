# PoC program to take command line arguments and output
# various information about the ISS.
#
# Interpreter: Python 3.7.3
# None-native Dependencies: requests
#
# Author: Walter Hernandez
#
# Usage: iss_poc ['loc', 'people', 'pass'] [latitude: float] [longitude: float]
#

import requests
import sys
from datetime import datetime


# formats coordinates in a more friendly way
def process_coord(latitude, longitude):
    # format direction
    lat_dir = 'N' if latitude > 0 else 'S'
    lon_dir = 'W' if longitude > 0 else 'E'
    
    return [abs(latitude), lat_dir, abs(longitude), lon_dir]
        

# API endpoints
uris = {
        'loc': 'http://api.open-notify.org/iss-now.json',
        'pass': 'http://api.open-notify.org/iss-pass.json',
        'people': 'http://api.open-notify.org/astros.json'
        }

# check for initial console arg
try:
    action = sys.argv[1]
except IndexError:
    sys.exit('Error: missing argument, should be "loc", "pass", or "people"')

# validate console arg
if action not in ['loc', 'pass', 'people']:
    sys.exit('Error: argument should be "loc", "pass", or "people"')
    
# set uri
uri = uris[action]

# validate 'pass' command
if action == 'pass':
    try:
        latitude, longitude = sys.argv[2], sys.argv[3]
    except IndexError:
        error = 'Error: "pass" requires a latitude and longitude as arguments, both as decimals.\n'
        error += '\te.g: ' + sys.argv[0] + ' pass 35.2271 80.8431'

        sys.exit(error)
        
    try:
        latitude, longitude = float(latitude), float(longitude)
    except ValueError:
        error = 'Error: "pass" requires a latitude and longitude to be a number or decimal.\n'
        error += '\te.g: ' + sys.argv[0] + ' pass 35.2271 80.8431'

        sys.exit(error)
        
    # make sure latitude and longitude is [-90,90] and [-180,180], respectively
    if latitude < -90 or latitude > 90:
        sys.exit('Error: latitude needs to be between -90 and 90, inclusive.')
        
    if longitude < -180 or longitude > 180:
        sys.exit('Error: longitude needs to be between -180 and 180, inclusive.')
    
    # add query params
    uri += '?lat=' + str(latitude) + '&lon=' +  str(longitude)
    
try:
    # hit endpoint
    response = requests.get(uri)

    # throw errors, if any
    response.raise_for_status()

except Exception as err:
    print(f'Error occurred: {err}')
else:
    payload = response.json()  # deserialize payload
    
    if action == 'loc':
        # grab data
        latitude = float(payload['iss_position']['latitude'])
        longitude = float(payload['iss_position']['longitude'])
        
        print('The ISS current location is at {} {}, {} {} '.format(*process_coord(latitude, longitude)))
    elif action == 'pass':
        output = 'The ISS will be overhead {} {}, {} {} '.format(*process_coord(latitude, longitude))
        
        # turn overhead time to datetime and format it nicely
        overhead_time = datetime.utcfromtimestamp(payload['response'][0]['risetime'])
        overhead_time = overhead_time.strftime("%b %d %Y %H:%M:%S")
        
        # seconds over location
        duration = payload['response'][0]['duration']
        
        output += 'on {} for {} seconds'.format(overhead_time, duration)
        
        print(output)
    else:   # 'people'
        craft_people = {}  # dict mapping spacecrafts to people {'craft': ['name', ...]}
        
		# map people to craft
        for person in payload['people']:
            craft = person['craft']
            
            if craft not in craft_people:
                craft_people[craft] = []
                
            craft_people[craft].append(person['name'])
         
		# print results
        for craft in craft_people:
            print('\nThe {} is housing the following astronauts:'.format(craft))
            for person in craft_people[craft]:
                print ('\t' + person)
                