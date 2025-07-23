from helper_functions import  stack_bands_clipped,search_sentinel2_scene, log_failed_scene
import os
import argparse



from config import (
    STAC_API,
    BBOX,
    DATE_RANGE,
    CLOUD_FILTER,
    BANDS,
    OUT_DIR,
    AOI_PATH,
    NUMBER_OF_IMG_DOWNLOAD
)


os.makedirs(OUT_DIR, exist_ok=True)


# -----------------------
# -----------------------
# Main process
# -----------------------
def main(max_items):
    print("🔎 Searching Sentinel-2 scenes...")

    try:
        items = search_sentinel2_scene(
            stac_api=STAC_API,
            bbox=BBOX,
            date_range=DATE_RANGE,
            cloud_filter=CLOUD_FILTER,
            max_items=max_items
        )
    except Exception as e:
        print(f"❌ Search failed: {e}")
        log_failed_scene("SearchFailed", e)
        return

    if not items:
        print("❌ No scenes found.")
        return


    for idx, item in enumerate(items, start=1):
        scene_name = item.id
        print(f"\n🚀 Processing scene {idx}/{len(items)}: {scene_name}")

        output_file = os.path.join(
            OUT_DIR, f"{scene_name}_stack_clipped_epsg32614_30m.tif"
        )

        try:
            success = stack_bands_clipped(item, BANDS, output_file, AOI_PATH)
            if not success:
                raise Exception("Stacking failed internally.")
        except Exception as e:
            print(f"⚠️ Failed to process {scene_name}: {e}")
            log_failed_scene(scene_name, e)

# -----------------------
# CLI Entry Point
# -----------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and process Sentinel-2 images.")
    parser.add_argument(
        '--max_items',
        type=int,
        default=NUMBER_OF_IMG_DOWNLOAD,
        help='Number of scenes to download and process (default: 1)'
    )
    args = parser.parse_args()  # ← ✅ Correct for CLI usage
    main(args.max_items)