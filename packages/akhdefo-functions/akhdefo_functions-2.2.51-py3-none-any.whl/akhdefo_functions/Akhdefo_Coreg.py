import cv2
import numpy as np
import os
import shutil
from osgeo import gdal

def raster_alignment(src_directory, ref_filename, delete_files=False):
    """
    Aligns raster images in a given source directory to a reference image.

    Args:
    src_directory (str): Path to the source directory containing images to align.
    ref_filename (str): Path to the reference image.
    delete_files (bool): If True, deletes the temporary directory created for alignment process. Defaults to False.

    Returns:
    str: Path to the directory containing all registered images.
    """
    # Get the current working directory
    current_dir = os.getcwd()

    # Create a temporary directory inside the current working directory
    temp_dir = os.path.join(current_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    ref = cv2.imread(ref_filename, cv2.IMREAD_COLOR) # Load the reference image in color
    gray_ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY) # Convert to grayscale for SIFT
    sift = cv2.SIFT_create()
    ref_kp, ref_des = sift.detectAndCompute(gray_ref, None) # Find keypoints in grayscale image

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Get the georeference info of the reference image
    ref_raster = gdal.Open(ref_filename)
    ref_geotransform = ref_raster.GetGeoTransform()
    ref_projection = ref_raster.GetProjection()

    # Iterate over each file in the directory
    for filename in os.listdir(src_directory):
        src_filename = os.path.join(src_directory, filename)

        src = cv2.imread(src_filename, cv2.IMREAD_COLOR) # Load the source image in color
        gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) # Convert to grayscale for SIFT
        src_kp, src_des = sift.detectAndCompute(gray_src, None) # Find keypoints in grayscale image

        matches = flann.knnMatch(src_des, ref_des, k=2)

        distances = [m.distance for m, _ in matches]
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)
        z_scores = [(m.distance - mean_distance) / std_distance for m, _ in matches]

        # Keep only the top 10 matches based on z-scores
        top_matches = [matches[i] for i in np.argsort(z_scores)[:10]]

        src_pts = np.float32([src_kp[m.queryIdx].pt for m, _ in top_matches]).reshape(-1, 1, 2)
        ref_pts = np.float32([ref_kp[m.trainIdx].pt for m, _ in top_matches]).reshape(-1, 1, 2)
        best_h, mask = cv2.findHomography(src_pts, ref_pts, cv2.RANSAC, 5.0)

        if len(top_matches) == 0:
            print(f"No good matches found for {filename}")
            continue

        aligned_src = cv2.warpPerspective(src, np.float32(best_h), (ref.shape[1], ref.shape[0]))

        # Crop the aligned source image to the size of the reference image
        height, width = ref.shape[:2]
        aligned_src = aligned_src[:height, :width, :]

        # Get the base name without extension
        base_filename = os.path.splitext(os.path.basename(src_filename))[0]
        # Use TIFF format for the registered image
        registered_filename = os.path.join(temp_dir, f"{base_filename}.tif")

        # Create a new georeferenced raster
        driver = gdal.GetDriverByName('GTiff')
        out_raster = driver.Create(registered_filename, width, height, 3, gdal.GDT_Byte)

        # Set the geo-transform to the one from the reference raster
        out_raster.SetGeoTransform(ref_geotransform)

        # Set the projection to the one from the reference raster
        out_raster.SetProjection(ref_projection)

        # Write the aligned and cropped image data to the raster bands
        for i in range(3):
            out_band = out_raster.GetRasterBand(i + 1)
            out_band.WriteArray(aligned_src[:, :, i])

        # Close the raster file
        out_raster = None

    if delete_files:
        shutil.rmtree(temp_dir)

    return temp_dir  # returns the directory containing all registered images




