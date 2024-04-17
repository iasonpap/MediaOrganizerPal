from utils.gps_utils import get_gps_from_image, get_lat_lon_from_gps

class TestGetGPSFromImage:
    def test_gps_is_not_None_for_images(self):
        import os 
        for file in os.listdir("tests/data"):
            if file.endswith(".jpg"):
                image_path = os.path.join("tests/data", file)
                gps_info = get_gps_from_image(image_path)
                assert gps_info is not None

    def test_lon_lat_exists(self):
        image_path = "tests/data/IMG_20220403_122754.jpg"
        gps_info = get_gps_from_image(image_path)
        assert "Exif.GPSInfo.GPSLatitude" in gps_info
        assert "Exif.GPSInfo.GPSLongitude" in gps_info

    def test_gps_is_None_for_videos(self):
        import os 
        for file in os.listdir("tests/data"):
            if file.endswith(".mp4"):
                video_path = os.path.join("tests/data", file)
                gps_info = get_gps_from_image(video_path)
                assert gps_info is None

    def test_gps_is_not_None_for_panoramas(self):
        import os 
        for file in os.listdir("tests/data"):
            if file.endswith(".jpg") and "PANO" in file:
                panorama_path = os.path.join("tests/data", file)
                gps_info = get_gps_from_image(panorama_path)
                assert gps_info is not None

    def test_gps_is_None_for_bad_path(self):
        bad_path = "tests/data/nonexistent.jpg"
        gps_info = get_gps_from_image(bad_path)
        assert gps_info is None

class TestGetLatLonFromGPS:
    gps_info = {
        "gps_image_1":{
            "Exif.GPSInfo.GPSLatitudeRef": "N",
            "Exif.GPSInfo.GPSLatitude": "47/1 59/1 536568/10000",
            "Exif.GPSInfo.GPSLongitudeRef": "E",
            "Exif.GPSInfo.GPSLongitude": "0/1 11/1 3702/10000",
        },
        "gps_image_2":{
            "Exif.GPSInfo.GPSLatitudeRef": "S",
            "Exif.GPSInfo.GPSLatitude": "35/1 31/1 81653/10000",
            "Exif.GPSInfo.GPSLongitudeRef": "W",
            "Exif.GPSInfo.GPSLongitude": "120/1 55/1 713652/10000",
        },
        "gps_image_3":{
            "Exif.GPSInfo.GPSLatitudeRef": "N",
            "Exif.GPSInfo.GPSLatitude": "41/1 44/1 486751/10000",
            "Exif.GPSInfo.GPSLongitudeRef": "W",
            "Exif.GPSInfo.GPSLongitude": "87/1 16/1 435162/10000",
        },
        "gps_image_4":{
            "Exif.GPSInfo.GPSLatitudeRef": "S",
            "Exif.GPSInfo.GPSLatitude": "25/1 30/1 987654/10000",
            "Exif.GPSInfo.GPSLongitudeRef": "E",
            "Exif.GPSInfo.GPSLongitude": "150/1 45/1 123456/10000",
        },
        "gps_image_5":{
            "Exif.GPSInfo.GPSLatitudeRef": "N",
            "Exif.GPSInfo.GPSLatitude": "37/1 30/1 987654/10000",
            "Exif.GPSInfo.GPSLongitudeRef": "E",
            "Exif.GPSInfo.GPSLongitude": "100/1 45/1 123456/10000",
        },
    }
    def test_lat_lon_is_tuple(self):
        for image_key, gps_info in self.gps_info.items():
            lat_lon = get_lat_lon_from_gps(gps_info)
            assert isinstance(lat_lon, tuple)
    
    def test_lat_lon_is_correct(self):
        lat_lon_decimal_answers = [
            (47.998238, 0.183436),
            (-35.518935, -120.93649),
            (41.746854, -87.278755),
            (-25.527435, 150.753429),
            (37.527435, 100.753429),
        ]
        for i, gps_info in enumerate(self.gps_info.values()):
            lat_lon = get_lat_lon_from_gps(gps_info)
            assert lat_lon == lat_lon_decimal_answers[i]

    def test_lat_lon_is_None_for_bad_gps_info(self):
        bad_gps_info = {
            "Exif.GPSInfo.GPSLatitudeRef": "N",
            "Exif.GPSInfo.GPSLatitude": "invalid",
            "Exif.GPSInfo.GPSLongitudeRef": "E",
            "Exif.GPSInfo.GPSLongitude": "invalid",
        }
        lat_lon = get_lat_lon_from_gps(bad_gps_info)
        assert lat_lon is None
