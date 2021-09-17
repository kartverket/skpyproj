
"""Transforms coordinates based on pyproj and EPSG codes

Authors:
--------

* Sveinung Himle <himsve@kartverket.no>


Description:
------------


Example:
--------

    >>> python input.csv output.csv 7789 4936

    input.csv is at the format ID X Y Z Epoch

"""

# Standard library imports
import numpy as np
import argparse

# External library imports
import csv as csvinput
import csv as csvoutput #not is use
from pyproj import Transformer, transform
from pyproj.aoi import AreaOfInterest, AreaOfUse, BBox
from pyproj.database import query_utm_crs_info, query_crs_info
  
parser = argparse.ArgumentParser(description='Transforms coordinates from csv files at format (ID x y z epoch).')

parser.add_argument('input', metavar='InputFile', type=str, help='Path to input csv file')
parser.add_argument('output', metavar='OutputFile', type=str, help='Path to output csv file')
parser.add_argument('epsgsource', metavar='EPSGSource', type=int, help='EPSG code source crs')
parser.add_argument('epsgtarget', metavar='EPSGTarget', type=int, help='EPSG code target crs')

args = parser.parse_args()
print('args is: ', args)

inFileName = args.input
outFileName = args.output
epsgsource = args.epsgsource
epsgtarget = args.epsgtarget

transformer1 = Transformer.from_crs(epsgsource, epsgtarget)

outputFile = open(outFileName, "w")

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
            res = transformer1.transform(x_coords, y_coords)            
        elif len(row) == 4:
            res = transformer1.transform(x_coords, y_coords, z_coords)            
        else:
            res = transformer1.transform(x_coords, y_coords, z_coords, epoch)
            
        if len(res) == 2:
            L = [id, ' ', str(res[0]), ' ', str(res[1])] 
            #pass
        elif len(res) == 3:
            L = [id, ' ', str(res[0]), ' ', str(res[1]), ' ', str(res[2])]
            #pass
        else:
           L = [id, ' ', str(res[0]), ' ', str(res[1]), ' ', str(res[2]), ' ', str(res[3])]
   
        outputFile.writelines(L)
        outputFile.writelines('\n')
        print(L)
        print(row)

outputFile.close()

#TODO: Print number of objects

print('Transformations succeed!')
#if __name__ == '__main__':
