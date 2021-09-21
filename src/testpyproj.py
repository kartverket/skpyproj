import numpy as np
import sqlite3
from pyproj import CRS, Proj
from pyproj import Transformer, transform
from pyproj.aoi import AreaOfInterest, AreaOfUse, BBox
from pyproj.database import query_utm_crs_info, query_crs_info
from pyproj.enums import PJType
from pyproj.datadir import get_data_dir

print(get_data_dir() + '\proj.db')

fromepsgcode = 7789 #int(input("Enter EPSG code source crs: "))
print(fromepsgcode)

toepsgcode = 4936 #int(input("Enter EPSG code target crs: "))
print(toepsgcode)

areaepsgcode = 1352 #int( input("Enter EPSG code area extent: "))
print(areaepsgcode)

south_lat = north_lat = west_lon = east_lon = 0

#TODO: Move to new class
connection = sqlite3.connect(get_data_dir() + '\proj.db')
cursor = connection.cursor()
cursor.execute("SELECT south_lat, north_lat, west_lon, east_lon FROM extent WHERE code = " + str(areaepsgcode) + ";")
results = cursor.fetchall()
if len(results) == 1:
    south_lat = float(results[0][0])
    north_lat = float(results[0][1])
    west_lon = float(results[0][2])
    east_lon = float(results[0][3])
cursor.close()
connection.close()

area = AreaOfInterest(west_lon, south_lat, east_lon, north_lat)
print(area)

if area.east_lon_degree == 0 and area.north_lat_degree == 0 and area.south_lat_degree and area.west_lon_degree:
    transformer = Transformer.from_crs(fromepsgcode, toepsgcode)
else:
    transformer = Transformer.from_crs(fromepsgcode, toepsgcode, area_of_interest = area)

#TRYS
x_coords = 2987993.64255 # np.random.randint(80000, 120000)
y_coords = 655946.42161  # np.random.randint(200000, 250000)
z_coords = 5578690.43270 # np.random.randint(200000, 250000)
epoch = 2020.00

res = transformer.transform(x_coords, y_coords, z_coords, epoch)
print(res)

#test 
crs = CRS.from_epsg(7789)
print(crs)
crs = CRS.from_string("epsg:4326")
print(crs)

print(crs.to_epsg())
print(crs.to_authority())
