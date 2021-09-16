
import numpy as np
import csv as csvinput 
import argparse

from pyproj import CRS
from pyproj import Transformer, transform
from pyproj.aoi import AreaOfInterest, AreaOfUse, BBox
from pyproj.database import query_utm_crs_info, query_crs_info

##parser = argparse.ArgumentParser(description='Process some integers.')
##parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
##parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')

parser = argparse.ArgumentParser(description='Transforms coordinates from csv files at format (ID,x,y,z,epoch).')

parser.add_argument('input', metavar='InputFile', type=ascii, help='Path to input csv file')
parser.add_argument('output', metavar='OutputFile', type=ascii, help='Path to output csv file')
parser.add_argument('epsgsource', metavar='EPSGSource', type=int, help='EPSG code source crs')
parser.add_argument('epsgtarget', metavar='EPSGTarget', type=int, help='EPSG code target crs')

args = parser.parse_args()
print('args is: ', args)

inFile = args.input
outFile = args.output
epsgsource = args.epsgsource
epsgtarget = args.epsgtarget

##print(args.accumulate(args.integers))

#TRYS
x_coords = 2987993.64255 # np.random.randint(80000, 120000)
y_coords = 655946.42161  # np.random.randint(200000, 250000)
z_coords = 5578690.43270 # np.random.randint(200000, 250000)
epoch = 2020.00

transformer1 = Transformer.from_crs(epsgsource, epsgtarget)
res1 = transformer1.transform(x_coords, y_coords, z_coords, epoch)
print(res1)

crs = CRS.from_epsg(7789)
crs = CRS.from_string("epsg:4326")

crs.to_epsg()
crs.to_authority()
