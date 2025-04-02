import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load your data bundle
data_bundle = np.load("/Users/aengus/PycharmProjects/Dzuds/data/sampled_data_bundle.npz", allow_pickle=True)

data = data_bundle["data"]           # shape (N, T, V)
lats = data_bundle["lat"]
lons = data_bundle["lon"]
times = pd.to_datetime(data_bundle["time"])  # Convert to pandas datetime
variables = data_bundle["variables"].tolist()  # array(['t2m', 'sp', ...])

# Index of 't2m' in the variable list
t2m_index = variables.index("t2m")

# Extract the time series for the first point
t2m_timeseries = data[0, :, t2m_index]

t2m_timeseries_c = t2m_timeseries - 273.15

# Plot
plt.figure(figsize=(12, 5))
plt.plot(times, t2m_timeseries_c)
plt.title(f"2m Temperature at lat={lats[0]:.2f}, lon={lons[0]:.2f}")
plt.xlabel("Time")
plt.ylabel("Temperature (K)")  # ERA5 gives temp in Kelvin
plt.grid(True)
plt.tight_layout()
plt.show()