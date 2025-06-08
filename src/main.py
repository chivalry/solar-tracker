from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timezone
import requests
from gpiozero import Servo
import json
from config import LATITUDE, LONGITUDE, AZIMUTH, ALTITUDE

LAT = 33.8042367
LONG = -116.9791774


def get_ip() -> str:
    """Retrieve the public IP address of the machine.
    Returns:
        str: The public IP address as a string, or None if an error occurs.
    """
    try:
        response: requests.Response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return response.json()['ip']
    except requests.RequestException as e:
        print(f'Error fetching IP: {e}')
        return None


def get_location() -> tuple[float, float]:
    """Retrieve the geographical location (latitude and longitude) based on the public IP
    address.
    Returns:
        tuple[float, float]: A tuple containing latitude and longitude, or manually configured
        IP address if an error occurs, such as an absense of internet connection.
    """
    ip: str = get_ip()
    if not ip:
        return None
    try:
        response: requests.Response = requests.get(f'https://ipinfo.io/{ip}/json')
        response.raise_for_status()
        data: dict[str, str] = response.json()
        loc: str = data.get('loc', '')
        if loc:
            lat, lon = map(float, loc.split(','))
            return lat, lon
        else:
            print('Location not found in response.')
            return None
    except requests.RequestException as e:
        print(f'Error fetching location: {e}')
        return LATITUDE, LONGITUDE


def main():
    date = datetime.now(timezone.utc)
    print(get_altitude(LAT, LONG, date))
    print(get_azimuth(LAT, LONG, date))
    print(AZIMUTH, ALTITUDE)
    location = get_location()
    if location:
        lat, lon = location
        date: datetime = datetime.now(timezone.utc)
        print(f'Latitude: {lat}, Longitude: {lon}')
        print(f'Solar Altitude: {get_altitude(lat, lon, date)}')
        print(f'Solar Azimuth: {get_azimuth(lat, lon, date)}')
    else:
        print('Could not retrieve location.')


if __name__ == '__main__':
    main()
