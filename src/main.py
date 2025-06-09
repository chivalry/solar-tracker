from datetime import datetime, timezone
from gpiozero import Servo
from locator import Locator
from pysolar.solar import get_altitude, get_azimuth


def main():
    locator = Locator()
    alt, az = locator.get_solar_direction()
    print(f'Solar Altitude: {alt}, Solar Azimuth: {az}')
    servo: Servo = Servo(14)
    print('servo: ', servo)


if __name__ == '__main__':
    main()
