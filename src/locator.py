import requests
from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timezone
from config import LATITUDE, LONGITUDE


class Locator:
    """Locator class to determine the geographical location and solar direction based on the public
    IP address of the machine.
    Attributes:
        lat (float): Default latitude, defaults to LATITUDE from config.
        long (float): Default longitude, defaults to LONGITUDE from config.
    """

    def __init__(self, lat: float = LATITUDE, long: float = LONGITUDE):
        """Initialize the Locator with a default latitude and longitude.
        Args:
            latitude (float): Default latitude.
            longitude (float): Default longitude.
        """
        self.lat = lat or LATITUDE
        self.long = long or LONGITUDE

    def get_ip(self) -> str:
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

    def get_location(self) -> tuple[float, float]:
        """Retrieve the geographical location (latitude and longitude) based on the public IP
        address.
        Returns:
            tuple[float, float]: A tuple containing latitude and longitude, or manually configured
            IP address if an error occurs, such as an absense of internet connection.
        """
        ip: str = self.get_ip()
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
                return self.lat, self.long
        except requests.RequestException as e:
            print(f'Error fetching location: {e}')
            return self.lat, self.long

    def get_solar_direction(self, date: datetime = None) -> tuple[float, float]:
        """Calculate the solar altitude and azimuth based on the current date and time.
        Args:
            date (datetime): The date and time for which to calculate the solar position.
        Returns:
            tuple[float, float]: A tuple containing solar altitude and azimuth.
        """
        date = date or datetime.now(timezone.utc)
        lat, lon = self.get_location()
        altitude: float = get_altitude(lat, lon, date)
        azimuth: float = get_azimuth(lat, lon, date)
        return altitude, azimuth
