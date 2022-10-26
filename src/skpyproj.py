
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

    Or:

    >>> python --input input.csv --output output.csv 7789 "+proj=utm +zone=32 +ellps=GRS80"
    
    Or with area extent:
    
    >>> python --input input.csv --output output.csv 7789 4936 --area 1352

"""

# Standard library imports
import numpy as np
import csv as csvinput
import os
import argparse
from datetime import date

# External library imports
from pyproj import Transformer, transform, CRS
from pyproj.aoi import AreaOfInterest, AreaOfUse, BBox
from pyproj.database import query_utm_crs_info, query_crs_info
from pyproj.datadir import get_data_dir, get_user_data_dir
from pyproj._show_versions import _get_proj_info

# Internal library imports
from utilies import get_boundary, try_parse_int, projsync

parser = argparse.ArgumentParser(description='Transforms coordinates from csv files at format ID(pointname) x y z epoch).')

parser.add_argument('sourcecrs', metavar='SourceCrs', type=str, help='EPSG code or proj string of source crs')
parser.add_argument('targetcrs', metavar='TargetCrs', type=str, help='EPSG code or proj string of target crs')

parser.add_argument('--input', metavar='InputFile', type=str, help='Path to input csv file')
parser.add_argument('--output', metavar='OutputFile', type=str, help='Path to output csv file')
parser.add_argument('--area', metavar = "Area", type=int, help = 'EPSG code area extent')
parser.add_argument('-d', metavar = "D", type=int, help = 'Number of decimals')

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

Decimals = 4

if args.d is not None:
    Decimals = args.d

varFormat =str('>18.' + str(Decimals) + 'f')

if outFileName != "":
    outputFile = open(outFileName, "w")

sourcecrs_epsg = args.sourcecrs
targetcrs_epsg = args.targetcrs

sourcecrs_epsg = try_parse_int(sourcecrs_epsg)
targetcrs_epsg = try_parse_int(targetcrs_epsg)

sourcecrs = CRS.from_user_input(sourcecrs_epsg)
targetcrs = CRS.from_user_input(targetcrs_epsg)

'''
Test på rekkjefylgje på x og y:
'''

# Frå source crs
is_geocentric_srs = sourcecrs.is_geocentric
is_geographic_srs = sourcecrs.is_geographic
is_vertical_srs = sourcecrs.is_vertical
is_projected_srs = sourcecrs.is_projected
is_compound_srs = sourcecrs.is_compound

# Frå target crs
is_geocentric_trg = targetcrs.is_geocentric
is_geographic_trg = targetcrs.is_geographic
is_vertical_trg = targetcrs.is_vertical
is_projected_trg = targetcrs.is_projected
is_compound_trg = targetcrs.is_compound

'''
Dette gjeld både input- og output-crs
Viss is_projected = True eller is_geocentric = True => rekkjefylgje (x, y)
Viss is_geographic = True => (y, x)

NB! Unngå å bruke crs som berre er is_vertical = True, t.d. 5941. Bruk heller 5942.
'''
 
# Denne er sett til False. Då er det betre å leggje logikken i is_geographic, is_geocentric eller is_projected
m_always_xy = False

if args.area is not None:
    area = args.area
    # print(get_data_dir())
    # print(get_user_data_dir())
    connectionString = get_data_dir() + '\proj.db'
    bound = get_boundary(connectionString, area)
    transformer = Transformer.from_crs(sourcecrs_epsg, targetcrs_epsg, area_of_interest = bound, always_xy=m_always_xy)
else:
    transformer = Transformer.from_crs(sourcecrs_epsg, targetcrs_epsg, always_xy=m_always_xy)

pointCount = 0

if os.path.exists(inFileName):
    if outputFile is not None:
        outputFile.writelines('Proj version: ' + str(_get_proj_info()) + '\n')
        outputFile.writelines('From crs: ' + str(sourcecrs_epsg) + ', to crs ' + str(targetcrs_epsg) + '\n')        
        outputFile.writelines('Date: ' + str(date.today()) + '\n')
        
    with open(inFileName) as csvfile:
        spamreader = csvinput.reader(csvfile, skipinitialspace = True, delimiter=' ', quotechar='|')
        for row in spamreader:
            while ('' in row) : row.remove('')

            if len(row) < 3:
                continue

            id = row[0]
            x = float(row[1]) if len(row) > 1 else 0
            y = float(row[2]) if len(row) > 2 else 0
            z = float(row[3]) if len(row) > 3 else 0
            e = float(row[4]) if len(row) > 4 else 0

            if len(row) == 3:
                res = transformer.transform(x, y)                
                output_line = ("{: <8}".format(id) + format(res[0], varFormat) + format(res[1], varFormat))
                input_line = ("{: <8}".format(id) + format(x, varFormat) + format(y, varFormat))
            elif len(row) == 4:
                res = transformer.transform(x, y, z)                
                output_line = ("{: <8}".format(id) + format(res[0], varFormat) + format(res[1], varFormat) + format(res[2], varFormat))
                input_line = ("{: <8}".format(id) + format(x, varFormat) + format(y, varFormat) + format(z, varFormat))
            else:
                res = transformer.transform(x, y, z, e)                
                output_line = ("{: <8}".format(id) + format(res[0], varFormat) + format(res[1], varFormat) + format(res[2], varFormat) + format(res[3], varFormat))                
                input_line = ("{: <8}".format(id) + format(x, varFormat) + format(y, varFormat) + format(z, varFormat) + format(e, varFormat))                

            pointCount = pointCount + 1

            if outputFile is not None:
                outputFile.writelines(output_line)
                outputFile.writelines('\n')

            print("Source coordinates: ", input_line)
            print("Target coordinates: ", output_line)
else:
    while True:
        inputcoord = input("Enter input coordinates (X Y Z Epoch): ")
        
        if inputcoord == '' or inputcoord.lower() == 'exit' or inputcoord.lower() == 'quit':
            break

        splitline = inputcoord.split()
        if len(splitline) == 2:
            x = float(splitline[0])
            y = float(splitline[1])
            res = transformer.transform(x, y)
            output_line = (format(res[0], varFormat) + format(res[1], varFormat))               
        elif len(splitline) ==3:
            x = float(splitline[0])
            y = float(splitline[1])
            z = float(splitline[2])
            res = transformer.transform(x, y, z)
            output_line = (format(res[0], varFormat) + format(res[1], varFormat) + format(res[2], varFormat))          
        elif len(splitline) == 4:
            x = float(splitline[0])
            y = float(splitline[1])
            z = float(splitline[2])
            e = float(splitline[3])
            res = transformer.transform(x, y, z, e)
            output_line = (format(res[0], varFormat) + format(res[1], varFormat) + format(res[2], varFormat) + format(res[3], varFormat))          
       
        pointCount = pointCount + 1

        print(output_line)

        if outputFile is not None:
            outputFile.writelines(output_line)
            outputFile.writelines('\n')

if outputFile is not None:
    outputFile.close()

print('Transformations succeed!')
print(f'{pointCount} points were transformed')
