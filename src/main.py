# /usr/bin/python3
from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timezone
import requests

LAT = 33.8042367
LONG = -116.9791774

date = datetime.now(timezone.utc)
print(get_altitude(LAT, LONG, date))
print(get_azimuth(LAT, LONG, date))


def get_ip() -> str:
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return response.json()['ip']
    except requests.RequestException as e:
        print(f'Error fetching IP: {e}')
        return None


def get_location() -> tuple[float, float]:
    ip = get_ip()
    if not ip:
        return None
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        response.raise_for_status()
        data = response.json()
        loc = data.get('loc', '')
        if loc:
            lat, lon = map(float, loc.split(','))
            return lat, lon
        else:
            print('Location not found in response.')
            return None
    except requests.RequestException as e:
        print(f'Error fetching location: {e}')
        return None


if __name__ == '__main__':
    location = get_location()
    if location:
        lat, lon = location
        date = datetime.now(timezone.utc)
        print(f'Latitude: {lat}, Longitude: {lon}')
        print(f'Solar Altitude: {get_altitude(lat, lon, date)}')
        print(f'Solar Azimuth: {get_azimuth(lat, lon, date)}')
    else:
        print('Could not retrieve location.')
