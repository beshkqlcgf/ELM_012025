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

# Print a brief summary of the file
print("=== Dataset Summary ===")
print(dataset)

# Print dimensions and sizes
print("\n=== Dimensions ===")
for dim_name, dim in dataset.dimensions.items():
    print(f"{dim_name}: Size {len(dim)}")

# Print global attributes
print("\n=== Global Attributes ===")
for attr in dataset.ncattrs():
    print(f"{attr}: {getattr(dataset, attr)}")

# Check specific variables
variables_to_check = ['SOIL_COLOR', 'LONGXY', 'LATIXY', 'time', 'MONTHLY_HEIGHT_TOP']

for variable_name in variables_to_check:
    if variable_name in dataset.variables:
        var = dataset.variables[variable_name]
        print(f"\n=== Variable: {variable_name} ===")
        print(f"Data type: {var.dtype}")
        print(f"Dimensions: {var.dimensions}")
        print(f"Shape: {var.shape}")
        print(f"Attributes: {var.ncattrs()}")

        # Safely handle the data output
        data = var[:]
        if data.ndim == 1:  # 1D variable
            print("Data (first 10 elements):", data[:10])
        elif data.ndim == 2:  # 2D variable
            print(f"Matrix Representation:\n{data}")
        elif data.ndim > 2:  # Multi-dimensional variable
            print(f"Variable has {data.ndim} dimensions. Extracting a 2D slice for visualization.")
            
            # For MONTHLY_HEIGHT_TOP, we extract the first slice along the `time` and `lsmpft` dimensions
            if variable_name == "MONTHLY_HEIGHT_TOP":
                print(f"Extracted 2D slice (time=0, lsmpft=0):\n{data[0, 0]}")
            else:
                print(f"Slice of data (first 2D slice):\n{data[0]}")

# Let us try to draw latitude and longitude grids 
longxy = dataset.variables['LONGXY'][:]
latixy = dataset.variables['LATIXY'][:]
# Create a high-resolution plot
fig, ax = plt.subplots(figsize=(16, 10), dpi=150, subplot_kw={'projection': ccrs.PlateCarree()})

# Plot the grid points using scatter
sc = ax.scatter(longxy, latixy, c=latixy, cmap='viridis', s=10, transform=ccrs.PlateCarree())
cbar = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.02, label='Latitude')

# Add features to the map
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.8)
ax.add_feature(cfeature.LAND, facecolor='lightgray', edgecolor='none')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue', edgecolor='none')

# Extract unique latitude and longitude values for gridlines
unique_lons = np.unique(longxy)
unique_lats = np.unique(latixy)

# Add vertical gridlines for all unique longitudes
for lon in unique_lons:
    ax.plot([lon, lon], [latixy.min(), latixy.max()], color='black', linestyle='-', linewidth=0.6, alpha=0.5, transform=ccrs.PlateCarree())

# Add horizontal gridlines for all unique latitudes
for lat in unique_lats:
    ax.plot([longxy.min(), longxy.max()], [lat, lat], color='black', linestyle='-', linewidth=0.6, alpha=0.5, transform=ccrs.PlateCarree())

# Add labels for gridlines
ax.set_xticks(unique_lons, crs=ccrs.PlateCarree())
ax.set_yticks(unique_lats, crs=ccrs.PlateCarree())
ax.tick_params(labelsize=8)
ax.gridlines(draw_labels=True, linewidth=0.8, color='gray', alpha=0.7, linestyle='--')

# Set the title
ax.set_title("High-Quality Map with Latitude and Longitude Grids (LONGXY and LATIXY)", fontsize=16)

# Show the plot
plt.tight_layout()
plt.savefig("grid.png")

# Extract data for mapping for SOIL_COLOR
soil_color = dataset.variables['SOIL_COLOR'][:]

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

