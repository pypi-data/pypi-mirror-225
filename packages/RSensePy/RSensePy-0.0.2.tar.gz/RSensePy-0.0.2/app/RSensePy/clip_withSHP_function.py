import rasterio
from rasterio.plot import show
import os
import numpy as np
import sys
import matplotlib
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
import fiona
from fiona.crs import from_epsg
from rasterio.crs import CRS
from RSensePy.writeRasterFunction import writeRaster

def clipRasterSHP(locationRaster,locationSHP):
	try:
		# Open the shapefile using fiona
		with fiona.open(locationSHP, "r") as shapefile:
			# Extract the geometries (shapes) from the shapefile
			shapes = [feature["geometry"] for feature in shapefile]
	except fiona.errors.DriverError:
		# Handle the case when the shapefile is not found
		print ("Error - Polygon shapefile not found, please check the file path")
		sys.exit()

	with rasterio.open(locationRaster) as src: # Open the raster using rasterio
		out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)  # Clip the raster using the provided shapes (geometries)
		out_meta = src.meta    # Get the metadata of the original raster
	 # Update the metadata for the clipped raster
	out_meta.update({"driver": "GTiff",   # Set the driver for GeoTIFF format
	                 "height": out_image.shape[1],  # Set the height of the clipped raster
	                 "width": out_image.shape[2], # Set the width of the clipped raster
	                 "transform": out_transform, # Set the transformation information
	                 "count":1,  # Set the number of bands (assuming it's a single-band raster)
	                 "dtype":'float32', # Set the data type of the clipped raster to float32
	                 "crs": CRS.from_dict(src.crs)}) # Set the coordinate reference system (CRS) from the original raster

	return out_image,out_meta,src.crs
