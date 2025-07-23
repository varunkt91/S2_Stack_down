import os
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
import fiona
import pyproj
from shapely.geometry import shape, mapping
from shapely.ops import transform as shapely_transform
from rasterio.shutil import copy as rio_copy
import tempfile
from pystac_client import Client
import csv
import numpy as np
from datetime import datetime


# function to search for S2 data
def search_sentinel2_scene(
    stac_api,
    bbox,
    date_range,
    cloud_filter=None,
    max_items=None,
    collection="sentinel-2-l2a"
):
    """
    Search Sentinel-2 L2A scenes using STAC API.

    Parameters:
        stac_api (str): STAC API URL
        bbox (list): Bounding box [minx, miny, maxx, maxy]
        date_range (str): Date range (e.g., "2023-01-01/2025-12-31")
        cloud_filter (int): Maximum allowable cloud cover %
        max_items (int): Max number of items to return
        collection (str): STAC collection to search

    Returns:
        list of pystac.Item: Matching STAC items
    """
    print("🔍 Connecting to STAC API and searching for Sentinel-2 scenes...")
    client = Client.open(stac_api)

    search = client.search(
        collections=[collection],
        bbox=bbox,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": cloud_filter}},
        sortby=[{"field": "properties.datetime", "direction": "desc"}],
        max_items=max_items
    )

    items = list(search.get_items())
    if not items:
        raise Exception("❌ No matching Sentinel-2 scenes found.")
    
    print(f"✅ Found {len(items)} scene(s). Most recent: {items[0].id}")
    return items

# function to load and reproject aoi for clipping

def load_aoi_geometry(aoi_path, target_crs):
    """Load AOI from GeoJSON and reproject it to the target CRS."""
    with fiona.open(aoi_path, 'r') as src:
        aoi_geom = [feature["geometry"] for feature in src]
        aoi_crs = src.crs
        if aoi_crs != target_crs:
            print("🔁 Reprojecting AOI to match image CRS...")
            project = pyproj.Transformer.from_crs(aoi_crs, target_crs, always_xy=True).transform
            aoi_geom = [mapping(shapely_transform(project, shape(geom))) for geom in aoi_geom]
    return aoi_geom


# function to read cog from aws api using stac and resmaple reproject and perfrom clipping
def read_reproject_clip(asset_href, dst_crs, dst_res, clip_geom):
    """Reproject, resample, and clip a single band raster to an AOI."""
    with rasterio.open(asset_href) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds, resolution=dst_res
        )

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        dst_array = np.empty((height, width), dtype=src.meta['dtype'])

        reproject(
            source=rasterio.band(src, 1),
            destination=dst_array,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )

        # Clip to AOI
        temp_meta = kwargs.copy()
        temp_meta.update(count=1)
        with rasterio.io.MemoryFile() as memfile:
            with memfile.open(**temp_meta) as tmp:
                tmp.write(dst_array, 1)
                clipped, clipped_transform = mask(tmp, clip_geom, crop=True)

        clipped_meta = temp_meta.copy()
        clipped_meta.update({
            'height': clipped.shape[1],
            'width': clipped.shape[2],
            'transform': clipped_transform
        })

        return clipped[0], clipped_meta



def stack_bands_clipped(item, band_keys, output_path, aoi_path, dst_crs="EPSG:32614", dst_res=30):
    """Stack and clip bands from Sentinel-2 scene, save final Cloud-Optimized GeoTIFF."""
    try:
        sample_asset = item.assets[band_keys[0]]
        image_crs = rasterio.open(sample_asset.href).crs

        # Load and reproject AOI
        clip_geom = load_aoi_geometry(aoi_path, image_crs)

        stacked_arrays = []
        out_meta = None

        for band_key in band_keys:
            try:
                print(f"🔄 Processing {band_key}")
                asset_href = item.assets[band_key].href
                array, meta = read_reproject_clip(asset_href, dst_crs, dst_res, clip_geom)
                stacked_arrays.append(array)
                if out_meta is None:
                    out_meta = meta
            except Exception as e:
                print(f"❌ Error processing band {band_key}: {e}")
                raise  # Skip entire scene if any band fails

        # Update metadata for multiband
        out_meta.update({
            'count': len(stacked_arrays),
            'driver': 'GTiff',
            'tiled': True,
            'blockxsize': 512,
            'blockysize': 512,
            'compress': 'deflate'
        })

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tmpfile:
            tmp_path = tmpfile.name

        try:
            with rasterio.open(tmp_path, 'w', **out_meta) as tmp_dst:
                for i, band in enumerate(stacked_arrays, start=1):
                    tmp_dst.write(band, i)

            rio_copy(
                tmp_path,
                output_path,
                driver='COG',
                compress='deflate',
                blocksize=512,
                overview_resampling=Resampling.bilinear,
                tiled=True,
                overview_level='AUTO'
            )

            print(f"✅ Final COG saved at: {output_path}")

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        return True  # Success

    except Exception as e:
        print(f"❌ Failed to process scene {item.id}: {e}")
        return False  # Failure


# -----------------------
# Logging failed scenes
# -----------------------
def log_failed_scene(scene_name, error, log_path=None):
    if log_path is None:
        log_path = "log_failed_scenes.txt"
    with open(log_path, 'a') as f:
        f.write(f"{scene_name} failed with error: {str(error)}\n")

# -----------------------
