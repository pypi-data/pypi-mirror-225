import os
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join

import cv2
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
from scipy.interpolate import griddata
from skimage.metrics import structural_similarity as ssim


def Optical_flow_akhdefo(input_dir="", output_dir="", AOI=None, zscore_threshold=2 , ssim_thresh=0.75, image_resolution='3125mm', interpolate=None, show_figure=False, point_size=2,
                          dem_path="", smoothing_kernel_size=11, Vegetation_mask=None):
   
    """
    Performs feature matching and velocity/displacement calculations across a series of images.

    Parameters
    ----------
    input_dir : str
        Path to the directory where the input images are stored.

    output_dir : str
        Path to the directory where the output files will be saved.

    AOI : str
        The shapefile that represents the Area of Interest (AOI).

    zscore_threshold : float
        The threshold value used to filter matches based on their Z-score.

    image_resolution : str
        The resolution of the images specified per pixel. This can be expressed in various units 
        like '3125mm', '3.125m' or '3.125meter'.

    Returns
    -------
    image1 : numpy.ndarray
        The first image in the series.

    image3 : numpy.ndarray
        The third image in the series.

    mean_vel_list : list
        A list of mean velocity arrays, each array corresponding to a pair of images.

    mean_flowx_list : list
        A list of mean x-flow arrays, each array corresponding to a pair of images.

    mean_flowy_list : list
        A list of mean y-flow arrays, each array corresponding to a pair of images.

    points1_i : numpy.ndarray
        Array of keypoints for the first image in the last pair.

    points2 : numpy.ndarray
        Array of keypoints for the second image in the last pair.

    start_date : str
        The start date of the image series.

    end_date : str
        The end date of the image series.
    
    Vegetation_mask: (str, optional)
        Path to a raster file that represents a vegetation mask. Pixels in the input image
        that correspond to non-vegetation in the mask will be set to one. 
    """

    def detect_keypoints(image):
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(image, None)
        return keypoints, descriptors


    def compare_images(image1, image2):
        # Rasterio reads data as (bands, height, width)
        # OpenCV expects data as (height, width, channels)
        # So we need to transpose the data
        # image1 = np.transpose(image1, [1, 2, 0])
        # image2 = np.transpose(image2, [1, 2, 0])
        # Convert the images to grayscale
        if image1.shape[2] < 3:
            gray1 = image1[:,:,0]  # Take only the first channel
        else:
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

        if image2.shape[2] < 3:
            gray2 = image2[:,:,0]  # Take only the first channel
        else:
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        # image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        # image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Compute the structural similarity index (SSIM) between the two images
        return ssim(gray1, gray2)


    def match_features(image1, image2, descriptor1, descriptor2, zscore_threshold=2):
        good_matches = [] # Initialize an empty list for good_matches
    
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptor1, descriptor2, k=2)

        # Calculate distances for all matches
        distances = [m.distance for m, n in matches]
        
        # Calculate mean and standard deviation of distances
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)
        
        # Define a threshold based on the Z-score
        z_score_threshold = zscore_threshold

        #mean_distance + z_score_threshold * std_distance
        
        # Filter matches based on the Z-score
        good_matches = [m for m, n in matches if m.distance < mean_distance + z_score_threshold * std_distance]
    
        return good_matches

    import cv2
    import numpy as np
    from scipy.stats import zscore
    from skimage.filters import gaussian

    def calculate_optical_flow(image1, image2, zscore_threshold=2.0, ssim_thresh=ssim_thresh):
        # Rasterio reads data as (bands, height, width)
        # OpenCV expects data as (height, width, channels)
        # So we need to transpose the data
        # image1 = np.transpose(image1, [1, 2, 0])
        # image2 = np.transpose(image2, [1, 2, 0])
        
        # Convert the images to grayscale

        if image1.shape[2] < 3:
            gray1 = image1[:,:,0]  # Take only the first channel
        else:
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

        if image2.shape[2] < 3:
            gray2 = image2[:,:,0]  # Take only the first channel
        else:
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Confirm that gray1 and gray2 are both 2D (grayscale) images of the same size
        assert gray1.ndim == 2, "gray1 is not a grayscale image"
        assert gray2.ndim == 2, "gray2 is not a grayscale image"
        assert gray1.shape == gray2.shape, "gray1 and gray2 are not the same size"
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    

        flowx=flow[..., 0]
        flowy=flow[..., 1]

        # Compute z-scores for the x_flow
        z_scores_x = zscore(flow[..., 0], axis=None)

        # Compute z-scores for the y_flow
        z_scores_y = zscore(flow[..., 1], axis=None)
        
        # Create a mask for vectors with a z-score less than the threshold
        mask_y = np.abs(z_scores_y) < zscore_threshold
        mask_x = np.abs(z_scores_x) < zscore_threshold
        
        # Zero out the vectors where the mask is False
        flowx[~mask_x] = 0
        flowy[~mask_x] = 0

        flowx[~mask_y] = 0
        flowy[~mask_y] = 0

        ssim=compare_images(image1, image2)
        
        flowx[ssim <ssim_thresh] = 0
        flowy[ssim <ssim_thresh] = 0


        # Compute the magnitude and angle of the 2D vectors
        magnitude, angle = cv2.cartToPolar(flowx, flowy)

        #     # Check if any pixel of flowx is negative
        if np.any(flowx < 0):
            magnitude *= np.sign(flowx)
        # negative_indices = np.where(flowx < 0)  # Find the indices where flowx is negative
        # magnitude[negative_indices] *= -1  # Set the corresponding pixels in magnitude to negative

       

        def compare_rasters(a, b, c):
            # Check if the input arrays have the same shape
            if a.shape != b.shape or a.shape != c.shape:
                raise ValueError("Input rasters must have the same shape.")

            # Iterate over each pixel
            for i in range(a.shape[0]):
                for j in range(a.shape[1]):
                    # Compare the pixel values
                    if a[i, j] < 0 and abs(a[i, j]) > b[i, j]:
                        c[i, j] = -1 * c[i, j]
            
            return c

        magnitude= compare_rasters(flowx, flowy, magnitude)


        return magnitude, flowx, flowy

    def filter_velocity(flow, good_matches, keypoints1, keypoints2):
        points1 = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 2)
        points2 = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 2)
        velocity = []
        for i in range(len(points1)):
            velocity.append(flow[int(points1[i][1]), int(points1[i][0])])
        return np.array(velocity), points1, points2

    def calculate_velocity_displacement(velocity, flowx, flowy, time_interval, conversion_factor):
        if time_interval == 0:
            raise ValueError("Time interval must not be zero.")
        velocity= velocity * conversion_factor/time_interval
        flowx = flowx * conversion_factor/time_interval
        flowy = flowy * conversion_factor/time_interval

        return velocity, flowx, flowy


    import re

    from mpl_toolkits.axes_grid1 import make_axes_locatable

    def separate_floats_letters(input_string):
        floats = re.findall(r'\d+\.\d+|\d+', input_string)
        letters = re.findall(r'[a-zA-Z]+', input_string)
        return letters, floats

    input_string = image_resolution
    unit, img_res = separate_floats_letters(input_string)

    import earthpy.plot as ep
    import earthpy.spatial as es
    import matplotlib.pyplot as plt
    import numpy as np
    # Import necessary packages
    import rasterio as rio
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    def calculate_hillshade(dem_file_path):
        # Open the raster data
        with rio.open(dem_file_path) as dem_src:
            dem = dem_src.read(1)

        # Calculate hillshade from the DEM
        hillshade = es.hillshade(dem)

        return hillshade

    

    def mask_raster(dem_array=None, mask_path=None, no_data_value=np.nan, scatter_x=None, scatter_y=None):
        """
        Mask a given raster (DEM) array using a binary mask and optionally filter scatter plot data 
        based on the same mask.

        Parameters:
        - dem_array (np.ndarray, optional): The 2D or 3D input raster array to be masked. If 3D, the last dimension 
                                is assumed to be the channel dimension (e.g., RGB).
        - mask_path (str): The path to the raster file containing the binary mask. Values of 1 in the mask 
                        represent areas to keep, and values of 0 represent areas to mask out.
        - no_data_value (scalar, optional): The value to replace the masked regions with in the `dem_array`. 
                                            Defaults to np.nan.
        - scatter_x (np.ndarray, optional): The x-coordinates of scatter plot data to be filtered based 
                                            on the mask. If provided, `scatter_y` must also be provided.
        - scatter_y (np.ndarray, optional): The y-coordinates of scatter plot data to be filtered based 
                                            on the mask. If provided, `scatter_x` must also be provided.

        Returns:
        - np.ndarray: The masked raster array. This array will be of the same shape and data type as 
                    the input `dem_array`.
        - (If scatter_x and scatter_y are provided)
        - np.ndarray: The x-coordinates of the scatter plot data after filtering with the mask.
        - np.ndarray: The y-coordinates of the scatter plot data after filtering with the mask.

        Note:
        If the `dem_array` data type is integer and the `no_data_value` is np.nan, the function will 
        replace NaN values with a default "no data" integer value (-9999) before casting back to the 
        original data type.
        """
        from scipy.ndimage import zoom
        # Read the binary mask
        with rasterio.open(mask_path, 'r') as mask_src:
            mask_array = mask_src.read(1)

        # If the shapes don't match and dem_array is provided, resize mask_array
        if dem_array is not None and dem_array.shape[:2] != mask_array.shape:
            y_scale = dem_array.shape[0] / mask_array.shape[0]
            x_scale = dem_array.shape[1] / mask_array.shape[1]
            mask_array = zoom(mask_array, (y_scale, x_scale))

        # Threshold mask_array
        mask_array = (mask_array >= 0.5).astype(np.int32)

        # Check if scatter_x and scatter_y are provided
        scatter_x_masked, scatter_y_masked = None, None
        if scatter_x is not None and scatter_y is not None:
            scatter_x = np.asarray(scatter_x)
            scatter_y = np.asarray(scatter_y)
            # Ensure scatter coordinates are within the bounds of the mask_array
            scatter_x_clipped = np.clip(scatter_x, 0, mask_array.shape[1]-1).astype(int)
            scatter_y_clipped = np.clip(scatter_y, 0, mask_array.shape[0]-1).astype(int)
            
            valid_indices = mask_array[scatter_y_clipped, scatter_x_clipped] == 1
            scatter_x_masked = scatter_x[valid_indices]
            scatter_y_masked = scatter_y[valid_indices]

        # If dem_array is provided, mask it
        masked_array = None
        if dem_array is not None:
            if dem_array.ndim == 2:
                masked_array = np.where(mask_array == 1, dem_array, no_data_value)
            else:
                masked_array = np.where(mask_array[:, :, np.newaxis] == 1, dem_array, no_data_value)

            # Handle casting to original data type
            original_dtype = dem_array.dtype
            if np.issubdtype(original_dtype, np.integer):
                int_no_data = -9999
                masked_array = np.where(np.isnan(masked_array), int_no_data, masked_array).astype(original_dtype)
            else:
                masked_array = masked_array.astype(original_dtype)

        if dem_array is not None and scatter_x is not None and scatter_y is not None:
            return masked_array, scatter_x_masked, scatter_y_masked
        elif dem_array is not None:
            return masked_array
        else:
            return scatter_x_masked, scatter_y_masked

    def plot_velocity_displacement(image1, image2, velocity, flowx, flowy, points1, points2, date1, date2, pdf_filename=None,
                                    time_interval=1, show_figure=False, unit='unit',
                                     s=10, bounds=[10,10,10,10], dem_file=dem_path):
        
        hillshade=calculate_hillshade(dem_file)
        #image1=image1.transpose([1, 2, 0])  
        # image size in pixels
        image_width = image1.shape[1]
        image_height = image1.shape[0]

        # image bounds in geographic coordinates
        geo_bounds = {
            'left': bounds[0],
            'right': bounds[1],
            'bottom': bounds[2],
            'top': bounds[3],
        }


        pixels = points1

       
        
        # convert pixel coordinates to geographic coordinates
        geo_coords = [(geo_bounds['left'] + (x / image_width) * (geo_bounds['right'] - geo_bounds['left']),
                    geo_bounds['top'] - (y / image_height) * (geo_bounds['top'] - geo_bounds['bottom'])) for x, y in pixels]

        # separate the coordinates for plotting
        lons, lats = zip(*geo_coords)

        

      
        def normalize(data, vmin=None, vmax=None ,cmap=None):
            import matplotlib.colors as mcolors
            import numpy as np

            # Check if data has any negative values
            if np.any(data < 0):
                # Calculate maximum absolute value of your data
                max_abs_value = np.max(np.abs(data))
                # Define the normalization range
                if vmin is None:
                    vmin = -max_abs_value
                if vmax is None:
                    vmax = max_abs_value
                # Use a diverging colormap
                if cmap is None:
                    cmap = 'RdBu_r'
                else:
                    cmap=cmap
            else:
                # Define the normalization range
                if vmin is None:
                    vmin = 0
                if vmax is None:
                    vmax = np.max(data)
                # Use a sequential colormap
                if cmap is None:
                    cmap = 'viridis'
                else:
                    cmap=cmap
               

            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
            return cmap, norm
       
        
        
        
        import cmocean


        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10), sharey=True)

        # Plot flowx
        #ep.plot_rgb(image1, ax=axes[0, 0], title=f'Disp-X({unit}) - {date1} to {date2}', extent=bounds)
        axes[0, 0].imshow(hillshade, cmap='gray', extent=bounds)
        minmax = np.max(np.abs(flowx))
        d=normalize(flowx, cmap='rainbow', vmin=-minmax, vmax=minmax)
        cmap, norm=d

        flowx_scatter = axes[0, 0].scatter(lons, lats, c=flowx, s=s, cmap=cmap, norm=norm)

        # Create colorbar for flowx
        flowx_colorbar_axes = make_axes_locatable(axes[0, 0]).append_axes("right", size="5%", pad=0.01)
        fig.colorbar(flowx_scatter, cax=flowx_colorbar_axes, orientation="vertical").set_label(unit, labelpad=0.5)
        axes[0,0].set_title(f'Disp-X({unit}) - {date1} to {date2}')
        # Plot flowy
        #ep.plot_rgb(image1, ax=axes[0, 1], extent=bounds, title=f'Disp-Y({unit}) - {date1} to {date2}')
        axes[0, 1].imshow(hillshade, cmap='gray', extent=bounds)
        minmax = np.max(np.abs(flowy))
        d=normalize(flowy, cmap='rainbow', vmin=-minmax, vmax=minmax)
        cmap, norm=d
        flowy_scatter = axes[0, 1].scatter(lons, lats, c=flowy, s=s, cmap= cmap, norm=norm)
        axes[0, 1].set_title(f'Disp-Y({unit}) - {date1} to {date2}')

        # Create colorbar for flowy
        flowy_colorbar_axes = make_axes_locatable(axes[0, 1]).append_axes("right", size="5%", pad=0.01)
        fig.colorbar(flowy_scatter, cax=flowy_colorbar_axes, orientation="vertical").set_label(unit, labelpad=0.5)

        # Plot Velocity Magnitude
        #ep.plot_rgb(image1, ax=axes[1, 0], extent=bounds, title=f'Velocity - {date1} to {date2}')
        axes[1, 0].imshow(hillshade, cmap='gray', extent=bounds)
        minmax = np.max(np.abs(velocity))
        min_v= np.nanmin(velocity)

        d=normalize(velocity, cmap='rainbow', vmin=min_v, vmax=minmax)
        cmap, norm=d
        velocity_scatter = axes[1, 0].scatter(lons, lats, c=velocity, s=s,  cmap=cmap, norm=norm)
        axes[1, 0].set_title(f'Velocity - {date1} to {date2}')
        # Create colorbar for velocity
        velocity_colorbar_axes = make_axes_locatable(axes[1, 0]).append_axes("right", size="5%", pad=0.01)
        fig.colorbar(velocity_scatter, cax=velocity_colorbar_axes, orientation="vertical").set_label(f'{(unit)}/{str(time_interval)}days', labelpad=0.5)

        # Plot Velocity Direction
        #ep.plot_rgb(image1, ax=axes[1, 1], extent=bounds, title=f'Velocity Direction - {date1} to {date2}')
        axes[1, 1].imshow(hillshade, cmap='gray', extent=bounds)
        velocity_direction = (360 - np.arctan2(flowy, flowx) * 180 / np.pi + 90) % 360
        
        d=normalize(velocity_direction, cmap=cmocean.cm.phase, vmin=0, vmax=360)
        cmap, norm=d
        velocity_direction_scatter = axes[1, 1].scatter(lons, lats, c=velocity_direction, s=s, cmap= cmap, norm=norm)
        axes[1, 1].set_title(f'Velocity Direction - {date1} to {date2}')

        # Create colorbar for velocity direction
        velocity_direction_colorbar_axes = make_axes_locatable(axes[1, 1]).append_axes("right", size="5%", pad=0.01)
        fig.colorbar(velocity_direction_scatter, cax=velocity_direction_colorbar_axes, orientation="vertical").set_label('degrees')
        

        # Set the extent of the axes
        axes[0, 0].set_xlim([bounds[0], bounds[1]])
        axes[0, 0].set_ylim([bounds[2], bounds[3]])
        axes[0, 1].set_xlim([bounds[0], bounds[1]])
        axes[0, 1].set_ylim([bounds[2], bounds[3]])
        axes[1, 0].set_xlim([bounds[0], bounds[1]])
        axes[1, 0].set_ylim([bounds[2], bounds[3]])
        axes[1, 1].set_xlim([bounds[0], bounds[1]])
        axes[1, 1].set_ylim([bounds[2], bounds[3]])

        if pdf_filename:
            plt.savefig(pdf_filename)
        
        if show_figure==False:
            plt.close()


    # def plot_velocity_displacement(image1, image2, velocity, flowx, flowy, points1, points2, date1, date2, pdf_filename=None, time_interval=1, show_figure=False, unit=unit, s=point_size):
    #     fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10), sharey=True)

    #     # Plot flowx
    #     axes[0, 0].imshow(image1, cmap='gray', origin='upper')
    #     flowx_min, flowx_max = np.percentile(flowx, [1, 99])
    #     flowx_abs_max = max(abs(flowx_min), abs(flowx_max))
    #     flowx_scatter = axes[0, 0].scatter(x=points1[:, 0], y=points1[:, 1], c=flowx, s=s, cmap='RdBu', vmin=-flowx_abs_max, vmax=flowx_abs_max)
    #     axes[0, 0].set_title(f'Disp-X({unit}) - {date1} to {date2}')

    #     # Create colorbar for flowx
    #     flowx_colorbar_axes = make_axes_locatable(axes[0, 0]).append_axes("right", size="5%", pad=0.01)
    #     fig.colorbar(flowx_scatter, cax=flowx_colorbar_axes, orientation="vertical").set_label(unit, labelpad=0.5)

    #     # Plot flowy
    #     axes[0, 1].imshow(image1, cmap='gray', origin='upper')
    #     flowy_min, flowy_max = np.percentile(flowy, [1, 99])
    #     flowy_abs_max = max(abs(flowy_min), abs(flowy_max))
    #     flowy_scatter = axes[0, 1].scatter(points1[:, 0], points1[:, 1], c=flowy, s=s, cmap='RdBu', vmin=-flowy_abs_max, vmax=flowy_abs_max)
    #     axes[0, 1].set_title(f'Disp-Y({unit}) - {date1} to {date2}')

    #     # Create colorbar for flowy
    #     flowy_colorbar_axes = make_axes_locatable(axes[0, 1]).append_axes("right", size="5%", pad=0.01)
    #     fig.colorbar(flowy_scatter, cax=flowy_colorbar_axes, orientation="vertical").set_label(unit, labelpad=0.5)

    #     # Plot Velocity Magnitude
    #     axes[1, 0].imshow(image1, cmap='gray', origin='upper')
    #     velocity_min, velocity_max = np.percentile(velocity, [1, 99])
    #     velocity_scatter = axes[1, 0].scatter(points1[:, 0], points1[:, 1], c=velocity, s=s, cmap='plasma', vmin=velocity_min, vmax=velocity_max)
    #     axes[1, 0].set_title(f'Velocity - {date1} to {date2}')

    #     # Create colorbar for velocity
    #     velocity_colorbar_axes = make_axes_locatable(axes[1, 0]).append_axes("right", size="5%", pad=0.01)
    #     fig.colorbar(velocity_scatter, cax=velocity_colorbar_axes, orientation="vertical").set_label(f'{(unit)}/{str(time_interval)}days', labelpad=0.5)

    #     # Plot Velocity Direction
    #     axes[1, 1].imshow(image1, cmap='gray', origin='upper')
    #     velocity_direction = (360 - np.arctan2(flowy, flowx) * 180 / np.pi + 90) % 360
    #     velocity_direction_min, velocity_direction_max = np.percentile(velocity_direction, [1, 99])
    #     velocity_direction_scatter = axes[1, 1].scatter(points1[:, 0], points1[:, 1], c=velocity_direction, s=s, cmap='hsv', vmin=velocity_direction_min, vmax=velocity_direction_max)
    #     axes[1, 1].set_title(f'Velocity Direction - {date1} to {date2}')

    #     # Create colorbar for velocity direction
    #     velocity_direction_colorbar_axes = make_axes_locatable(axes[1, 1]).append_axes("right", size="5%", pad=0.01)
    #     fig.colorbar(velocity_direction_scatter, cax=velocity_direction_colorbar_axes, orientation="vertical").set_label('degrees')
        
    #     if pdf_filename:
    #         plt.savefig(pdf_filename)
        
    #     if show_figure==False:
    #         plt.close()

        flowx_scatter=flowx_scatter.get_offsets()
        x_data = flowx_scatter[:, 0]
        y_data = flowx_scatter[:, 1]

        

        return pixels[:, 0], pixels[:, 1]

    def extract_date_from_filename(filename):
        try:
            # Searching for a date in the format 'YYYY-MM-DD' or 'YYYYMMDD'
            match = re.search(r'(\d{4}-\d{2}-\d{2})|(\d{8})', filename)
            if match is not None:
                date_str = match.group()
                # Determine the date format
                date_format = '%Y%m%d' if '-' not in date_str else '%Y-%m-%d'
                # Parse the date string
                date_obj = datetime.strptime(date_str, date_format).date()
                return date_obj.strftime('%Y-%m-%d')
            else:
                print("No date string found in filename.")
                return None
        except ValueError:
            print(f"Date string '{date_str}' in filename is not in expected format.")
            return None



    def mean_of_arrays(array1, array2):
        # Determine the size of the larger array
        max_size = max(array1.shape, array2.shape)

        # Use np.pad to extend the smaller array with zeros
        array1 = np.pad(array1, (0, max_size[0] - array1.shape[0]))
        array2 = np.pad(array2, (0, max_size[0] - array2.shape[0]))

        # Compute the mean of the two arrays element-wise
        mean_array = np.nanmean([array1, array2], axis=0)

        return mean_array

    

    import geopandas as gpd
    import numpy as np
    import rasterio
    from rasterio.features import geometry_mask
    from rasterio.transform import from_origin
    from scipy.interpolate import griddata
    from scipy.spatial import cKDTree

    def replace_nan_with_nearest(x, y, z, width, height):
        try:
            # Create a 2D grid of coordinates based on the x, y values
            xi = np.linspace(np.nanmin(x), np.nanmax(x), width)
            yi = np.linspace(np.nanmin(y), np.nanmax(y), height)
            xi, yi = np.meshgrid(xi, yi)

            # Flatten the coordinates grid and build a KDTree
            flattened_coordinates = np.column_stack((xi.ravel(), yi.ravel()))
            tree = cKDTree(flattened_coordinates)

            # Query the tree for nearest neighbors to each point in x, y
            _, indices = tree.query(np.column_stack((x, y)))

            # Replace NaNs with z values at these indices
            zi = np.full_like(xi, np.nan)
            np.put(zi, indices, z)

            return zi

        except Exception as e:
            print("An error occurred:", str(e))
            return None


    

    

    def save_xyz_as_geotiff(x, y, z, filename, reference_raster, shapefile=None, interpolate=None, 
    smoothing_kernel_size=smoothing_kernel_size, Vegetation_mask=Vegetation_mask):
        try:
            # Get the CRS, width, height, and transform from the reference raster
            with rasterio.open(reference_raster) as src:
                crs = src.crs
                width = src.width
                height = src.height
                transform = src.transform
                bounds = src.bounds
                x_min = bounds.left
                x_max = bounds.right
                y_min = bounds.bottom
                y_max = bounds.top
                pixel_size_x = src.res[0]
                pixel_size_y = src.res[1]



            # Create a 2D grid of coordinates based on the x, y values
            xi = np.linspace(np.min(x), np.max(x), width)
            yi = np.linspace(np.min(y), np.max(y), height)
            xi, yi = np.meshgrid(xi, yi)

            # Create an array of the same size as the x, y grid filled with NaN
            zi = np.full_like(xi, np.nan)

            
                

            if interpolate is not None:
                # Interpolate z values onto the new grid
                zi = griddata((x, y), z, (xi, yi), method=interpolate, rescale=True)

                # Replace interpolated values outside the range with mean of initial z values
                z_min = np.min(z)
                z_max = np.max(z)
                zi[zi < z_min] = np.mean(z)
                zi[zi > z_max] = np.mean(z)

                # Find the indices of interpolated points exceeding the data range
                out_of_range_indices = np.logical_or(xi < np.min(x), xi > np.max(x)) | np.logical_or(yi < np.min(y), yi > np.max(y))

                # Replace out-of-range interpolated points with the mean of valid data points
                zi_valid = zi[~out_of_range_indices]
                mean_valid = np.nanmean(zi_valid)
                zi = np.where(out_of_range_indices, mean_valid, zi)
            else:
                zi=replace_nan_with_nearest(x, y, z, width, height)
            
             # Apply low-pass filter
            if smoothing_kernel_size is not None:
                zi = gaussian(zi, sigma=smoothing_kernel_size )  # Adjust sigma according to your desired smoothing strength

            if shapefile is not None:
                # Load shapefile, convert it to the correct CRS and get its geometry
                gdf = gpd.read_file(shapefile).to_crs(crs)
                shapes = gdf.geometry.values

                # Generate a mask from the shapes
                mask = geometry_mask(shapes, transform=transform, out_shape=zi.shape, invert=False, all_touched=True)

                # Apply the mask to the interpolated data
                zi = np.where(mask, np.nan, zi)

                if Vegetation_mask is not None:
                    zi=mask_raster(zi, Vegetation_mask )


            # Define the profile
            profile = {
                'driver': 'GTiff',
                'height': height,
                'width': width,
                'count': 1,
                'dtype': zi.dtype,
                'crs': crs,
                'transform': transform,
                'nodata': np.nan,  # specify the nodata value
            }

            # Write to a new .tif file
            with rasterio.open(filename + ".tif", 'w', **profile) as dst:
                dst.write(zi, 1)

        except Exception as e:
            print("An error occurred while creating the GeoTIFF:")
            print(e)

    import os

    import numpy as np
    import rasterio
    from rasterio.windows import from_bounds
    from shapely.geometry import box

    def crop_to_overlap(folder_path):
        image_files = sorted(os.listdir(folder_path))
        valid_extensions = ['.tif', '.jpg', '.png', '.bmp', '.tiff']
        image_path_list=[]
        bound_list=[]

        # Calculate mutual overlap
        overlap_box = None
        for file in image_files:
            if os.path.splitext(file)[1] in valid_extensions:
                image_path = os.path.join(folder_path, file)
                image_path_list.append(image_path)
                with rasterio.open(image_path) as src:
                    bounds = src.bounds
                    bound_list.append(bounds)
                    image_box = box(*bounds)
                    if overlap_box is None:
                        overlap_box = image_box
                    else:
                        overlap_box = overlap_box.intersection(image_box)

        # Read images and crop to mutual overlap
        cropped_images = []
        keypoints=[]
        descriptors=[]
        for image_path in image_path_list:
            with rasterio.open(image_path) as src:
                overlap_window = from_bounds(*overlap_box.bounds, transform=src.transform)
                cropped_image = src.read(window=overlap_window)
                 # Rasterio reads data as (bands, height, width)
                #OpenCV expects data as (height, width, channels)
                #So we need to transpose the data
                cropped_image = np.transpose(cropped_image, [1, 2, 0])
                cropped_images.append(cropped_image)
                kp, des = detect_keypoints(cropped_image)
                keypoints.append(kp)
                descriptors.append(des)
                

        #print("Cropped {} images.".format(len(cropped_images)))
        return cropped_images, bound_list, keypoints, descriptors, image_path_list


