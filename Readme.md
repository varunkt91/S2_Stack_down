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
- `stack_bands_clipped(item, bands, output_file, aoi_path)`: Downloads, stacks, and clips the specified bands from a scene.
- `log_failed_scene(scene_name, error)`: Logs failure messages.

---

## 🚀 Main Script Flow

1. Creates the output directory (if it doesn't exist).
2. Searches for Sentinel-2 scenes using STAC API and user-defined filters.
3. Iterates over the scenes:
   - Downloads and stacks specified bands.
   - Clips them to the provided AOI.
   - Saves the output as a GeoTIFF.
4. Logs any failed attempts.

---

## 🔧 Command-Line Usage

You can run the script from the command line with the following syntax:

```bash
python main_script.py --max_items 3
