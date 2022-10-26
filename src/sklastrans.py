"""Transforms las-files based on python packages pyproj and laspy. EPSG codes are used for source and target crs'es.

Authors:
--------

* Sveinung Himle <himsve@kartverket.no>


Description:
------------


Example:
--------

    >>> python --input input.las --output output.las 25832 "+proj=utm +zone=31 +ellps=GRS80" 
         
    Or:
    
    >>> python --input input.las --output output.las 25832 5105

"""

# Standard library imports
import csv as csvinput
import os
import argparse
import sys

# External library imports
import laspy
#import liblas
from pyproj import Transformer, transform, CRS
from progress.bar import Bar

# Internal library imports
from utilies import try_parse_int, projsync

parser = argparse.ArgumentParser(description='Transforms data in LAS-files based on EPSG-kodes.')

parser.add_argument('sourcecrs', metavar='SourceCrs', type=str, help='EPSG code or proj string of source crs')
parser.add_argument('targetcrs', metavar='TargetCrs', type=str, help='EPSG code or proj string of target crs')

parser.add_argument('--input', metavar='InputFile', type=str, help='Path to input LAS file')
parser.add_argument('--output', metavar='OutputFile', type=str, help='Path to output LAS file')

args = parser.parse_args()
print('args is: ', args)

projsync()

outputFile = None

if args.input is not None:
    inFileName = args.input
else:
    inFileName = ""

if args.output is not None:
    outFileName = args.output
else:
    outFileName = ""    

sourcecrs_epsg = args.sourcecrs
targetcrs_epsg = args.targetcrs

sourcecrs_epsg = try_parse_int(sourcecrs_epsg)
targetcrs_epsg = try_parse_int(targetcrs_epsg)

sourcecrs = CRS.from_user_input(sourcecrs_epsg)
targetcrs = CRS.from_user_input(targetcrs_epsg)

# Reads input las file
print ('Reads data from: ', inFileName)
las = laspy.read(inFileName)

x_offset = las.header.x_offset
y_offset = las.header.y_offset
z_offset = las.header.z_offset

x_scale = las.header.x_scale
y_scale = las.header.y_scale
z_scale = las.header.z_scale

x_min = las.header.x_min
y_min = las.header.y_min
z_min = las.header.z_min

x_max = las.header.x_max
y_max = las.header.y_max
z_max = las.header.z_max

new_las = laspy.LasData(las.header)
new_las.header.add_crs(targetcrs)
#print(new_las.header)
new_lasPoints = new_las.points
#print(new_lasPoints)
lasPoints = las.points

#lasPoints
transformer = Transformer.from_crs(sourcecrs_epsg, targetcrs_epsg)
point_format = las.point_format

# New header numbers    
new_x_offset = 0.0
new_y_offset = 0.0
new_z_offset = 0.0

new_x_min = sys.float_info.max
new_y_min = sys.float_info.max
new_z_min = sys.float_info.max

new_x_max = -sys.float_info.max
new_y_max = -sys.float_info.max
new_z_max = -sys.float_info.max

no_of_points = len(lasPoints)

i = 0

bar = Bar('Processed points', max=no_of_points)
for point in lasPoints:
    #print (point.X, point.Y, point.Z)
    
    x_input = point.X*x_scale + x_offset
    y_input = point.Y*y_scale + y_offset
    z_input = point.Z*z_scale + z_offset
    
    #print (x_input, y_input, z_input)
      
    res = transformer.transform(x_input, y_input, z_input)
    
    #print (res[0], res[1], res[2])
    
    if new_x_offset == 0.0 and new_y_offset == 0.0 and new_z_offset == 0.0:
        new_x_offset = round(res[0] - x_input + x_min + (x_max - x_min)/2, -3)
        new_y_offset = round(res[1] - y_input + y_min + (y_max - y_min)/2, -3)
        new_z_offset = round(res[2] - z_input + z_min + (z_max - z_min)/2, -3)
                
    new_x = (res[0] - new_x_offset)/x_scale
    new_y = (res[1] - new_y_offset)/y_scale
    new_z = (res[2] - new_z_offset)/z_scale
    
    #x_test = new_x*x_scale + new_x_offset
    #y_test = new_y*y_scale + new_y_offset
    #z_test = new_z*z_scale + new_z_offset
    
    new_x_min = res[0] if res[0] < new_x_min else new_x_min
    new_y_min = res[1] if res[1] < new_y_min else new_y_min
    new_z_min = res[2] if res[2] < new_z_min else new_z_min
    new_x_max = res[0] if res[0] > new_x_max else new_x_max
    new_y_max = res[1] if res[1] > new_y_max else new_y_max
    new_z_max = res[2] if res[2] > new_z_max else new_z_max
    
    new_lasPoints.X[i] = new_x
    new_lasPoints.Y[i] = new_y
    new_lasPoints.Z[i] = new_z
    
    #print (new_lasPoints.X[i], new_lasPoints.Y[i], new_lasPoints.Z[i])

    bar.next()

    i = i + 1

    #if i > 25000:
    #    break;

print()

# Updates new_lasPoints
new_lasPoints.offsets[0] = new_x_offset
new_lasPoints.offsets[1] = new_y_offset
new_lasPoints.offsets[2] = new_z_offset

new_lasPoints.scales[0] = x_scale
new_lasPoints.scales[1] = y_scale
new_lasPoints.scales[2] = z_scale

# Updates new header
new_las.header.x_max = new_x_max
new_las.header.y_max = new_y_max
new_las.header.z_max = new_z_max
new_las.header.x_min = new_x_min
new_las.header.y_min = new_y_min
new_las.header.z_min = new_z_min

new_las.header.x_offset = new_x_offset
new_las.header.y_offset = new_y_offset
new_las.header.z_offset = new_z_offset
new_las.header.x_scale = x_scale
new_las.header.y_scale = y_scale
new_las.header.z_scale = z_scale

print ('Writes data to: ', outFileName)
new_las.write(outFileName)

print ('Finished')
