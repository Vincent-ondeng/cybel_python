import math
from math import cos, atan, atan2, sin, sqrt
from dataclasses import dataclass
from typing import Optional


def minutes_to_degrees(minutes: float) -> float:
    return minutes * (1.0 / 60.0)
    pass


def seconds_to_degrees(seconds: float) -> float:
    return seconds * (1.0 / 3600.0)
    pass


@dataclass
class LatLongCoordinate:
    degrees: float = 0
    minutes: float = 0
    seconds: float = 0

    def to_degrees(self):
        working_degrees = math.fabs(self.degrees)
        r = working_degrees + minutes_to_degrees(self.minutes) + seconds_to_degrees(self.seconds)
        if self.degrees < 0:
            r = -r
            pass
        return r

    def to_radians(self):
        """Converts this Coordinate to its Radian unit equivalent
        """
        full_degrees = self.to_degrees()
        return full_degrees * (22.0 / 7.0) / 180.0


def converges(old_geodetic_latitude, new_geodetic_latitude):
    if old_geodetic_latitude == new_geodetic_latitude:
        return True
    return False


def geodetic_coordinates_to_xyz(lat, long, height):
    # a = 6371.0  # Kilometres
    # a *= 1000  # metres
    a = 6_378_137  # metres

    f = 1 / 298.25722101
    b = a * (1 - f)

    first_eccentricity = (a ** 2 - b ** 2) / a ** 2  # e squared
    R_knot_n = a / (sqrt(1 - first_eccentricity * (sin(lat) ** 2)))

    x = (R_knot_n + height) * cos(lat) * cos(long)
    y = (R_knot_n + height) * cos(lat) * sin(long)
    z = ((1.0 - first_eccentricity) * R_knot_n + height) * sin(lat)

    print(f'P({x}, {y}, {z})')
    pass


help_shown: bool = False
mode: int = 0  # 0 - dms, Any other value - absolute degree


def input_coordinate(prompt='') -> LatLongCoordinate:
    global mode
    if mode == 0:
        return input_coordinate_dms(prompt)
    return input_coordinate_absolute_degrees(prompt)
    pass


def input_coordinate_dms(prompt: str = '') -> LatLongCoordinate:
    global help_shown

    def info(message, end='\n'):
        print(f'[INFO]: {message}', end=end)
        pass

    help_message = ''
    if not help_shown:
        help_message = """Help on DMS Input:
    To input the DMS latitude or longitude of a place, separate the Degrees, Minutes, Seconds and direction 
    with a space. 
    For example, Nairobi in Kenya, is at latitude, 1° 17' 31.4376'' S, thus the format to input the
    latitude is: 
    >>> 1 17 31.4376 S
    \n"""
        help_shown = True

    dms_in = input(help_message + f"{prompt}")

    lat_or_long = dms_in.split()

    degrees: float = 0
    minutes: float = 0
    seconds: float = 0
    direction: Optional[str] = None

    if len(lat_or_long) > 0:
        degrees = float(lat_or_long[0])
    if len(lat_or_long) > 1:
        minutes = float(lat_or_long[1])
    if len(lat_or_long) > 2:
        seconds = float(lat_or_long[2])
    if len(lat_or_long) > 3:
        direction = lat_or_long[3]

    if degrees < 0:
        pass
    else:
        if direction is None:
            info('The input DMS coordinate did not have a direction, assuming Northern Latitude or Eastern '
                 'Longitude.')
        else:
            if direction.upper() == 'N':
                pass
            if direction.upper() == 'S':
                degrees = -degrees
                pass
            if direction.upper() == 'E':
                pass
            if direction.upper() == 'W':
                degrees = -degrees
                pass

    r = LatLongCoordinate(degrees, minutes, seconds)
    # print(r)
    # print(r.to_degrees())
    return r
    pass


