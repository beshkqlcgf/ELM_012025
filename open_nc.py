##########################################################
#################### EXPLORE .NC FILE ####################
##########################################################

# open .nc file
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# file path
file_path = "/pscratch/sd/w/wang1698/rw_project/surfdata_0.9x1.25_simyr1700_c240826.nc"
dataset = Dataset(file_path, mode='r')

# get a brief summary
print(dataset)

## explore metadata
# list dimensions
print("Dimensions:", dataset.dimensions.keys())
for dim_name, dim in dataset.dimensions.items():
    print(f"Dimension: {dim_name}, Size: {len(dim)}")

# global attributes
print("Global attributes:", dataset.ncattrs())
for attr in dataset.ncattrs():
    print(f"{attr}: {getattr(dataset, attr)}")

# explore variables
print("Variables:", dataset.variables.keys())

# check three specific variables: 'SOIL_COLOR', 'LONGXY', and 'LATIXY'
variables_to_check = ['SOIL_COLOR', 'LONGXY', 'LATIXY']
for variable_name in variables_to_check:
    if variable_name in dataset.variables:
        var = dataset.variables[variable_name]
        print(f"\nVariable: {variable_name}")
        print(f"Data type: {var.dtype}")
        print(f"Dimensions: {var.dimensions}")
        print(f"Shape (size of each dimensions): {var.shape}")
        print(f"Attributes: {var.ncattrs()}")
        print(f"Data: {var[:]}")  # Be cautious with large datasets

# Extract data for mapping
if all(var in dataset.variables for var in ['SOIL_COLOR', 'LONGXY', 'LATIXY']):
    soil_color = dataset.variables['SOIL_COLOR'][:]
    longxy = dataset.variables['LONGXY'][:]
    latixy = dataset.variables['LATIXY'][:]
else:
    raise ValueError("One or more required variables are missing from the dataset.")

# Set matplotlib to use the non-interactive backend
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for headless systems

# Import other libraries
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Dummy data for testing (replace with your dataset variables)
longxy, latixy = np.meshgrid(np.linspace(-180, 180, 50), np.linspace(-90, 90, 25))
soil_color = np.random.random((25, 50))  # Replace with dataset variable 'SOIL_COLOR'

# Map visualization
plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# Plot data on the map
mesh = ax.pcolormesh(longxy, latixy, soil_color, transform=ccrs.PlateCarree(), cmap='viridis')
plt.colorbar(mesh, ax=ax, orientation='vertical', label="Soil Color")
plt.title("SOIL COLOR MAP")

# Save the plot instead of showing it
plt.savefig("map_output.png")
print("Map saved as map_output.png")
