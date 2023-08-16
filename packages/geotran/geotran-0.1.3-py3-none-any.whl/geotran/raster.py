from math import radians, cos, sin, asin, sqrt
import rasterio
from matplotlib import pyplot
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
import pandas as pd
import shutil
from rasterio.warp import reproject, Resampling, calculate_default_transform
from shapely.geometry import Point
from rasterio import transform
from rasterio import features
from rasterio.enums import MergeAlg

def normalise(array):
    min = np.percentile(array, 0.5)  
    max = np.percentile(array, 99.5)    
    norm = (array - min) / (max-min)
    norm[norm<0.0] = 0.0
    norm[norm>1.0] = 1.0
    return norm

def plot(file, bands=(3, 2, 1),cmap='viridis', title='Raster photo',ax=None):
    src = rasterio.open(file)
    if len(bands) == 3:
        image_data = src.read(bands)
    elif len(bands) == 1:
        image_data = src.read(bands)
    else:
        raise ValueError("You must provide 1 or 3 bands to display.")
    image_data[image_data == 65536] = 0.0
    normalized_data = np.stack([normalise(band) for band in image_data])

    show(normalized_data,cmap=cmap, title=title, ax=ax)

def plot_contour(file):
    src = rasterio.open(file)
    fig, ax = pyplot.subplots(1, figsize=(12, 12))
    show((src, 1), cmap='Greys_r', interpolation='none', ax=ax)
    show((src, 1), contour=True, ax=ax)
    pyplot.show()

def plot_hist(file, bin=50, title="Histogram"):
    src = rasterio.open(file)
    show_hist(
    src, bins=bin, lw=0.0, stacked=False, alpha=0.3,
    histtype='stepfilled', title=title)  

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

def stack_rasters(input_files, output_file, band_names=None):
    # Read metadata of the first file
    with rasterio.open(input_files[0]) as src0:
        meta = src0.meta

    # Update meta to reflect the number of layers
    meta.update(count=len(input_files))

    if band_names:
        meta.update(nodename=','.join(band_names))

    # Create the output stacked raster file
    with rasterio.open(output_file, 'w', **meta) as dst:
        for idx, layer in enumerate(input_files):
            with rasterio.open(layer) as src:
                dst.write_band(idx + 1, src.read(1))
                if band_names:
                    dst.set_band_description(idx + 1, band_names[idx])

    return output_file

def update_band_names(input_raster, band_names):
    with rasterio.open(input_raster, 'r+') as src:
        src.descriptions = tuple(band_names)


def getFeatures(geo):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(geo.to_json())['features'][0]['geometry']]

def clip_raster_by_shp(raster_file, shapefile, output_file, epsg_code=4326):
    geo = gpd.read_file(shapefile)
    coords = getFeatures(geo)
    src = rasterio.open(raster_file)

    # Clip the raster with Polygon
    out_img, out_transform = mask(dataset=src, shapes=coords, crop=True)

    # Copy the metadata
    out_meta = src.meta.copy()
    band_names = src.descriptions

    out_meta.update({"driver": "GTiff",
                    "height": out_img.shape[1],
                     "width": out_img.shape[2],
                     "transform": out_transform,
                     "crs": epsg_code,
                     }
                    )

    # # save the clipped raster to Subset folder
    with rasterio.open(output_file, "w", **out_meta) as dest:
        dest.write(out_img)

    if band_names:
        update_band_names(output_file, band_names)


def extract(rf, shp):
    gdf = gpd.read_file(shp)
    src = rasterio.open(rf)
    pixel_coords = []
    extracted_data = []

    for idx, row in gdf.iterrows():
        geom = row.geometry
        attributes = row.to_dict()  # Get all columns as a dictionary

        mask = rasterio.features.geometry_mask([geom], src.shape, transform=src.transform, invert=True, all_touched=True)
        data = {}
        for i in range(src.count):
            band = src.read(i + 1, masked=True)[mask]
            column_name = f'band_{i+1}'
            data[column_name] = band.flatten()

        row, col = np.where(mask == True)
        coords = [Point(src.xy(r, c)) for r, c in zip(row, col)]

        # Create a DataFrame for the extracted data
        extracted_df = pd.DataFrame(data)
        
        # Include all shapefile columns as attributes
        for key, value in attributes.items():
            extracted_df[key] = value
        
        extracted_df['geometry'] = coords
        
        extracted_data.append(extracted_df)

    gdf_extracted = pd.concat(extracted_data, ignore_index=True)
    gdf_extracted = gpd.GeoDataFrame(gdf_extracted, geometry='geometry', crs=src.crs)

    return gdf_extracted


def savetif(output, gdf, colname='FVC', input_raster=None, resolution=10, dtype=rasterio.float32):
    
    bbox = gdf.total_bounds
    xmin, ymin, xmax, ymax = bbox

    if input_raster:        
        with rasterio.open(input_raster) as src:            
            res = src.res[0]
    else:
        res = resolution  # Default desired resolution

    w = int(xmax - xmin) // res
    h = int(ymax - ymin) // res
    out_meta = {
        "driver": "GTiff",
        "dtype": dtype,
        "height": h,
        "width": w,
        "count": 1,
        "crs": gdf.crs,
        "transform": transform.from_bounds(xmin, ymin, xmax, ymax, w, h),
        "compress": 'lzw'
    }
    with rasterio.open(output, 'w+', **out_meta) as out:
        out_arr = out.read(1)

        # this is where we create a generator of geom, value pairs to use in rasterizing
        shapes = ((geom, value)
                  for geom, value in zip(gdf.geometry, gdf[colname]))
        burned = features.rasterize(shapes, out=out_arr,
                                    out_shape=out.shape,
                                    transform=out.transform,
                                    all_touched=True,
                                    fill=255,   # background value
                                    merge_alg=MergeAlg.replace,
                                    dtype=dtype)

        out.write_band(1, burned)