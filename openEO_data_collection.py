import openeo
import geopandas as gpd
import pandas as pd

# Connect to openEO backend
connection = openeo.connect("https://openeo.cloud")
connection.authenticate_oidc()  # Authenticate if required

# Load Monte Carlo Sample Locations
mcs_file = "monte_carlo_samples.geojson"
gdf = gpd.read_file(mcs_file)

# Select Sentinel-3 SLSTR dataset
data_collection = "SENTINEL3_SLSTR"
bands = ["S8", "S9"]  # Thermal bands

# Define time range
time_range = ("2016-01-01", "2025-01-01")

# Initialize empty results list
results = []

for index, row in gdf.iterrows():
    point = {"type": "Point", "coordinates": [row.geometry.x, row.geometry.y]}

    # Load data for this point
    datacube = connection.load_collection(
        data_collection,
        spatial_extent={
            "west": row.geometry.x - 0.01, "east": row.geometry.x + 0.01,
            "south": row.geometry.y - 0.01, "north": row.geometry.y + 0.01
        },  # Small bounding box to avoid MultiPoint issues
        temporal_extent=time_range,
        bands=bands
    ).filter_spatial(geometries=point)  # Single Point instead of MultiPoint

    # Aggregate temporal data
    time_series = datacube.aggregate_temporal(
        intervals=[time_range],
        reducer="mean"
    ).execute()

    # Append result
    results.append({
        "lon": row.geometry.x,
        "lat": row.geometry.y,
        "time_series": time_series
    })

# Convert to DataFrame
df = pd.DataFrame(results)

# Save and display results
df.to_csv("sentinel3_lst_timeseries.csv", index=False)
