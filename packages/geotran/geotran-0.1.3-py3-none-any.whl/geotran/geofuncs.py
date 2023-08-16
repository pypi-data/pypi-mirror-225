from math import radians, cos, sin, asin, sqrt
import rasterio
from matplotlib import pyplot
def geoplot(file):
    src = rasterio.open(file)
    pyplot.imshow(src.read(1), cmap='pink')
    pyplot.show()
    return 0
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:

    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers
    return c * r


