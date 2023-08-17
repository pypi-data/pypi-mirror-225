import rasterio
import sys
def writeRaster(out_img,out_meta,out_tif): # Input numpy array of the biophysical output, metadata of clipped raster, output location
  	# Input: `out_img` - numpy array of the biophysical output
    #        `out_meta` - metadata of the clipped raster
    #        `out_tif` - output location to save the raster (GeoTIFF)

	try:
		# Open a new GeoTIFF file for writing with the provided metadata
		with rasterio.open(out_tif, "w", **out_meta) as dest:
			# Write the `out_img` numpy array to the newly created GeoTIFF file
			dest.write(out_img)
	except Exception:
		# Handle any exception that occurs during the writing process
		print ("Invalid output file location")
		sys.exit()