def Coregistration(input_Folder=r"", output_folder=r"", grid_res=20, min_reliability=60, window_size=(64,64), path_figures=r"", showFig=False, no_data=[0,0], single_ref_path=""):

    """
    This program coregisteres multiple rasters using both structural similarity index and feature matching techniqws.
    This program is written based on arosics python library.
    
    Parameters
    ----------
   
    input_Folder: str
        Path to input raster folders
 
    grid_res: int
    
    min_reliability: int
        structural simialrity index threshold to differentaite deformation from raster shift (min=20, max=100)

    window_size: tuple
        window size for pixel search

    showFig: bool
        True to display results or False to not displat results

    no_data: list
        No data values to be ignored for both reference and target image

    single_ref_path: str
        provide path to raster if interested to coregister all rasters to a single reference, ignore this option the program uses subsequent rasters as refernce. 
    
    output_folder: str
        returns coregistred and georeferenced raster in geotif format

    path_figures: str
        returns figure with plotted displaced pixels in raster coordinate system units

    Returns
    -------
    coregistred rasters

   
    """

    import os
    from os.path import isfile, join
    import numpy as np
    from arosics import COREG, COREG_LOCAL
    from geoarray import GeoArray
    
    if not os.path.exists( output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(path_figures):
        os.makedirs(path_figures)
    
    img_list = [f for f in sorted(os.listdir(input_Folder)) if isfile(join(input_Folder, f))]
    
    f=1
    for n in range(0, len(img_list)):
        # for item2 in img_list[n+1:]:
        #     for item3 in img_list[n+2:]:

       
        # img_src1=rasterio.open(join(input_Folder,img_list[n]), "r+", masked=True)
        # img_src2=rasterio.open(join(input_Folder,img_list[n+1]), "r+", masked=True)
        # img_src3=rasterio.open(join(input_Folder,img_list[n+2]), "r+", masked=True)
        if single_ref_path!="":
            item1=img_list[n]
           
            
            im_reference = single_ref_path
            im_target1    = join(input_Folder,img_list[n])
            
            #####################
            # # get a sample numpy array with corresponding geoinformation as reference image
            # geoArr  = GeoArray(im_reference)

            # ref_ndarray = geoArr[:]            # numpy.ndarray with shape (10980, 10980)
            # ref_gt      = geoArr.geotransform  # GDAL geotransform: (300000.0, 10.0, 0.0, 5900040.0, 0.0, -10.0)
            # ref_prj     = geoArr.projection    # projection as WKT string ('PROJCS["WGS 84 / UTM zone 33N....')

            # # get a sample numpy array with corresponding geoinformation as target image
            # geoArr  = GeoArray(im_target1)

            # tgt_ndarray = geoArr[:]            # numpy.ndarray with shape (10980, 10980)
            # tgt_gt      = geoArr.geotransform  # GDAL geotransform: (300000.0, 10.0, 0.0, 5900040.0, 0.0, -10.0)
            # tgt_prj     = geoArr.projection    # projection as WKT string ('PROJCS["WGS 84 / UTM zone 33N....')

            
            
            ###############
            kwargs = {
            'grid_res'     : grid_res,
            'window_size'  : window_size,
            'path_out' : output_folder + "/" + item1,
            'fmt_out'  : 'GTIFF',
            'min_reliability': min_reliability , 'nodata': no_data}
            
            # CRL = COREG_LOCAL(GeoArray(ref_ndarray, ref_gt, ref_prj),
            #       GeoArray(tgt_ndarray, tgt_gt, tgt_prj),
            #       **kwargs)
            CRL = COREG_LOCAL(im_reference,im_target1,**kwargs)
            CRL.correct_shifts()
            title="Coregistration: "+ im_reference[:-4] + "_" + item1[:-4]
            CRL.view_CoRegPoints(figsize=(15,15), backgroundIm='ref', title=title, savefigPath=path_figures+"/"+item1[:-4]+".jpg", showFig=showFig)
        else:
            item1=img_list[n]
            item2=img_list[n+1]
            item3=img_list[n+2]
                
            if n==0:
                im_reference = join(input_Folder,img_list[0])
                im_target1    = join(input_Folder,img_list[n+1])
                im_target2    = join(input_Folder,img_list[n+2])
                
                kwargs = {
                'grid_res'     : grid_res,
                'window_size'  : window_size,
                'path_out' : output_folder + "/" + item1,
                'fmt_out'  : 'GTIFF',
                'min_reliability': min_reliability , 'nodata': no_data}

                CRL = COREG_LOCAL(im_reference,im_target1,**kwargs)
                CRL.correct_shifts()
                title="Coregistration: "+ item1[:-4] + "_" + item1[:-4]
                CRL.view_CoRegPoints(figsize=(15,15), backgroundIm='ref', title=title, savefigPath=path_figures+"/"+title[16:]+".jpg", showFig=showFig)
            elif n> 0:
                im_reference = join(input_Folder,img_list[n])
                im_target1    = join(input_Folder,img_list[n+1])
                im_target2    = join(input_Folder,img_list[n+2])

                kwargs2 = {
                'grid_res'     : grid_res,
                'window_size'  : window_size,
                'path_out' : output_folder + "/" + item2,
                'fmt_out'  : 'GTIFF',
                'min_reliability': min_reliability , 'nodata': no_data}

                CRL = COREG_LOCAL(im_reference,im_target1,**kwargs2)
                CRL.correct_shifts()
                title="Coregistration: "+ item1[:-4] + "_" + item2[:-4]
                CRL.view_CoRegPoints(figsize=(15,15), backgroundIm='ref', title=title, savefigPath=path_figures+"/"+title[16:]+".jpg", showFig=showFig)
                
                kwargs3 = {
                'grid_res'     : grid_res,
                'window_size'  : window_size,
                'path_out' : output_folder + "/" + item3,
                'fmt_out'  : 'GTIFF',
                'min_reliability': min_reliability , 'nodata': no_data}

                CRL = COREG_LOCAL(im_reference,im_target2,**kwargs3)
                CRL.correct_shifts()
                
                title="Coregistration: "+ item1[:-4] + "_" + item3[:-4]
                CRL.view_CoRegPoints(figsize=(15,15), backgroundIm='ref', title=title, savefigPath=path_figures+"/"+title[16:]+".jpg", showFig=showFig)
                
            elif (len(img_list) - 2) == f:
                im_reference = join(input_Folder,img_list[f])
                im_target1    = join(input_Folder,img_list[f])
                #im_target2    = join(input_Folder,img_list[f])
                
                kwargs = {
                'grid_res'     : grid_res,
                'window_size'  : window_size,
                'path_out' : output_folder + "/" + item1,
                'fmt_out'  : 'GTIFF',
                'min_reliability': min_reliability , 'nodata': no_data}

                CRL = COREG_LOCAL(im_reference,im_target1,**kwargs)
                CRL.correct_shifts()
                title="Coregistration: "+ item1[:-4] + "_" + item1[:-4]
                CRL.view_CoRegPoints(figsize=(15,15), backgroundIm='ref', title=title, savefigPath=path_figures+"/"+title[16:]+".jpg", showFig=showFig)
            if (len(img_list)) == f:
                break
            print (" process is compeleted")
        print (" process is compeleted")      
