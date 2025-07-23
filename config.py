# config.py

STAC_API = "https://earth-search.aws.element84.com/v1"
BBOX = [-98.23, 41.07, -98.17, 41.13]
DATE_RANGE = "2023-01-01/2025-12-31"
CLOUD_FILTER = 10
BANDS = ["blue", "swir16"]
OUT_DIR = "resampled_reprojected_30m"
AOI_PATH = r"C:\Users\varun\Downloads\t\clip_area.geojson"
LOG_PATH = "failed_scenes_log.csv"
NUMBER_OF_IMG_DOWNLOAD = 1