def input_coordinate_absolute_degrees(prompt: str = '') -> LatLongCoordinate:
    global help_shown
    help_message = """Help on absolute degree input:
    To input the latitude or longitude of a place, convert the Minutes and Seconds to degrees, 
    and sum to the degrees; then the direction determines whether the summed Degrees are negative or positive. 
    For example, Nairobi in Kenya, is at latitude, 1° 17' 31.4376'' S; 
    this translates to an accumulated Degrees of -1.292066; thus the format to input the latitude is: 
    >>> -1.292066"""

    if not help_shown:
        print(help_message, end='\n\n')
        help_shown = True
    degrees = float(input(prompt))

    return LatLongCoordinate(degrees)
    pass


def main():
    global debug_mode  # TODO End Debug Mode

    # Geographical Coordinates of Nairobi, Kenya
    pos_deg_latitude = -1.286389
    pos_deg_longitude = 36.817223

    if not debug_mode:
        pos_deg_latitude = input_coordinate(
            "Enter the latitude of the position on Earth.\n>>> ").to_degrees()
        pos_deg_longitude = input_coordinate(
            "Enter the longitude of the position on Earth.\n>>> ").to_degrees()

    print()
    print(f'Calculating the Geodetic coordinates of Latitude-Longitude Point:\n'
          f'\tP({pos_deg_latitude}, {pos_deg_longitude}) >> Units: Degrees')

    # Convert latitude and longitude of the given position to radians
    pos_deg_latitude = LatLongCoordinate(pos_deg_latitude).to_radians()
    pos_deg_longitude = LatLongCoordinate(pos_deg_longitude).to_radians()

    print(f'\tP({pos_deg_latitude}, {pos_deg_longitude}) >> Units: Radians')

    # a = 6371.0  # Kilometres
    # a *= 1000  # metres
    a = 6_378_137  # metres

    f = 1 / 298.25722101
    b = a * (1 - f)

    x = a * cos(pos_deg_latitude) * cos(pos_deg_longitude)
    y = a * cos(pos_deg_latitude) * sin(pos_deg_longitude)
    z = a * sin(pos_deg_latitude)
    print(f'\nECEF xyz coordinate of the Point, P(x, y, z) -> \n\t P({x}, {y}, {z}) >> Units: metres')
    print()

    assert (a / b) == 1 / (1 - f)

    geodetic_longitude_lambda = atan2(y, x)

    # r = sqrt(x ** 2 + y ** 2 + z ** 2)
    p = sqrt(x ** 2 + y ** 2)

    geocentric_latitude = atan2(p, z)

    geodetic_latitude_now = geocentric_latitude
    geodetic_latitude: float  # = None

    iteration: int = 0
    while True:
        first_eccentricity = (a ** 2 - b ** 2) / a ** 2  # e squared
        R_knot_n = a / (sqrt(1 - first_eccentricity * (sin(geodetic_latitude_now) ** 2)))
        h = (p / cos(geodetic_latitude_now)) - (R_knot_n * geodetic_latitude_now)

        geodetic_latitude_next = atan((z / p) * (1 - first_eccentricity * (R_knot_n / (R_knot_n + h))) ** -1)
        print(f'Iteration: {iteration}')
        print(f'\tcurrent geodetic latitude: {geodetic_latitude_now} \n\t'
              f'estimated geodetic latitude: {geodetic_latitude_next}')
        iteration += 1
        if converges(geodetic_latitude_now, geodetic_latitude_next):
            geodetic_latitude = geodetic_latitude_next
            break

        geodetic_latitude_now = geodetic_latitude_next

    print()
    print('----------------------------------------------------------')
    print('----------------GEODETIC COORDINATES----------------------')
    print('----------------------------------------------------------')

    print(f'geodetic longitude (\u03BB): {geodetic_longitude_lambda} radians')
    print(f'geodetic latitude (\u03C9): {geodetic_latitude} radians')

    h = (p / cos(geodetic_latitude)) - R_knot_n

    print(f'geodetic height: {h} metres')

    # print(f'\n\nReverse:\n\t', end='')
    # geodetic_coordinates_to_xyz(geodetic_latitude, geodetic_longitude_lambda, h)
    pass


debug_mode = False
if __name__ == '__main__':
    main()
    pass

