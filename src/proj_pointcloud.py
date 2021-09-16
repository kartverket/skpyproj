

import numpy as np
from pyproj import CRS
from pyproj import Transformer, transform
from pyproj.aoi import AreaOfInterest, AreaOfUse, BBox
from pyproj.database import query_utm_crs_info, query_crs_info

fromepsgcode = 7789 #int(input("Enter EPSG code source crs: "))
print(fromepsgcode)

toepsgcode = 4936 #int(input("Enter EPSG code target crs: "))
print(toepsgcode)

areaepsgcode = 1352 #int( input("Enter EPSG code area extent: "))
print(areaepsgcode)

# Norway 1352
if areaepsgcode == 1352:
    area = AreaOfInterest(4.68, 57.93, 31.22, 71.21)
    aou = AreaOfUse(4.68, 57.93, 31.22, 71.21, "Norway - onshore")
else:
    area = AreaOfInterest(10.03, 54.96, 24.17, 69.07)
    aou = AreaOfUse(10.03, 54.96, 24.17, 69.07, "Sweden")

utm_crs_list = query_utm_crs_info(
    datum_name="WGS 84",
    area_of_interest=AreaOfInterest(
        west_lon_degree=-93.581543,
        south_lat_degree=42.032974,
        east_lon_degree=-93.581543,
        north_lat_degree=42.032974,
    ),
)
utm_crs = CRS.from_epsg(utm_crs_list[0].code)
print(utm_crs)

#TRYS
x_coords = 2987993.64255 # np.random.randint(80000, 120000)
y_coords = 655946.42161  # np.random.randint(200000, 250000)
z_coords = 5578690.43270 # np.random.randint(200000, 250000)
epoch = 2020.00

transformer1 = Transformer.from_crs(fromepsgcode, toepsgcode, area_of_interest = area)
#transformer1 = Transformer.from_crs(CRS.from_epsg(7789), CRS.from_epsg(4936))
#transformer1 = Transformer.from_crs(CRS.from_epsg(7789), CRS.from_epsg(4936), area_of_interest = area)
res1 = transformer1.transform(x_coords, y_coords, z_coords, epoch)
print(res1)

# Sweden 4378
transformer2 = Transformer.from_proj(fromepsgcode, toepsgcode)
res2 = transformer2.transform(x_coords, y_coords, z_coords, epoch)
print(res2)

transform(fromepsgcode, toepsgcode, x_coords, y_coords, z_coords, epoch)

crs = CRS.from_epsg(7789)
crs = CRS.from_string("epsg:4326")

crs.to_epsg()
crs.to_authority()

print(x_coords, y_coords, z_coords, epoch)
