
"""Transforms coordinates based on pyproj and EPSG codes

Authors:
--------

* Sveinung Himle <himsve@kartverket.no>


Description:
------------


Example:
--------

    >>> python input.csv output.csv 7789 4936

    input.csv is at the format ID(pointname) X Y Z Epoch

"""

# Standard library imports
import numpy as np
import sqlite3
import argparse
import csv as csvinput
import csv as csvoutput #not is use

# External library imports
from pyproj import Transformer, transform
from pyproj.aoi import AreaOfInterest, AreaOfUse, BBox
from pyproj.database import query_utm_crs_info, query_crs_info
from pyproj.datadir import get_data_dir

# Internal library imports
from utilies import get_boundary
  
parser = argparse.ArgumentParser(description='Transforms coordinates from csv files at format ID(pointname) x y z epoc).')

parser.add_argument('input', metavar='InputFile', type=str, help='Path to input csv file')
parser.add_argument('output', metavar='OutputFile', type=str, help='Path to output csv file')
parser.add_argument('epsgsource', metavar='EPSGSource', type=int, help='EPSG code source crs')
parser.add_argument('epsgtarget', metavar='EPSGTarget', type=int, help='EPSG code target crs')
parser.add_argument('--area', metavar = "Area", type=int, help = 'Drit og dra')

args = parser.parse_args()
print('args is: ', args)

inFileName = args.input
outFileName = args.output
epsgsource = args.epsgsource
epsgtarget = args.epsgtarget

if args.area is not None:
    area = args.area
    connectionString = get_data_dir() + '\proj.db'
    bound = get_boundary(connectionString, area)
    transformer = Transformer.from_crs(epsgsource, epsgtarget, area_of_interest = bound)
else:
    #area = 0
    transformer = Transformer.from_crs(epsgsource, epsgtarget)

outputFile = open(outFileName, "w")

pointCount = 0

with open(inFileName) as csvfile:
    spamreader = csvinput.reader(csvfile, skipinitialspace = True, delimiter=' ', quotechar='|')
    for row in spamreader:        
        while ('' in row) : row.remove('')     
        if len(row) < 3:
            continue

        id = row[0]
        x_coords = float(row[1]) if len(row) > 1 else 0
        y_coords = float(row[2]) if len(row) > 2 else 0
        z_coords = float(row[3]) if len(row) > 3 else 0
        epoch = float(row[4]) if len(row) > 4 else 0

        if len(row) == 3:
            res = transformer.transform(x_coords, y_coords)
        elif len(row) == 4:
            res = transformer.transform(x_coords, y_coords, z_coords)
        else:
            res = transformer.transform(x_coords, y_coords, z_coords, epoch)
            
        if len(res) == 2:
            L = [id +' ' + str(res[0]) + ' ' + str(res[1])]
        elif len(res) == 3:
            L = [id + ' ' + str(res[0]) + ' ' + str(res[1]) + ' ' + str(res[2])]
        else:
           L = [id + ' ' + str(res[0]) + ' ' + str(res[1]) + ' ' + str(res[2]) + ' ' + str(res[3])]

        pointCount = pointCount + 1 
    
        outputFile.writelines(L)
        outputFile.writelines('\n')

        print("Source coordinates: ", row)
        print("Target coordinates: ", L)

outputFile.close()

print('Transformations succeed!')
print(f'{pointCount} points were transformed')

#if __name__ == '__main__':
