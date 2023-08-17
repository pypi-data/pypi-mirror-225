import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from RSensePy.clip_withBB_function import clipRasterBB
from RSensePy.clip_withSHP_function import clipRasterSHP
from RSensePy.writeRasterFunction import writeRaster
def cloud_mask_landsat8_clip_shp(image_path, locationSHP):
    resultTest=clipRasterSHP(image_path,locationSHP)
    qa_bandTest = resultTest[0]
    #Extract cloud and cloud shadow bits
    cloud_bit = 3
    cloud_shadow_bit = 4

    # Create cloud mask based on confidence thresholds
    cloud_mask = np.bitwise_and(np.right_shift(qa_bandTest, cloud_bit), 1)
    cloud_shadow_mask = np.bitwise_and(np.right_shift(qa_bandTest, cloud_shadow_bit), 1)
    cloud_mask = np.where(qa_bandTest >= (1 << cloud_bit), cloud_mask, 0)
    cloud_shadow_mask = np.where(qa_bandTest >= (1 << cloud_shadow_bit), cloud_shadow_mask, 0)
    
    # Combine cloud and cloud shadow masks
    
    combined_mask = np.logical_or(cloud_mask, cloud_shadow_mask)
    combined_mask =  np.where((combined_mask==0)|(combined_mask==1), combined_mask^1,combined_mask) # Convert zeors to one and ones to zero
    combined_mask = np.where(combined_mask==0, np.nan, combined_mask) # Assign null values to zeros
    return combined_mask,resultTest[1]

def cloud_mask_landsat8_clip(image_path, bbcoord):
    resultTest=clipRasterBB(image_path,bbcoord)  # Call clip function to clip the QA band.
    qa_bandTest = resultTest[0]
    #Extract cloud and cloud shadow bits
    cloud_bit = 3
    cloud_shadow_bit = 4
    # Create cloud mask based on confidence thresholds
    cloud_mask = np.bitwise_and(np.right_shift(qa_bandTest, cloud_bit), 1)
    cloud_shadow_mask = np.bitwise_and(np.right_shift(qa_bandTest, cloud_shadow_bit), 1)
    


    """
    The function applies the confidence thresholds to the cloud and cloud shadow masks. 
    It uses the bitwise right shift operator to shift the value 1 by the cloud and cloud 
    shadow bits and compares it to the QA band values. If the QA band value is greater 
    than or equal to the shifted value, the pixel is considered to have sufficient confidence 
    for cloud or cloud shadow detection. Otherwise, the pixel is set to 0 in the respective mask.
    """
    cloud_mask = np.where(qa_bandTest >= (1 << cloud_bit), cloud_mask, 0)
    cloud_shadow_mask = np.where(qa_bandTest >= (1 << cloud_shadow_bit), cloud_shadow_mask, 0)
    
    # Combine cloud and cloud shadow masks
    
    combined_mask = np.logical_or(cloud_mask, cloud_shadow_mask)

    combined_mask =  np.where((combined_mask==0)|(combined_mask==1), combined_mask^1,combined_mask) # Convert zeors to one and ones to zero
    combined_mask = np.where(combined_mask==0, np.nan, combined_mask) # Assign null values to zeros
    return combined_mask,resultTest[1]