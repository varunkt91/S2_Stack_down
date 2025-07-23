# S2_Stack_down

# Sentinel-2 Image Downloader and Processor

This script automates the search, download, and band stacking of Sentinel-2 imagery using STAC API. It clips the imagery to a defined Area of Interest (AOI) and saves the processed files locally.

## 📁 Project Structure

├── main_script.py # The script documented here
├── config.py # Configuration constants
├── helper_functions.py # Utility functions for search, stacking, and logging
├── aoi.geojson # AOI file (if referenced in config)
└── output/ # Output directory for stacked TIFFs

## ⚙️ Configuration (`config.py`)

Ensure the following variables are defined in your `config.py`:

- `STAC_API`: URL of the STAC API endpoint (e.g., `https://earth-search.aws.element84.com/v1`)
- `BBOX`: Bounding box for the search query `[minLon, minLat, maxLon, maxLat]`
- `DATE_RANGE`: Date range as a tuple, e.g., `("2023-01-01", "2023-12-31")`
- `CLOUD_FILTER`: Maximum cloud coverage (e.g., `10`)
- `BANDS`: List of band names to include (e.g., `["B04", "B03", "B02"]`)
- `OUT_DIR`: Output folder for saving the processed TIFFs
- `AOI_PATH`: File path to your AOI GeoJSON or shapefile
- `NUMBER_OF_IMG_DOWNLOAD`: Default number of scenes to process if not specified in CLI

---

## 🛠️ Functions

The script uses helper functions imported from `helper_functions.py`:

- `search_sentinel2_scene(...)`: Queries the STAC API and returns matching scenes.
- 
- `stack_bands_clipped (item, band_keys, output_path, aoi_path, dst_crs="EPSG:32614", dst_res=30)`: Downloads, stacks, and clips the specified bands from a scene.
- `log_failed_scene(scene_name, error)`: Logs failure messages.
-  load_aoi_geometry(aoi_path, target_crs): Use to load aoi and perform reprojection.
-  read_reproject_clip (asset_href, dst_crs, dst_res, clip_geom): Open image bands, reproject, resample, and clip to the AOI.
-  log_failed_scene (scene_name, error, log_path=None): maintains log file in case something is broken
---

## 🚀 How to run

1. ## 🚀 How to Run

1. **Open your terminal or Anaconda Prompt** and navigate to the project folder  
   (this folder should contain all `.py` files and the `environment.yml` file):
   ```bash
   cd path/to/your/project
   
2. Create the Conda environment using the YAML file:
   ```bash
   - cd path/to/your/yml/file
   - conda env create -f environment.yml

4. Activate the environment (the environment is named S2_download):
   ```bash
     conda activate S2_download
   
5. (Optional): Update the input variables in the config.py file if needed. By default, they are configured based on the take-home assignment requirements.
   
7. Run the script to download the latest available Sentinel-2 image:
   ```bash
   conda run -n S2_download python main.py --max_items 1

