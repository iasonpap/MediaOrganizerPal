from geopy.geocoders import Nominatim
import pyexiv2
import re

CITIES = {'Le Mans': (48.0073849, 0.1967849),
          'London': (51.5073219, -0.1276474),
          'Truro': (50.2627515, -5.0520467),
          'Athens': (37.9839412, 23.7283052),
          'Etretat': (49.707636, 0.2042726),
          'Paris': (48.8566969, 2.3514616),
          'Marseille': (43.2961743, 5.3699525),
          'Rouen': (49.4404591, 1.0939658),
          }

def get_gps_from_image(image_path):
    """Return the GPS coordinates from an image."""
    gps_info = {}
    with pyexiv2.Image(image_path) as img:
        metadata = img.read_exif()
        # if "Exif.GPSInfo" category is in the metadata
        # extract only the GPSInfo data
        for key in metadata.keys():
            if "Exif.GPSInfo" in key:
                gps_info[key] = metadata[key]
    if gps_info == {}:
        return None
    return gps_info

def get_lat_lon_from_gps(gps_info):
    """Return the latitude and longitude from GPSInfo in decimal degrees."""
    if not gps_info or not isinstance(gps_info, dict):
        return None
    # check if the GPSInfo dictionary has the required keys
    lat_ref = gps_info.get("Exif.GPSInfo.GPSLatitudeRef")
    lon_ref = gps_info.get("Exif.GPSInfo.GPSLongitudeRef")
    # check if the GPSInfo dictionary has the required keys
    lat = gps_info.get("Exif.GPSInfo.GPSLatitude")
    lon = gps_info.get("Exif.GPSInfo.GPSLongitude")

    if lat_ref not in ["N", "S"] or lon_ref not in ["E", "W"]:
        return None
    gps_pattern = r"\d+/\d+ \d+/\d+ \d+/\d+"
    if re.search(gps_pattern, lat) is None \
        or re.search(gps_pattern, lon) is None:
        return None
    # convert the GPS coordinates to decimal degrees
    lat_deg, lat_min, lat_sec = [float(val.split('/')[0]) / float(val.split('/')[1]) for val in lat.split()]
    lon_deg, lon_min, lon_sec = [float(val.split('/')[0]) / float(val.split('/')[1]) for val in lon.split()]

    lat_decimal = lat_deg + lat_min/60 + lat_sec/3600
    lon_decimal = lon_deg + lon_min/60 + lon_sec/3600
    if lat_ref == 'S':
        lat_decimal = -lat_decimal
    if lon_ref == 'W':
        lon_decimal = -lon_decimal

    # round to 6 decimal places
    return round(lat_decimal, 6), round(lon_decimal, 6)
