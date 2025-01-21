##########################################################
#################### EXPLORE .NC FILE ####################
##########################################################

# open .nc file 
from netCDF4 import Dataset

# file path 
file_path = "/pscratch/sd/w/wang1698/rw_project/surfdata_0.9x1.25_simyr1700_c240826.nc"
dataset = Dataset(file_path, mode='r')

# get a brief summary
print(dataset)

## explore metadata
# list dimensions 
print(dataset.dimensions.keys())
for dim_name, dim in dataset.dimensions.items():
    print(f"Dimension: {dim_name}, Size: {len(dim)}")

# global attributes 
print(dataset.ncattrs())
for attr in dataset.ncattrs():
    print(f"{attr}: {getattr(dataset, attr)}")

# explore variables 
print(dataset.variables.keys())

# let's check one specific varaible as an example: 'SOIL_COLOR'
# check dimensions, attributes, and data points for 'SOIL_COLOR'
variable_name = 'SOIL_COLOR'
if variable_name in dataset.variables:
    var = dataset.variables[variable_name]
    print(f"variable: {variable_name}")
    print(f"dimensions: {var.dimensions}")
    print(f"attributes: {var.ncattrs()}")
    print(f"data_sample: {var[:]}")

# data visualization


##########################################################
#################### END OF THIS FILE ####################
##########################################################
