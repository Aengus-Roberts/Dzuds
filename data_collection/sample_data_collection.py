import geopandas as gpd
import pandas as pd
import time
from rasterio.io import MemoryFile
from sentinelhub import SentinelHubRequest, MimeType, bbox_to_dimensions, BBox, CRS
from tqdm import tqdm  # Progress bar
from api_key import config

# 🔹 Read Monte Carlo Sample Locations
mcs_file = "../data/monte_carlo_samples.geojson"
gdf = gpd.read_file(mcs_file).to_crs(epsg=4326)  # Ensure WGS84 CRS
print(f"Loaded {mcs_file} with CRS: {gdf.crs}")

# 🔹 Define Sentinel Data Parameters
resolution = 1000  # 1 km grid

# Read date windows from file
with open("../data/date_windows.txt", "r") as f:
    dates = [line.strip() for line in f.readlines()]

# Create date intervals
date_windows = [(dates[i], dates[i + 1]) for i in range(len(dates) - 1)]

# Define Evalscript to Fetch Multiple Bands
evalscript_s2 = """
//VERSION=3
function setup() {
    return {
        input: ["B08", "B04", "B11", "B02"],  // NDVI, Snow Cover, Ice Thickness
        output: { bands: 4 }
    };
}
function evaluatePixel(sample) {
    return [
        (sample.B08 - sample.B04) / (sample.B08 + sample.B04),  // NDVI
        sample.B11,  // Snow thickness proxy
        sample.B02,  // Snow coverage
        sample.B04   // Ice thickness proxy
    ];
}
"""

evalscript_s3 = """
//VERSION=3
function setup() {
    return {
        input: ["S8", "S9"],  // Thermal Infrared bands for LST calculation
        output: { bands: 1 }
    };
}
function evaluatePixel(sample) {
    var lst = (sample.S8 + sample.S9) / 2 - 273.15;  // Convert to Celsius
    return [lst];
}
"""

# 🔹 Create Data Storage
results = []
count = 0

# 🔹 Loop Over Each Sample Location and Each Date Window
for index, row in tqdm(gdf.iterrows(), total=len(gdf)):
    if index < 100:
        lat, lon = row.geometry.y, row.geometry.x  # Extract lat/lon
        bbox = BBox(bbox=[lon - 0.005, lat - 0.005, lon + 0.005, lat + 0.005], crs=CRS.WGS84)  # Small bbox per point

        for time_from, time_to in date_windows:
            # Sentinel Hub Request with updated time range
            s2_request = SentinelHubRequest(
                evalscript=evalscript_s2,
                input_data=[{
                    "type": "Sentinel-2-L2A",
                    "dataFilter": {"timeRange": {"from": time_from, "to": time_to}}
                }],
                bbox=bbox,
                size=bbox_to_dimensions(bbox, resolution=resolution),
                config=config,
                responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)]
            )

            s3_request = SentinelHubRequest(
                evalscript=evalscript_s3,
                input_data=[{
                    "type": "Sentinel-3-SLSTR",
                    "dataFilter": {"timeRange": {"from": time_from, "to": time_to}}
                }],
                bbox=bbox,
                size=bbox_to_dimensions(bbox, resolution=resolution),
                config=config,
                responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)]
            )
            print(s3_request.get_data()[0][0][0])
            try:
                # Fetch Sentinel-2 Data
                s2_response = s2_request.get_data()[0][0][0]
                ndvi_mean, snow_thickness_mean, snow_coverage_mean, ice_thickness_mean = map(float, s2_response)

                # Fetch Sentinel-3 Data
                s3_response = s3_request.get_data()[0][0][0]
                land_temp = float(s3_response)  # Sentinel-3 LST

                # Append results with time information
                results.append({
                    "latitude": lat,
                    "longitude": lon,
                    "timestamp": time_from,  # Store actual date window
                    "NDVI": ndvi_mean,
                    "snow_thickness": snow_thickness_mean,
                    "snow_coverage": snow_coverage_mean,
                    "ice_thickness": ice_thickness_mean,
                    "land_temp": land_temp  # Now using Sentinel-3 LST
                })

            except Exception as e:
                print(f"❌ Error retrieving data for {lat}, {lon}: {e}")

            time.sleep(0.1)  # Avoid hitting API rate limits

            if index % 20 == 19:
                df = pd.DataFrame(results)
                df.to_csv("landsat_data_{}.csv".format(count), index=False)  # CSV format
                df.to_parquet("landsat_data_{}.parquet".format(count))  # Parquet format (faster for large data)
                results = []
                count += 1

# 🔹 Convert Results to DataFrame
df = pd.DataFrame(results)

# 🔹 Save Data
df.to_csv("sentinel_data_last.csv", index=False)  # CSV format
df.to_parquet("sentinel_data_last.parquet")  # Parquet format (faster for large data)

print("✅ Data collection complete! Saved as CSV & Parquet.")
