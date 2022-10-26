import sqlite3
from pyproj.aoi import AreaOfInterest
from pyproj.datadir import get_data_dir
import pyproj.sync

def try_parse_int(text):
    try:
        return int(text)
    except:
        return text

def get_boundary(database_file, areaepsgcode):
    south_lat = north_lat = west_lon = east_lon = 0

    connection = sqlite3.connect(database_file)
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

    return AreaOfInterest(west_lon, south_lat, east_lon, north_lat)

def projsync():
    #syncs Norwegian resources
    pyproj.sync.get_transform_grid_list('no_kv', include_already_downloaded=False)
    #syncs NKG resources
    pyproj.sync.get_transform_grid_list('eur_nkg', include_already_downloaded=False)
