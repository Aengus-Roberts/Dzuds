import xarray as xr
import scipy
import geopandas as gpd
import numpy as np
from tqdm import tqdm

# Replace with your actual file path
grib_file = "../data/39d048b223926fa08a56cda2e64350f8.grib"

# Open the GRIB file with cfgrib engine
ds = xr.open_dataset(grib_file, engine="cfgrib")

gdf = gpd.read_file("../data/monte_carlo_samples.geojson")
# Extract lat/lon lists
lats = gdf.geometry.y.values
lons = gdf.geometry.x.values

n_points = len(lats)
n_times = len(ds['t2m'].time)
variables = ['t2m', 'sp', 'licd', 'sd', 'cvh', 'cvl', 'tcc', 'swvl1']
n_vars = len(variables)

sampled_data = np.empty((n_points, n_times, n_vars), dtype=np.float32)

for k, var_name in enumerate(variables):
    da = ds[var_name]  # DataArray for the variable
    print(da)
    for j, t in enumerate(tqdm(da.time,total=n_times)):
        # Interpolate all points at once
        values = da.sel(time=t).interp(latitude=("points", lats), longitude=("points", lons))
        sampled_data[:, j, k] = values.values

np.savez("../data/sampled_data_bundle.npz", data=sampled_data, lat=lats, lon=lons, time=ds.time.values, variables=variables)