# Usage example:
#cropped_images, bound_list = crop_to_overlap('2023/crop_demo/')



       


        

    import os
    from datetime import datetime

    import numpy as np
    import rasterio
    from tqdm import tqdm
    

    def feature_matching(folder_path=input_dir, output_dir=output_dir, zscore_threshold=zscore_threshold, 
    AOI=AOI, conversion_factor=float(img_res[0]), ssim_thresh=ssim_thresh, Vegetation_mask=Vegetation_mask):
        
        folder_path = folder_path
        
        images, bound_list, keypoints, descriptors, image_path_list = crop_to_overlap(folder_path)
        image_files = [filename for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]

        image_files = sorted(image_files)

        #image_files = sorted(os.listdir(folder_path))
        # images = []
        # keypoints = []
        # descriptors = []
        # bound_list=[]
        # # List of valid extensions
        # valid_extensions = ['.tif', '.jpg', '.png', '.bmp']
        # image_path_list=[]
        # for file in image_files :
        #     if os.path.splitext(file)[1] in valid_extensions:
        #         image_path = os.path.join(folder_path,file)
        #         image_path_list.append(image_path)
        #         with rasterio.open(image_path) as src:
        #             image = np.dstack([src.read(i) for i in src.indexes])  # This line stacks the bands of the image
        #             bounds=src.bounds
        #             bound_list.append(bounds)
        #             #image=src.read(1)
        #         images.append(image)
        #         kp, des = detect_keypoints(image)
        #         keypoints.append(kp)
        #         descriptors.append(des)


        
        ######################
        mean_vel_list=[]
        mean_flowx_list=[]
        mean_flowy_list=[]
        pointx_list=[]
        pointsy_list=[]
        dates_names_list=[]

        lf=0

        if Vegetation_mask is not None:
            from scipy.ndimage import zoom
            mask_file=rasterio.open(Vegetation_mask)
            mask_data=mask_file.read(1)
            # Ensure mask_data is boolean (0 or 1)
            
        
        for i in tqdm(range(0, len(images)-2), desc="Processing"):
            bound=bound_list[i]
            image1 = images[i]
            image2 = images[i + 1]
            image3=images[i + 2]
            keypoints1 = keypoints[i]
            keypoints2 = keypoints[i + 1]
            keypoints3 = keypoints[i + 2]
            descriptors1 = descriptors[i]
            descriptors2 = descriptors[i + 1]
            descriptors3 = descriptors[i + 2]

            if Vegetation_mask is not None:
                # If the shapes don't match and dem_array is provided, resize mask_array
                if image1 is not None and image1.shape[:2] != mask_data.shape:
                    y_scale = image1.shape[0] / mask_data.shape[0]
                    x_scale = image1.shape[1] / mask_data.shape[1]
                    mask_data = zoom(mask_data, (y_scale, x_scale))

                    # Threshold mask_array
                    mask_data = (mask_data >= 0.5).astype(np.int32)
                    mask_data = mask_data.astype(bool)
                
                # Apply the mask for each band using broadcasting
                image1[~mask_data, :] = 0
                image2[~mask_data, :] = 0
                image3[~mask_data, :] = 0

                # plt.imshow(image1)
                # plt.show()



            # descriptors1 and descriptors2 are assumed to be numpy arrays
            descriptors12 = np.concatenate((descriptors1, descriptors2), axis=0)
            descriptors13 = np.concatenate((descriptors1, descriptors3), axis=0)

            keypoints12 = np.concatenate((keypoints1, keypoints2), axis=0)
            keypoints13 = np.concatenate((keypoints1, keypoints3), axis=0)

            good_matches12 = match_features(image1, image2, descriptors12, descriptors13)
            good_matches13 = match_features(image1, image3, descriptors12, descriptors13)

            flow12, flowx12, flowy12 = calculate_optical_flow(image1, image2, zscore_threshold=zscore_threshold, ssim_thresh=ssim_thresh)
            flow13, flowx13, flowy13 = calculate_optical_flow(image1, image3, zscore_threshold=zscore_threshold, ssim_thresh=ssim_thresh)

            flow=mean_of_arrays(flow12, flow13)
            flowx=mean_of_arrays(flowx12, flowx13)
            flowy=mean_of_arrays(flowy12,flowy13)

            vel, points1_i, points2 = filter_velocity(flow, good_matches12, keypoints12, keypoints13)
            flowx, points1_i, points2 = filter_velocity(flowx, good_matches12, keypoints12, keypoints13)
            flowy, points1_i, points2 = filter_velocity(flowy, good_matches12, keypoints12, keypoints13)
            
            # vel13, points1, points3 = filter_velocity(flow13, good_matches13, keypoints12, keypoints13)
            # flowx13, points1, points3 = filter_velocity(flowx13, good_matches13, keypoints12, keypoints13)
            # flowy13, points1, points3 = filter_velocity(flowy13, good_matches13, keypoints12, keypoints13)

            # points12 = np.concatenate((points1_i[:,0], points2[:,1]), axis=0)
            # points13 = np.concatenate((points1[:,0], points3[:,1]), axis=0)

            # print(points12.shape)
            # print(points13.shape)

            #Extract All dates to List for Later use
            
            date1 = (extract_date_from_filename(image_files[lf])).replace("-", "")
            date2 = (extract_date_from_filename(image_files[lf + 1])).replace("-", "")
            date3= (extract_date_from_filename(image_files[lf + 2])).replace("-", "")
            lf=lf+1

            time_interval_1_2 = (datetime.strptime(date2, '%Y%m%d') - datetime.strptime(date1, '%Y%m%d')).days
            time_interval_1_3 = (datetime.strptime(date3, '%Y%m%d') - datetime.strptime(date1, '%Y%m%d')).days
            if time_interval_1_2 == 0:
                print(f"Skipping computation for {date1} to {date2} as the time interval is zero.")
                continue  # Skip the rest of this loop iteration
        
            
            conversion_factor = float(img_res[0])  # 1 pixel = 0.1 centimeter, meter, or mm etc..

        
            vel, flowx, flowy = calculate_velocity_displacement(vel, flowx, flowy , time_interval_1_3, conversion_factor)

            mean_vel_list.append(vel)
            mean_flowx_list.append(flowx)
            mean_flowy_list.append(flowy)
            pointx_list.append(points1_i)
            pointsy_list.append(points2)

            X_folder=output_dir+"/flowx/"
            Y_folder=output_dir+"/flowy/"
            VEL_folder=output_dir+"/vel/"
            plot_folder=output_dir+"/plots/"

            os.makedirs(X_folder) if not os.path.exists(X_folder) else None
            os.makedirs(Y_folder) if not os.path.exists(Y_folder) else None
            os.makedirs(VEL_folder) if not os.path.exists(VEL_folder) else None
            os.makedirs(plot_folder) if not os.path.exists(plot_folder) else None

            file_name_x=X_folder+ str(date1)+"_" + str(date2)+ "_" + str(date3)
            file_name_y=Y_folder+ str(date1) + "_" + str(date2)+ "_" +str(date3)
            file_name_vel=VEL_folder+ str(date1)+ "_" + str(date2)+ "_" +str(date3)
            plot_name=plot_folder+ str(date1)+"_" + str(date2)+ "_" + str(date3)

            dates_names_list.append(str(date1) + "_" + str(date2)+ "_" + str(date3))
        
            x, y= plot_velocity_displacement(image1, image3, vel, flowx, flowy, points1_i, points2, date1, date3, pdf_filename=plot_name, time_interval=time_interval_1_3 , 
                                             show_figure=show_figure, unit=unit[0], s=point_size,
                                               bounds=[bound.left, bound.right, bound.bottom, bound.top])
            
            # if Vegetation_mask is not None:
            #     x, y= mask_raster(dem_array=None, mask_path=Vegetation_mask, no_data_value=np.nan,scatter_x=x, scatter_y=y)
                
            #     flowx, flowy= mask_raster(dem_array=None, mask_path=Vegetation_mask, no_data_value=np.nan, scatter_x=flowx, 
            #     scatter_y=flowy)

            #     vel, flowy= mask_raster(dem_array=None, mask_path=Vegetation_mask, no_data_value=np.nan, scatter_x=vel, 
            #     scatter_y=flowy)
                

                

            save_xyz_as_geotiff(x, y, flowx, file_name_x, dem_path, AOI, interpolate=interpolate )
            save_xyz_as_geotiff(x, y, flowy, file_name_y, dem_path, AOI, interpolate=interpolate )
            save_xyz_as_geotiff(x, y, vel, file_name_vel, dem_path, AOI , interpolate=interpolate)


        
        dates_list=[extract_date_from_filename(filename) for filename in image_files]
        # Filter image_files based on extensions and extract dates
        # image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']
        # dates_list = [extract_date_from_filename(filename) for filename in image_files if os.path.splitext(filename)[1].lower() in image_extensions]
            
        Total_days = (datetime.strptime(extract_date_from_filename(image_files[len(image_files)-1]), '%Y-%m-%d') - datetime.strptime(extract_date_from_filename(image_files[0]), '%Y-%m-%d')).days
            
        
        print(f'Total Days: {Total_days}')
        with open(output_dir+"/Names.txt", "w") as file:
            file.write('\n'.join(dates_names_list))
        #print(f'Dates: {dates_list}')

    #     data=[dates_list,pointx_list, pointsy_list, mean_flowx_list, mean_flowy_list,mean_vel_list ]
    #    # Create DataFrame
    #     df = pd.DataFrame(data, columns=column_names)

        
        
        return image1, image3, mean_vel_list, mean_flowx_list, mean_flowy_list, points1_i, points2, dates_list[0], dates_list[len(dates_list)-1]

    feature_matching(folder_path=input_dir, output_dir=output_dir, zscore_threshold=zscore_threshold, AOI=AOI, conversion_factor=float(img_res[0]), ssim_thresh=ssim_thresh)

    
