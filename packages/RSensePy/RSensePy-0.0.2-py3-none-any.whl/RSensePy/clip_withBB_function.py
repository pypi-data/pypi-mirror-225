import rasterio
from rasterio.plot import show
import os
import sys
import numpy as np
import matplotlib
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
from rasterio.crs import CRS

from RSensePy.writeRasterFunction import writeRaster

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

def clipRasterBB(locationRaster,bbox): #Location - original raster file location and bounding box coordinates bbbox = [minx,miny,maxx,maxy]
	Raster =rasterio.open(locationRaster) # Open raster file
	CRSraster = Raster.crs # Get raster file coordinates
	try:
		bbox = box(bbox[0], bbox[1], bbox[2], bbox[3]) # Define bounding box
	except Exception:
			print ("Error - Bounding box coordinates missing - 4 values needed")
			sys.exit()
	geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs="EPSG:4326") # Define bouding box coordinate system
	geo = geo.to_crs(CRSraster) # Project bounding box coordinates to raster coordinate system
	coords = getFeatures(geo) # Get bounding box coordinates in raster coordinate system
	out_img, out_transform = mask(Raster, coords, crop=True)
	out_meta = Raster.meta.copy() # Create a copy of the original raster file
	#epsg_code = int(Raster.crs.data['init'][5:]) # Get EPSG coordinate value only
	out_meta.update({"driver": "GTiff",
				"height": out_img.shape[1], 
				"width": out_img.shape[2], 
				"transform": out_transform,
				"count":1,
				"dtype":'float32',
				"crs": CRS.from_dict(Raster.crs)}) # Update meta data for the clipped raster
	return out_img,out_meta,Raster.crs  # Return clipped image as a numpy, meta data and epsg_code