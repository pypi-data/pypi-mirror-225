The Python Geospatial Library, Geotran, is a comprehensive toolkit for geospatial data preprocessing, analysis, and modeling. It provides a variety of functions for transforming and manipulating geospatial data, including data normalization, resampling, filtering, and feature selection. It also offers a range of analytical techniques, such as spatial clustering, classification, and regression, as well as machine learning algorithms for predictive modeling.    

Geotran is designed to work with a variety of geospatial data formats, including shapefiles, GeoJSON, and raster data. It also supports integration with popular geospatial tools and platforms, such as QGIS, GDAL, and ArcGIS.     

Geotran is widely used in the geospatial industry, research, and open-source communities for developing geospatial applications, performing spatial analysis, and modeling complex geospatial phenomena.        

Example:     

```
from geotran import raster
from matplotlib import pyplot


fig, (axr, axg, axb) = pyplot.subplots(1,3, figsize=(21,7))

raster.plot('T60GVV.tif',bands=[3],ax=axr, title="Red", cmap='Reds')
raster.plot('T60GVV.tif',bands=[2],ax=axg, title="Green", cmap="Greens")
raster.plot('T60GVV.tif',bands=[1],ax=axb, title="Blue", cmap="Blues")
![Alt text](image.png)

input_raster_files = ['blue.tif', 'green.tif',
                      'red.tif', 'red-edge.tif', 'nir.tif']
output_raster_file = datetime.now().strftime("%d%m%Y%H%M%S") + "_stacked.tif"

stacked_file = stack_rasters(input_raster_files, output_raster_file, band_names=[
                             'blue', 'green', 'red', 'rededge', 'nir'])

clip_raster_by_shp(raster_file, shapefile, output_file, epsg_code=2193)

(more)