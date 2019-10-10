print("loading packages")
try:
    import shapefile
except ImportError:
    print('ERROR: shapefile package could not be imported')
    print('Install: py -m pip install pyshp')

try:
    import shapely.geometry as geometry
except ImportError:
    print('ERROR: shapely package could not be imported')
    print('https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely')
    sys.exit()
    
from shapely.geometry import Point, Polygon


try:
    import pandas as pd
except ImportError:
    print('ERROR: pandas package could not be imported')
    print('py -m pip install pandas --user')
    sys.exit()
    
import random
try:
    from geopy.geocoders import Nominatim
except ImportError:
    print('ERROR: geopy package could not be imported')
    print('py -m pip install geopy')
    sys.exit()
    
from functools import partial
try:
    import pyproj
except ImportError:
    print('ERROR: pyproj package could not be imported')
    print('py -m pip install geopy --user')
    sys.exit()
    
from shapely.ops import transform
import cProfile
import re

print("Done")

