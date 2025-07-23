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
- `stack_bands_clipped (item, band_keys, output_path, aoi_path, dst_crs="EPSG:32614", dst_res=30)`: Downloads, stacks, and clips the specified bands from a scene.
- `log_failed_scene(scene_name, error)`: Logs failure messages.
-  load_aoi_geometry(aoi_path, target_crs): Use to load aoi and perform reprojection.
-  read_reproject_clip (asset_href, dst_crs, dst_res, clip_geom): Open image bands, reproject, resample, and clip to the AOI.
-  log_failed_scene (scene_name, error, log_path=None): maintains log file in case something is broken
---

## 🚀 How to run

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
   
7. Run the script to download the latest available Sentinel-2 image (max_items is set to 1 because we want to download the latest image):
   ```bash
   conda run -n S2_download python main.py --max_items 1

<h2>🚀 Overall Workflow</h2>

<p>
  The process for downloading and preparing Sentinel-2 imagery follows these key steps:
</p>

<ol>
  <li>Query the STAC API to retrieve available Sentinel-2 scenes.</li>
  <li>Reproject each image band to the target coordinate reference system (CRS).</li>
  <li>Resample the bands to a consistent spatial resolution.</li>
  <li>Clip each band to the area of interest (AOI).</li>
  <li>Stack the clipped bands into a single multi-band image.</li>
  <li>Save the final stacked image as a Cloud-Optimized GeoTIFF (COG).</li>
</ol>

<h2>🚀 Future Improvements</h2>

<ol>
  <li>Implement an automated routine to query the STAC API and download new Sentinel-2 images daily at a scheduled time whenever new data is available.</li>
  <li>Incorporate cloud masking using the QA60 band and cloud probability band to better remove clouds from imagery.</li>
  <li>Optimize the script to reduce processing time and improve efficiency.</li>
  <li>Add robust exception handling with logging to capture and manage errors effectively.</li>
  <li>Extend functionality to handle multiple areas of interest (AOIs) for batch downloading and preprocessing of data.</li>
</ol>
   
