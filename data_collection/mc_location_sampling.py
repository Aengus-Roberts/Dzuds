import numpy as np
import pandas as pd
import geopandas as gpd

# Define Mongolia bounding box (approximate)
lat_min, lat_max = 41.5, 52.2
lon_min, lon_max = 87.5, 119.9

# Generate random lat/lon points (1000 locations)
num_samples = 1000
sampled_lats = np.random.uniform(lat_min, lat_max, num_samples)
sampled_lons = np.random.uniform(lon_min, lon_max, num_samples)

# Convert to DataFrame
mc_samples = pd.DataFrame({"latitude": sampled_lats, "longitude": sampled_lons})

# Convert to GeoDataFrame for export
gdf = gpd.GeoDataFrame(mc_samples, geometry=gpd.points_from_xy(sampled_lons, sampled_lats),crs="EPSG:4326")
gdf.to_file("monte_carlo_samples.geojson", driver="GeoJSON")

print("Monte Carlo Sampling Complete: 1000 locations saved.")