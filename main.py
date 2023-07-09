import requests
from constants import APIKEY

def get_time_zone(country):
    # Geocoding API URL
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={country}&key={APIKEY}'

    # Get latitude and longitude coordinates for the country
    response = requests.get(geocoding_url)
    data = response.json()

    if data['status'] == 'OK':
        result = data['results'][0]
        location = result['geometry']['location']
        lat = location['lat']
        lng = location['lng']

        # Time Zone API URL
        timezone_url = f'https://maps.googleapis.com/maps/api/timezone/json?location={lat},{lng}&timestamp=0&key={APIKEY}'

        # Get time zone information
        response = requests.get(timezone_url)
        data = response.json()

        if data['status'] == 'OK':
            time_zone_id = data['timeZoneId']
            dst_offset = data['dstOffset']
            raw_offset = data['rawOffset']
            return time_zone_id, dst_offset, raw_offset
        else:
            print('Error: Unable to retrieve time zone information.')
    else:
        print('Error: Unable to retrieve geocoding information.')



country = None
while not country:
    country = input("Enter the country you would like to check: ")

    time_zone_id, dst_offset, raw_offset = get_time_zone(country)

    if time_zone_id:
        if dst_offset != 0:
            print(f'Daylight Saving Time is observed in {country} (Time Zone: {time_zone_id}).')

        else:
            print(f'Daylight Saving Time is not observed in {country} (Time Zone: {time_zone_id}).')
    else:
        print('Invalid country. Please try again.')
        country = None


