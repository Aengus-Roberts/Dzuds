import numpy as np
import cdsapi, time, geopandas as gpd, pandas as pd
import xarray as xr
from tqdm import tqdm

mcs_file = "../data/monte_carlo_samples.geojson"
gdf = gpd.read_file(mcs_file).to_crs(epsg=4326)  # Ensure WGS84 CRS
print(f"Loaded {mcs_file} with CRS: {gdf.crs}")

# Read date windows from file
with open("../data/date_windows.txt", "r") as f:
    dates = [line.strip() for line in f.readlines()]


client = cdsapi.Client()
results = []

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "2m_temperature",
        "surface_pressure",
        "total_precipitation",
        "lake_ice_depth",
        "snow_depth",
        "snowfall",
        "high_vegetation_cover",
        "low_vegetation_cover",
        "total_cloud_cover",
        "volumetric_soil_water_layer_1"
    ],
    "year": [
        "1940", "1941", "1942",
        "1943", "1944", "1945",
        "1946", "1947", "1948",
        "1949", "1950", "1951",
        "1952", "1953", "1954",
        "1955", "1956", "1957",
        "1958", "1959", "1960",
        "1961", "1962", "1963",
        "1964", "1965", "1966",
        "1967", "1968", "1969",
        "1970", "1971", "1972",
        "1973", "1974", "1975",
        "1976", "1977", "1978",
        "1979", "1980", "1981",
        "1982", "1983", "1984",
        "1985", "1986", "1987",
        "1988", "1989", "1990",
        "1991", "1992", "1993",
        "1994", "1995", "1996",
        "1997", "1998", "1999",
        "2000", "2001", "2002",
        "2003", "2004", "2005",
        "2006", "2007", "2008",
        "2009", "2010", "2011",
        "2012", "2013", "2014",
        "2015", "2016", "2017",
        "2018", "2019", "2020",
        "2021", "2022", "2023",
        "2024", "2025"
    ],
    "month": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"
    ],
    "day": ["01", "15"],
    "time": ["12:00"],
    "data_format": "grib",
    "download_format": "unarchived"
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()

"""
for index, row in  tqdm(gdf.iterrows(), total=len(gdf)):
    lat = row.geometry.y
    lon = row.geometry.x

    filename = f"era5_{lat}_{lon}.nc"
    client.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': [
                '2m_temperature', 'snow_depth', 'snowfall',
                'lake_ice_depth', 'volumetric_soil_water_layer_1',
                'total_precipitation', 'surface_pressure',
                'total_cloud_cover', 'high_vegetation_cover',
                'low_vegetation_cover'
            ],
            'date': dates,
            'time': ['12:00'],
            'format': 'netcdf',
            'area': [lat + 0.05, lon - 0.05, lat - 0.05, lon + 0.05],  # small bbox
        },
        filename
    )
    time.sleep(1)

"""