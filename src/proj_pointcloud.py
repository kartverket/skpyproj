
import numpy as np
import csv as csvinput
import csv as csvoutput
import argparse

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
        id = row[0]
        x_coords = float(row[1])
        y_coords = float(row[2])
        z_coords = float(row[3])
        epoch = float(row[4])
        res = transformer1.transform(x_coords, y_coords, z_coords, epoch)
        x_coords = res[0]
        y_coords = res[1]
        z_coords = res[2]
        L = [id, ' ', str(x_coords), ' ', str(y_coords), ' ', str(z_coords), ' ', str(epoch)]      
        outputFile.writelines(L)
        outputFile.writelines('\n')
        print(L)
        print(row)

outputFile.close()
