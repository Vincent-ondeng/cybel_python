# Random number guessing game
import csv
import os
import requests
import time
ORS_API_KEY = '5b3ce3597851110001cf62483cb7c76cea2c44aa8a5587b797124b51'

def get_driving_distance(source_coordinates, dest_coordinates):
    parameters = {
    'api_key': ORS_API_KEY,
    'start' : '{},{}'.format(source_coordinates[1], source_coordinates[0]),
    'end' : '{},{}'.format(dest_coordinates[1], dest_coordinates[0])
    }

    response = requests.get(
        'https://api.openrouteservice.org/v2/directions/driving-car', params=parameters)

    if response.status_code == 200:
        data = response.json()
        summary = data['features'][0]['properties']['summary']
        distance = summary['distance']
        return distance/1000
    else:
        print('Request failed.')
        return -9999

san_francisco = (37.7749, -122.4194)

destination_cities = {
    'Los Angeles': (34.0522, -118.2437),
    'Boston': (42.3601, -71.0589),
    'Atlanta': (33.7490, -84.3880)

}
for city in destination_cities.items():
        driving_distance = get_driving_distance(san_francisco, destination_cities)
        print ('The driving distance between', city,'and San fransisco', 'km')
        time.sleep(2)