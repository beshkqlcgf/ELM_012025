##########################################################
################# EXPLORE SURF_DATA FILE #################
##########################################################

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# File path
file_path = "/pscratch/sd/w/wang1698/rw_project/surfdata_0.9x1.25_simyr1700_c240826.nc"
dataset = Dataset(file_path, mode='r')

# Get a brief summary
print(dataset)

# Explore metadata
print("Dimensions:", dataset.dimensions.keys())
for dim_name, dim in dataset.dimensions.items():
    print(f"Dimension: {dim_name}, Size: {len(dim)}")

# Global attributes
print("Global attributes:", dataset.ncattrs())
for attr in dataset.ncattrs():
    print(f"{attr}: {getattr(dataset, attr)}")

# Explore variables
print("Variables:", dataset.variables.keys())

# Check three specific variables: 'SOIL_COLOR', 'LONGXY', and 'LATIXY'
variables_to_check = ['SOIL_COLOR', 'LONGXY', 'LATIXY']
for variable_name in variables_to_check:
    if variable_name in dataset.variables:
        var = dataset.variables[variable_name]
        print(f"\nVariable: {variable_name}")
        print(f"Data type: {var.dtype}")
        print(f"Dimensions: {var.dimensions}")
        print(f"Shape (size of each dimension): {var.shape}")
        print(f"Attributes: {var.ncattrs()}")
        print(f"Data: {var[:]}")  # Be cautious with large datasets

        # Print matrix representation
        data = var[:]
        print(f"\nMatrix Representation of {variable_name}:\n")
        if data.ndim == 2:
            print(data)
        else:
            print(f"{variable_name} has more than 2 dimensions; showing a 2D slice.")
            print(data[0])  # Display first "slice" of high-dimensional data

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

# Save the plot
plt.savefig("map_output.png")
print("Map saved as map_output.png")

