import geopandas as gpd
import pandas as pd
import numpy as np
import time
import ee  # Import Google Earth Engine
from tqdm import tqdm  # Progress bar
from api_key import config

#Authentication
ee.Authenticate()
# Initialize Google Earth Engine
ee.Initialize(project='ee-asr66')

# 🔹 Read Monte Carlo Sample Locations
mcs_file = "monte_carlo_samples.geojson"
gdf = gpd.read_file(mcs_file)

# 🔹 Define Landsat Data Parameters
start_date = "2016-01-01"  # Landsat-8/9 earliest availability
end_date = "2024-02-25"  # Current date

# 🔹 Create Data Storage
results = []

# 🔹 Loop Over Each Sample Location
for index, row in tqdm(gdf.iterrows(), total=len(gdf)):
    if index < 10:
        lat, lon = row.geometry.y, row.geometry.x  # Extract lat/lon

        # Define a point and buffer for the area of interest
        point = ee.Geometry.Point(lon, lat)
        buffer = point.buffer(500)  # 500m buffer

        # Create a function to calculate NDVI, Snow Coverage, and LST
        def add_indices(image):
            ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
            ndsi = image.normalizedDifference(['SR_B3', 'SR_B6']).rename('NDSI')
            lst = image.select('ST_B10').multiply(0.00341802).add(149.0).subtract(273.15).rename('LST')  # Convert to Celsius
            return image.addBands(ndvi)#.addBands(ndsi).addBands(lst)

        # Fetch Landsat data
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')  \
            .filterBounds(buffer) \
            .filterDate(start_date, end_date) \
            .map(add_indices)

        # Get the data and extract values
        try:
            image_list = collection.toList(collection.size())
            for i in range(image_list.size().getInfo()):
                image = ee.Image(image_list.get(i))

                # Get image properties
                timestamp = image.get('system:time_start').getInfo()
                ndvi_mean = image.select('NDVI').reduceRegion(ee.Reducer.mean(), buffer).get('NDVI').getInfo()
                snow_coverage_mean = image.select('NDSI').reduceRegion(ee.Reducer.mean(), buffer).get('NDSI').getInfo()
                lst_mean = image.select('LST').reduceRegion(ee.Reducer.mean(), buffer).get('LST').getInfo()

                # Append results with time information
                results.append({
                    "latitude": lat,
                    "longitude": lon,
                    "timestamp": timestamp,  # Timestamp from image
                    "NDVI": ndvi_mean,
                    "snow_coverage": snow_coverage_mean,
                    "LST": lst_mean,
                })
        except Exception as e:
            print(f" Error retrieving data for {lat}, {lon}: {e}")

        time.sleep(0.5)  # Avoid hitting API rate limits

# 🔹 Convert Results to DataFrame
df = pd.DataFrame(results)

# 🔹 Save Data
df.to_csv("landsat_data_full.csv", index=False)  # CSV format
df.to_parquet("landsat_data_full.parquet")  # Parquet format (faster for large data)

print("✅ Data collection complete! Saved as CSV & Parquet.")
