
def Time_Series(stacked_raster_EW=r"", stacked_raster_NS=r"", velocity_points=r"", dates_name=r"", output_folder="", outputFilename="",
                 std=1, VEL_Scale='year' , velocity_mode="mean", master_reference=False):
    
    '''
    This program uses candiate velocity points from stackprep function and performs linear interpolation in time-domain to calibrate
    stacked velocity. Additionally produces corrected timeseries velocity(daily) in a shapefile.
    
    Parameters
    ----------
    b   
    stacked_raster_EW: str
    
    stacked_raster_NS: str
    
    velocity_points: str 
        Velcity Candidate points
    
    dates_name: str
        text file include name of each date in format YYYYMMDD
    
    output_folder: str
    
    outputFilename: str
    
    VEL_Scale: str
        'year' , "month" or empty  to calculate velocity within provided dataset date range
    
    velocity_mode: str
        "mean" or "linear"
        
    master_reference: bool
        True if calculate TS to a single reference date, False if calculate TS to subsequent Reference dates
    
    Returns
    -------
    
    Time-series shape file of velocity and direction EW, NS, and 2D(resultant Velocity and direction)
    
    '''
    import glob
    import os
    from datetime import datetime
    from os.path import join

    import dask.dataframe as dd
    import geopandas as gpd
    import geowombat as gw
    import numpy as np
    import pandas as pd
    import scipy.stats as stats
    from dateutil import parser 
    
    
    def Helper_Time_Series(stacked_raster=r"", velocity_points=r"", dates_name=r"", output_folder="", outputFilename="", std=1 , VEL_Scale=VEL_Scale):
        
        '''
        stacked_raster: Path to raster stack .tif file
        
        velocity_points: Path to velocity points in arcmap shapfile format .shp
        
        dates_name: path to text file contains date names of each time series triplets .txt
        
        output_folder: Path to output Folder
        
        outputFilename: name for out time-series velocity shapefile
        '''
        
        
        
        if not os.path.exists(output_folder):
                os.makedirs(output_folder)
    
        
        #Open Raster stack, extract pixel info into shape file

        with gw.open(stacked_raster, stack_dim='time') as src:
            print(src)
            #df = src.gw.extract(velocity_points)
            df = src.gw.extract(velocity_points, use_client=True , dtype='float32')
            df[df.select_dtypes(np.float64).columns] = df.select_dtypes(np.float64).astype(np.float32)

        

        #Import names to label timeseries data    
        names = []
        dnames=[]
        with open(dates_name, 'r') as fp:
            for line in fp:
                # remove linebreak from a current name
                # linebreak is the last character of each line
                x = 'D'+ line[:-1]

                # add current item to the list
                names.append(x)
                dnames.append(x[:-18])

        print (len(dnames))
        print(len(df.columns))

        cci=(len(df.columns)- len(dnames))
        df2=df.iloc[:, cci:]
        cc=np.arange(1,cci)
        #Add Timesereises column names
        
        # #find outliers using z-score iter 1
        # lim = np.abs((df2[cc] - df2[cc].mean(axis=1)) / df2[cc].std(ddof=0, axis=1)) < std
        
        # # # # replace outliers with nan
        # df2[cc]= df2[cc].where(lim, np.nan)
        
        
        
        # df2[cc] = df2[cc].astype(float).apply(lambda x: x.interpolate(method='linear', limit_direction='both'), axis=1).ffill().bfill()
       
        
        # df2=df2.T
        
        # #find outliers using z-score iter 2
        # lim = np.abs((df2 - df2.mean(axis=0)) / df2.std(ddof=0,axis=0)) < std
        # #lim=df2.apply(stats.zscore, axis=1) <1
        # # # # replace outliers with nan
        # df2= df2.where(lim, np.nan)
        
        # df2= df2.astype(float).apply(lambda x: x.interpolate(method='linear', limit_direction='both'), axis=0).ffill().bfill()
        
        # for col in df2.columns:
        #     #print (col)
        #     #df2[col]=pd.to_numeric(df2[col])
        #     df2[col]= df2[col].interpolate(method='index', axis=0).ffill().bfill()
        
        # df2=df2.T
            
           
        #Add Timesereises column names
        df2.columns = dnames
        
        df2 = dd.from_pandas(df2, npartitions=10)
        
        
        # define a function to replace outliers with NaN using z-scores along each row
        def replace_outliers(row, stdd=std):
            zscores = (row - row.mean()) / row.std()
            row[abs(zscores) > stdd] = np.nan
            return row

        # apply the function to each row using apply
        df2 = df2.apply(replace_outliers, axis=1)
        
        #df2=df2.compute()
        
        # Select columns with 'float64' dtype  
        #float64_cols = list(df2.select_dtypes(include='float64'))

        # The same code again calling the columns
        df2[dnames] = df2[dnames].astype('float32')
        
        
        
        df2[dnames] = df2[dnames].apply(lambda x: x.interpolate(method='linear', limit_direction='both'), axis=1).ffill().bfill()
        
        df2=df2.compute()
        
        df2=df2.T
        for col in df2.columns:
            #print (col)
            #df2[col]=pd.to_numeric(df2[col])
            df2[col]= df2[col].interpolate(method='index', axis=0).ffill().bfill()
        
        df2=df2.T
        
        df2.columns = dnames
        
        
        

        # # interpolate missing values along each row
        # df2.interpolate(axis=1, limit_direction='both', limit_area='inside', method='linear', inplace=True)
                
        #  # Forward fill the DataFrame
        # df2.ffill(inplace=True)

        # # Backward fill the DataFrame
        # df2.bfill(inplace=True)
        
        #Calculate Linear Velocity for each data point
        def linear_VEL(df, dnames):
            
            # def best_fit_slope_and_intercept(xs,ys):
            #     from statistics import mean
            #     xs = np.array(xs, dtype=np.float64)
            #     ys = np.array(ys, dtype=np.float64)
            #     m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
            #         ((mean(xs)*mean(xs)) - mean(xs*xs)))
                
            #     b = mean(ys) - m*mean(xs)
                
            #     return m, b
            dd_list=[x.replace("D", "") for x in dnames]
            dates_list=([datetime.strptime(x, '%Y%m%d') for x in dd_list])
            days_num=[( ((x) - (pd.Timestamp(year=x.year, month=1, day=1))).days + 1) for x in dates_list]
            days_num=list(range(0, len(dnames)))
            dslope=[]
            std_slope=[]
            for index, dr in df.iterrows():
                #if index==0:
                rows=df.loc[index, :].values.flatten().tolist()
                row_values=rows
                # dfr = pd.DataFrame(dr).transpose()
                # dfr = dfr.loc[:, ~dfr.columns.str.contains('^Unnamed')]
            
                #slopeVEL=best_fit_slope_and_intercept(days_num, row_values)
                #print("slope", slopeVEL[0])
                slope, intercept, r_value, p_value, std_err = stats.linregress(days_num, row_values)
                dslope.append(slope)
                std_slope.append(std_err)
            return dslope, std_slope
        
        
        
        
            
        
        ###########################################################################
  
        
        dnames_new=[x.replace("D", "") for x in dnames]
        def input_dates(start_date="YYYYMMDD", end_date="YYYYMMDD"):
            start_date1=parser.parse(start_date)
            end_date2=parser.parse(end_date)
            date_list_start=[]
            date_list_end=[]
            for idx, item in enumerate(dnames_new):
                #filepath1, img_name = os.path.split(item) 
                str_date1=item
                str_date2=dnames_new[len(dnames_new)-1]
                #input start date
                date_time1 = parser.parse(str_date1)
                date_list_start.append(date_time1)
                #input end date
                date_time2 = parser.parse(str_date2)
                date_list_end.append(date_time2)
            st_date=min(date_list_start, key=lambda d: abs(d - start_date1))
            text_date1=st_date.strftime("%Y%m%d")
            End_date=min(date_list_end, key=lambda d: abs(d - end_date2))
            No_ofDays=(End_date-st_date).days
            
            text_date2=End_date.strftime("%Y%m%d")
            return [text_date1, text_date2, No_ofDays]

        velocity_scale=(input_dates(start_date=dnames_new[0], end_date=dnames_new[len(dnames_new)-1]))
        
        #################################
        # for idx, row in df2[dnames].iterrows():
        #     lim = np.abs((row[dnames] - df2[dnames]()) / row[dnames].std(ddof=0)) < 1
        #     row[dnames]= row[dnames].where(lim, np.nan)
        #     row[dnames] = row[dnames].astype(float).apply(lambda x: x.interpolate(method='linear', limit_direction='both'), axis=1).ffill().bfill()
            
        
        print (df2.describe())
        temp_df=pd.DataFrame()
        temp_df[dnames[0]]=df2[dnames[0]]
        #Choosing first date as reference for Time Series
        
        if master_reference==True:
            
            df2 = df2.sub(df2[dnames[0]], axis=0)
        else:
            
            df2=df2.diff(axis = 1, periods = 1)
        # count=0
        # for idx, col in enumerate(df2.columns):
        #     df2[col] = df2[col].sub(df2[dnames[count]], axis=0)
        #     count=count+1
            
       
        df2[dnames[0]]=0
            
        linear_velocity=linear_VEL(df2[dnames], dnames)
        out=df2
        if velocity_mode=="mean":
            out['VEL']=out[dnames].mean(axis=1)
            out['VEL_STD']=out[dnames].std(axis=1)
        elif velocity_mode=="linear":
            out['VEL']=linear_velocity[0]
            out['VEL_STD']=linear_velocity[1]
        if VEL_Scale=="month": 
            out['VEL']=out['VEL']/velocity_scale[2] * 30  #velocity_scale[2] is number of days
            out['VEL_STD']=out['VEL_STD'] /velocity_scale[2] *30
        elif VEL_Scale=="year":
            out['VEL']=out['VEL']/velocity_scale[2] * 365
            out['VEL_STD']=out['VEL_STD']/velocity_scale[2] * 365
        else:
            out['VEL']=out['VEL']
            out['VEL_STD']=out['VEL_STD']
               
        
            
        out['geometry']=df['geometry']
        out['CODE']=df['SiteID']
        #out[dnames[0]]=temp_df[dnames[0]]
        # out['HEIGHT']=0
        # out['H_STDEV']=0
        #out['V_STDEV']=out[dnames].std(axis=1)
        #out['COHERENCE']=0
        #out['H_STDEF']=0
        out['x']=df['x']
        out['y']=df['y']

        col_titles=['CODE','geometry','x', 'y', 'VEL', 'VEL_STD' ]+dnames
        out = out.reindex(columns=col_titles)
        
        

        geo_out=gpd.GeoDataFrame(out, geometry='geometry', crs=df.crs)

        geo_out.to_file(output_folder +"/" + outputFilename)
        (geo_out)

        return geo_out, dnames, linear_VEL
    
    if output_folder=="":
            output_folder= "stack_data/TS"
            
    
    if not os.path.exists(output_folder):
                os.makedirs(output_folder)
    if outputFilename=="":
            outputFilename= "TS_2D_"+ os.path.basename(velocity_points)
            
            
            
    EW=Helper_Time_Series(stacked_raster=stacked_raster_EW, velocity_points=velocity_points ,
                             dates_name=dates_name, output_folder=output_folder, outputFilename="TS_EW_"+ os.path.basename(velocity_points), std=std, VEL_Scale=VEL_Scale)
                             
    NS=Helper_Time_Series(stacked_raster=stacked_raster_NS, velocity_points=velocity_points, 
                             dates_name=dates_name, output_folder=output_folder, outputFilename="TS_NS_"+ os.path.basename(velocity_points), std=std, VEL_Scale=VEL_Scale)
    
    if not os.path.exists(output_folder):
                os.makedirs(output_folder)
    if outputFilename=="":
            outputFilename= "TS_2D_"+ os.path.basename(velocity_points)
            
            
    gdf_ew=EW[0]
    gdf_ns=NS[0]
    dnames=NS[1]
    df_2D_VEL=pd.DataFrame()
    df_2D_VEL['CODE']=gdf_ew['CODE']
    df_2D_VEL['geometry']=gdf_ew['geometry']
    df_2D_VEL['x']=gdf_ew['x']
    df_2D_VEL['y']=gdf_ew['y']
    
   
   #Calculate resultant velocity magnitude
    for col in gdf_ew[dnames].columns:
       
        df_2D_VEL[col]=np.hypot(gdf_ns[col],gdf_ew[col])
       
    df_2D_VEL['VEL_MEAN']=df_2D_VEL[dnames].mean(axis=1)
    df_2D_VEL['V_STDEV']=df_2D_VEL[dnames].std(axis=1)
    #we call linear velocity function from above then reuse it below to replace VEL_2D Mean an STD below for lines
    # linear_2D_Velocity_function=EW[2]
    # linear_2D_Velocity=linear_2D_Velocity_function(df_2D_VEL[dnames], dnames)
    # df_2D_VEL['VEL']=linear_2D_Velocity[0]
    # df_2D_VEL['V_STDEV']=linear_2D_Velocity[1]
    #############################
    col_titles=['CODE','geometry','x', 'y', 'VEL_MEAN' , 'V_STDEV' ]+ dnames 
    df_2D_VEL = df_2D_VEL.reindex(columns=col_titles)
    gdf_2D_VEL=gpd.GeoDataFrame(df_2D_VEL, geometry='geometry', crs=gdf_ew.crs)
    
    
    
    gdf_2D_VEL.to_file(output_folder +"/" + outputFilename)
    
    
    #Calculate resultant velocity direction
    
    dir_df_2D_VEL=pd.DataFrame()
    dir_df_2D_VEL['CODE']=gdf_ew['CODE']
    dir_df_2D_VEL['geometry']=gdf_ew['geometry']
    dir_df_2D_VEL['x']=gdf_ew['x']
    dir_df_2D_VEL['y']=gdf_ew['y']
    
    newcol_dir_list=[]
    for col in gdf_ew[dnames].columns:
        newcol_dir= col
        newcol_dir_list.append(newcol_dir)
        dir_df_2D_VEL[newcol_dir]=np.arctan2(gdf_ns[col],gdf_ew[col])
        dir_df_2D_VEL[newcol_dir]=np.degrees(dir_df_2D_VEL[newcol_dir])
        dir_df_2D_VEL[newcol_dir]=(450-dir_df_2D_VEL[newcol_dir]) % 360
    dir_df_2D_VEL['VELDir_MEAN']=dir_df_2D_VEL[newcol_dir_list].mean(axis=1)
    col_titles=['CODE','geometry','x', 'y', 'VELDir_MEAN'  ]+ newcol_dir_list
    dir_df_2D_VEL = dir_df_2D_VEL.reindex(columns=col_titles)
    dir_gdf_2D_VEL=gpd.GeoDataFrame(dir_df_2D_VEL, geometry='geometry', crs=gdf_ew.crs)
    
    dir_gdf_2D_VEL.to_file(output_folder +"/" + outputFilename[:-4]+"_dir.shp")
    
    #Calcuate Mean Corrected velocity products MEAN X, Y, 2D and Dir
    corrected_mean_products=pd.DataFrame()
    corrected_mean_products['CODE']=gdf_ew['CODE']
    corrected_mean_products['geometry']=gdf_ew['geometry']
    corrected_mean_products['x']=gdf_ew['x']
    corrected_mean_products['y']=gdf_ew['y']
    corrected_mean_products['VEL_E']=gdf_ew['VEL']
    corrected_mean_products['VEL_N']=gdf_ns['VEL']
    #corrected_mean_products['VEL_2D']=df_2D_VEL['VEL_MEAN']
    corrected_mean_products['VEL_2D']=df_2D_VEL['VEL_MEAN']
    corrected_mean_products['2DV_STDEV']=df_2D_VEL['V_STDEV']
    corrected_mean_products['VEL_2DDir']=dir_df_2D_VEL['VELDir_MEAN']
    corrected_mean_products_geo=gpd.GeoDataFrame(corrected_mean_products, geometry='geometry', crs=gdf_ew.crs)
    
    corrected_mean_products_geo.to_file(output_folder +"/" + outputFilename[:-4]+"_mean.shp")
    
    

def akhdefo_dashApp(directory="", DEM_Path='', std_thresh_interpolation=1.0, port=8051, smoothing=False):


    """
    An application that visualizes and analyzes raster data using Dash.

    Args:
        directory (str): The path to the directory containing the raster files. Default is an empty string.
        DEM_Path (str): The path to the DEM (Digital Elevation Model) file. Default is an empty string.
        std_thresh_interpolation (float): The standard deviation threshold for interpolation. Default is 1.0.
        port (int): The port number for running the Dash server. Default is 8051.
        smoothing(bool): if True re-interpolate the entire raster with 16 pixel average to fill Nan Values 

    Returns:
        Dash: The Dash application object.

    """
    import os
    from datetime import datetime

    import cmocean
    import dash
    import dash_daq as daq
    import earthpy.spatial as es
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import numpy as np
    import plotly.colors as colors
    import rasterio
    from dash import dcc, html
    from dash.dependencies import Input, Output, State
    from rasterio.enums import Resampling
    from rasterio.transform import from_origin
    from scipy import interpolate


    app = dash.Dash(__name__)

    

    def stack_rasters(directory):
        raster_list = []
        transform_list=[]
        raster_files = sorted([f for f in os.listdir(directory) if f.endswith('.tif')])

        for file in raster_files:
            with rasterio.open(os.path.join(directory, file)) as src:
                raster_list.append(src.read(1))
                transform_list.append(src.transform)
                crs=src.crs

        return np.dstack(raster_list), raster_files, transform_list, crs

    def calculate_mean_circle(raster_stack, x, y, r):
        indices = np.indices(raster_stack.shape[:2])
        distances = np.sqrt((indices[0] - y)**2 + (indices[1] - x)**2)
        mask = distances < r
        pixel_values = raster_stack[mask, :]
        return np.nanmean(pixel_values, axis=0)
    
    def save_layers_as_geotiff(raster_stack, transforms, crs, output_dir, output_prefix, raster_files):

        ################Uncomment this section if you want to subtrcat each raster deformation to first raster deformation)###################

        # # Create a copy of the raster stack
        # result_stack = np.copy(raster_stack)
        # # Create an empty mask array with the same shape as the raster stack
        # mask_stack = np.zeros_like(raster_stack)
        
        # # Subtract each band by the first band
        # for i in range((result_stack.shape[2])):
        #     mask = np.isnan(raster_stack[:, :, i])  # Create a mask for NaN values
        #     result_stack[:, :, i] = np.where(mask, 0, raster_stack[:, :, i])  # Replace NaN values with zero
        #     result_stack[:, :, i]=result_stack[:, :, i]-result_stack[:, :, 0]
        #     mask_stack[:, :, i] = mask  # Store the mask for this band in the mask stack
        #     result_stack[:, :, i][mask]=np.nan
        
        # raster_stack=result_stack

        #########################################################################################################################################

        path=output_dir

        import re

        def convert_path(path):
            if re.match(r'^[A-Za-z]:\\', path):
                path = r'\\'.join(re.split(r'[\\/]+', path))
            return path

        
        converted_path = convert_path(path)
        converted_path=converted_path + "/" + "corrected"

        if not os.path.exists(converted_path):
            os.makedirs(converted_path)

       

        base_names = [os.path.basename(file) for file in raster_files]
        count=0
        for layer_index in range(raster_stack.shape[2]):
            output_filename = output_prefix + "_" + base_names[count]
            output_path = os.path.join(converted_path, output_filename)

            # Create a new GeoTIFF file
            with rasterio.open(output_path, 'w', driver='GTiff', height=raster_stack.shape[0], 
                            width=raster_stack.shape[1], count=1, dtype=raster_stack.dtype,
                            crs=crs, transform=transforms[layer_index]) as dst:
                # Write the layer to the GeoTIFF file
                dst.write(raster_stack[:, :, layer_index], 1)

            print(f"Layer {layer_index} saved as {output_path}")
            count=count+1
        

    def interpolate_rasters(raster_stack, raster_files, transform_list, crs, std_thresh_interpolation, smoothing):

        #raster_stack
        
        # #raster_stack=raster_stack - raster_stack[0]
        # # Calculate the cumulative sums along the third dimension
        # #raster_stack = np.cumsum(raster_stack, axis=2)



        if std_thresh_interpolation is not None:

            x = np.arange(0, raster_stack.shape[2])
            y = np.arange(0, raster_stack.shape[1])
            z = np.arange(0, raster_stack.shape[0])

             
            #  # Replace outliers with NaN
            outlier_mask = np.abs(raster_stack - np.nanmean(raster_stack)) > std_thresh_interpolation * np.nanstd(raster_stack)
            raster_stack[outlier_mask] = np.nan

            interp_func = interpolate.RegularGridInterpolator((z, y, x), raster_stack, method='nearest')

            nan_locs = np.where(np.isnan(raster_stack))
            raster_stack[nan_locs] = interp_func(nan_locs)
        
        #  # Replace outliers with NaN
        # outlier_mask = np.abs(raster_stack - np.nanmean(raster_stack)) > std_thresh_interpolation * np.nanstd(raster_stack)
        # raster_stack[outlier_mask] = np.nan

        # #################
        # #Reinterpolate non-NaN values with the 16-pixel average of nearest values. This helps to elimnate spikes in the dataset
        if smoothing==True:
           
            from scipy.ndimage import convolve

            def replace_non_nan_with_avg(arr):
                kernel = np.ones((3, 3, 1))
                kernel[1, 1, 0] = 0  # Exclude the center pixel from the kernel

                # Calculate the sum of the neighboring pixels for each non-NaN pixel
                sum_neighbors = convolve(arr, kernel, mode='constant', cval=np.nan)

                # Count the number of non-NaN neighbors for each pixel
                non_nan_count = convolve(~np.isnan(arr).astype(int), kernel, mode='constant', cval=0)

                # Calculate the average of neighboring pixels and replace non-NaN values with the average
                avg_neighbors = np.where(non_nan_count > 0, sum_neighbors / non_nan_count, np.nan)
                filled_arr = np.where(np.isnan(arr), avg_neighbors, arr)

                return filled_arr
            raster_stack = replace_non_nan_with_avg(raster_stack)   
            # raster_stack = np.where(non_nan_count > 0, np.divide(raster_sum, non_nan_count, where=non_nan_count > 0), np.nan)

    #Uncomment below function to replace fill nan values
    # import numpy as np
    # from scipy.ndimage import convolve

    # def fill_nan(arr):
    #     kernel = np.ones((3, 3, 1))
    #     kernel[1, 1, 0] = 0  # Exclude the center pixel from the kernel

    #     # Count the number of non-NaN neighbors for each pixel
    #     non_nan_count = convolve(~np.isnan(arr).astype(int), kernel, mode='constant', cval=0)

    #     # Calculate the sum of non-NaN neighbors for each pixel
    #     sum_neighbors = convolve(arr, kernel, mode='constant', cval=np.nan)

    #     # Calculate the average by dividing the sum by the count
    #     filled_arr = np.where(non_nan_count > 0, sum_neighbors / non_nan_count, np.nan)

    #     return filled_arr


        #     for z in range(raster_stack.shape[0]):
        #         for y in range(raster_stack.shape[1]):
        #             for x in range(raster_stack.shape[2]):
        #                 if not np.isnan(raster_stack[z, y, x]):
        #                     patch = raster_stack[max(0, z-1):z+2, max(0, y-1):y+2, max(0, x-1):x+2]
        #                     patch_mean = np.nanmean(patch)
        #                     raster_stack[z, y, x] = patch_mean

        
        
        # #  # Replace outliers with NaN
        # # outlier_mask = np.abs(raster_stack - np.nanmean(raster_stack)) > std_thresh_interpolation * np.nanstd(raster_stack)
        # # raster_stack[outlier_mask] = np.nan

        # #######################################################
        # # Replace outliers with the 8-pixel average of nearest values
        
        # outlier_locs = np.where(outlier_mask)
        # for z, y, x in zip(*outlier_locs):
        #     patch = raster_stack[max(0, z-1):z+2, max(0, y-1):y+2, max(0, x-1):x+2]
        #     patch_mean = np.nanmean(patch)
        #     raster_stack[z, y, x] = patch_mean

        #print("raster_stack shape", raster_stack.shape)
        #############################################
       
        

        #save_layers_as_geotiff(raster_stack, transform_list, crs, output_dir, 'interpolated_', raster_files)

        

        return raster_stack, raster_files, transform_list, crs
    
  
    from datetime import datetime

    def calculate_total_days(start_date, end_date):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        time_difference = end_date_obj - start_date_obj
        total_days = time_difference.days + 1

        return total_days

    def calculate_cumulative_deformation(lst):
        lst = np.array(lst)
        cumulative_deformation = np.insert(np.cumsum(lst), 0, 0)
        #cumulative_deformation=np.cumsum(lst)
        return cumulative_deformation.tolist()

    def calculate_std(pixel_values):
        std = np.std(pixel_values)
        return std
    from numpy import arange, where, zeros, zeros_like
    from scipy.interpolate import interp1d
    from scipy.stats import linregress

    def interpolate_nans(band_values):
        mask = np.isnan(band_values)
        if mask.all():
            return np.zeros_like(band_values)
        else:
            x = np.arange(len(band_values))
            y = np.array(band_values)[~mask]
            f = interp1d(x[~mask], y, bounds_error=False, fill_value='extrapolate')
            xnew = np.arange(len(band_values))
            return f(xnew)
    
    def calculate_linear_change(pixel_values, polyfit_order):
       
        times = arange(len(pixel_values))
        # Fit a linear polynomial (degree 1) to the data
        coefficients = np.polyfit(times, pixel_values, polyfit_order)
        # Extract the slope and intercept from the coefficients
        slope = coefficients[0]
        # Calculate the residuals (errors)
        residuals = pixel_values - (slope * times + coefficients[1])
        # Calculate the standard deviation of the residuals
        std_res = np.nanstd(residuals)
        std=np.nanstd(pixel_values)

        return slope, std, residuals
    
    # def create_linear_velocity_map(raster_stack):
    #     height, width, num_bands = raster_stack.shape

    #     velocity_map = np.zeros((height, width), dtype=float)

    #     band_values = np.transpose(raster_stack, axes=(2, 0, 1)).reshape(num_bands, -1)

    #     #interpolated_band_values = np.apply_along_axis(interpolate_nans, axis=0, arr=band_values)

    #     times = np.arange(num_bands)

    #     slopes = np.apply_along_axis(lambda x: linregress(times, x)[0], axis=0, arr=band_values)

    #     velocity_map = slopes.reshape(height, width)

    #     return velocity_map
    
    def create_cumulative_deformation_map(raster_stack):
        # # Extract the dimensions of the raster stack
        # height, width, num_bands = raster_stack.shape

        # # Create an empty array to store the cumulative deformation map
        # deformation_map = np.zeros((height, width), dtype=float)

        #     # Get the values of each band for all pixels at once
        # band_values = raster_stack.reshape(-1, raster_stack.shape[2])

        # Compute the mean deformation 
        deformation_map = np.nanmean(raster_stack, axis=2)

        # Reshape the deformation array to match the dimensions of deformation_map
        #deformation_map = deformation.reshape(height, width)
        

        return deformation_map

    
    
    
    def calculate_mean_raster(raster_stack):
        # Ensure rasters is a numpy array
        raster_stack = np.array(raster_stack)

        mean_raster = np.nanmean(raster_stack, axis=0)
        
        
        
        return mean_raster
    
    def export_mean_raster(mean_raster, crs, transform, output_directory):
    # Create a new GeoTIFF file for the mean raster
        path=output_directory

        import re

        def convert_path(path):
            if re.match(r'^[A-Za-z]:\\', path):
                path = r'\\'.join(re.split(r'[\\/]+', path))
            return path

        
        converted_path = convert_path(path)

        if not os.path.exists(converted_path):
            os.makedirs(converted_path)

        

        output_path = os.path.join(converted_path, "Mean_Annual_VEL.tif")
        with rasterio.open(output_path, 'w', driver='GTiff', height=mean_raster.shape[0],
                        width=mean_raster.shape[1], count=1, dtype=mean_raster.dtype,
                        crs=crs, transform=transform) as dst:
            dst.write(mean_raster, 1)
        print("Mean raster saved as GeoTIFF: ", output_path)
        return 
        
    raster_directory = directory
    raster_stack, raster_files, transform_list, crs= stack_rasters(raster_directory)
    
    raster_stack, raster_files, transform_list, crs = interpolate_rasters( raster_stack, raster_files, transform_list, crs, std_thresh_interpolation=std_thresh_interpolation, smoothing=smoothing)
    
    cumulative_deformation_map = create_cumulative_deformation_map(raster_stack)
    #linear_velocity_map = create_linear_velocity_map(raster_stack)
    
    #mean_raster, raster_diff = calculate_mean_raster(raster_stack)

    raster_dates = [datetime.strptime(f[:8], "%Y%m%d") for f in raster_files]
    dem_path = DEM_Path
    with rasterio.open(dem_path) as dem_src:
        dem = dem_src.read(1)

    hillshade = es.hillshade(dem)

    # import matplotlib.cm as cm

    # # Get a list of all available colormaps
    # cmap_options = [cmap for cmap in cm.datad]

    # # Set the default cmap value
    # default_cmap = cmap_options[0]
    # # Get cmocean colormap names
    # cmaps = cmocean.cm.cmapnames


    def matplotlib_to_plotly(cmap, pl_entries):
        h = 1.0/(pl_entries-1)
        pl_colorscale = []
        
        for k in range(pl_entries):
            C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
            pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
            
        return pl_colorscale

        # Include all cmocean colormaps
    cmap_options = [cmap for cmap in cmocean.cm.cmapnames]
    # Include all matplotlib colormaps
    cmap_options.extend([cmap for cmap in plt.colormaps()])

        # Define the app layout
    app.layout = html.Div([
        html.Div([
            html.Div([
                html.Label('X-axis Label:'),
                dcc.Input(id='x-axis-input', type='text', placeholder='Enter X-axis label', value='Dates'),
                html.Label('Y-axis Label:'),
                dcc.Input(id='y-axis-input', type='text', placeholder='Enter Y-axis label', value='cm'),
                html.Label('Enter Path to Save Geotif Products:'),
                dcc.Input(id='Path_meanraster-input', type='text', placeholder='Enter Path to Directory to Save Mean Velocity Raster', value='./'),
                html.Div(id="output-div"),
            ], style={'padding': '10px', 'vertical-align': 'top'}),
            
            html.Div([
                dcc.Graph(id='raster-plot', figure={
                    'data': [
                    {'z': hillshade, 'type': 'heatmap', 'colorscale': 'Greys', 'zmin': 0, 'zmax': 255, 'name': 'Hillshade',
                    'colorbar': {'thickness': 0}, 'layer': 'below'},  # Hide the colorbar for hillshade trace
                    {'z': cumulative_deformation_map, 'type': 'heatmap', 'colorscale': 'Viridis', 'name': 'Deformation',
                    'colorbar': {'title': 'colorbar-label'}}
                    ],
                    'layout': {
                        'title': 'Raster Overlay',
                        'hovermode': 'closest',
                        'yaxis': {'autorange': 'reversed'},
                        'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50},
                        'height': '500px',
                        'resizable': True,
                        'colorway': ['black', 'blue'],
                        'coloraxis': {'colorbar': {'title': 'Colorbar Label'}}  # Add colorbar label
                    }
                })
            ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
            html.Div([
                dcc.Graph(id='profile-plot', style={'height': '400px'})
            ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'})
        ], style={'padding': '10px', 'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        html.Div([
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        id='selection-type2',
                        options=[{'label': i, 'value': i} for i in ['Deformation', 'Velocity']],
                        value='Deformation',
                        labelStyle={'display': 'inline-block'}
                    ),
                    html.Hr(),  # Add horizontal line
                    dcc.Input(id='fig_title', type='text', placeholder='Type Figure Title', value='Figure Title'),
                    html.Hr(),  # Add horizontal line
                    dcc.Input(id='fig_colorbar_label', type='text', placeholder='Type Figure Colorbar Label', value='Colorbar Label'),
                    html.Hr(),  # Add horizontal line
                    html.Label('Circle Size:'),
                    daq.Slider(
                        id='circle-size-slider',
                        min=1,
                        max=100,
                        step=1,
                        value=10,
                        marks={i: str(i) for i in range(0, 101, 10)},
                        included=True,
                    ),
                    html.Div(style={'height': '20px'})  # Add extra space
                ]),
                
                html.Div([
                    dcc.RadioItems(
                        id='selection-type',
                        options=[{'label': i, 'value': i} for i in ['Point', 'Circle']],
                        value='Point',
                        labelStyle={'display': 'inline-block'}
                    ),
                    html.Hr(),  # Add horizontal line
                    html.Label('Start Date:'),
                    html.Hr(),  # Add horizontal line
                    dcc.DatePickerSingle(
                        id='start-date-picker',
                        min_date_allowed=min(raster_dates),
                        max_date_allowed=max(raster_dates),
                        initial_visible_month=min(raster_dates),
                        date=min(raster_dates)
                    ),
                    html.Div(id="selected-start-date"),
                    html.Hr(),  # Add horizontal line
                    html.Label('End Date:'),
                    dcc.DatePickerSingle(
                        id='end-date-picker',
                        min_date_allowed=min(raster_dates),
                        max_date_allowed=max(raster_dates),
                        initial_visible_month=max(raster_dates),
                        date=max(raster_dates)
                    ),
                    html.Div(id="selected-end-date"),
                    html.Hr(),  # Add horizontal line
                    html.Button('Reset', id='reset-button', n_clicks=0)
                ], style={'padding': '10px', 'vertical-align': 'top'})
            ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}),
            
            html.Div([
                html.Div([
                    html.Button('Toggle Trendline', id='toggle-trendline', n_clicks=0),
                    html.Hr(),
                    html.Button('Toggle Cumulative-Deformation', id='toggle-cum_sum', n_clicks=0),
                    html.Hr(),  # Add horizontal line
                    html.Button("Download GeoTIFF", id="btn_download", n_clicks=0),
                    dcc.Download(id="download"),
                    html.Label('Colormap:'),
                    html.Hr(),  # Add horizontal line
                    dcc.Dropdown(
                        id='colorscale-dropdown',
                        options=[{'label': cmap, 'value': cmap} for cmap in cmap_options],
                        value='Viridis',
                        clearable=True,
                        searchable=True
                    ),
                    html.Label('Transparency:'),
                    html.Hr(),  # Add horizontal line
                    daq.Slider(
                        id='transparency-slider',
                        min=0,
                        max=1,
                        step=0.1,
                        value=0.6,
                        marks={i / 10: str(i / 10) for i in range(0, 11)},
                        included=True , 
                    ), html.Div(style={'height': '20px'}),  # Add extra space
                    
                    html.Label('PolyFit-Order:', style={"margin-bottom": "10px"}),
                    
                    daq.Slider(
                        id='polyfit-slider',
                        min=1,
                        max=10,
                        step=1,
                        value=1,
                        marks={i : str(i) for i in range(0, 11, 1)},
                        included=True
                    )
                ], style={'padding': '20px', 'vertical-align': 'top'})
            ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'})
        ], style={'padding': '10px', 'width': '10%', 'display': 'inline-block', 'vertical-align': 'top'})  # Adjust the width to 40%
    ], style={'padding': '10px', 'width': '100%', 'display': 'flex'})


        
   
    @app.callback(
        Output('raster-plot', 'figure'),
        [Input('colorscale-dropdown', 'value'), Input('transparency-slider', 'value'), Input('raster-plot', 'clickData'),
        Input('reset-button', 'n_clicks'), Input('selection-type', 'value'), Input('circle-size-slider', 'value'), Input('fig_title', 'value'),
        Input('fig_colorbar_label', 'value'), Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'), Input('selection-type2', 'value')]
    )
    def update_raster_plot(cmap_value, transparency, click_data, reset_clicks, selection_type, circle_size, Fig_title, Fig_cbar_label, start_date, end_date, selection_type2):
        
        # start_index = raster_dates.index(datetime.strptime(start_date, "%Y-%m-%d"))
        # end_index = raster_dates.index(datetime.strptime(end_date, "%Y-%m-%d"))

        # raster_stack = raster_stack[:, :, start_index:end_index + 1]

       
        if cmap_value in cmocean.cm.cmapnames:
            cmap = cm.get_cmap('cmo.'+cmap_value.lower())
        else:
            cmap = cm.get_cmap(cmap_value.lower())
            
        cmap_plotly = matplotlib_to_plotly(cmap, 255)
        
        
        
        if reset_clicks:
            return {
                'data': [ {'z': hillshade, 'type': 'heatmap', 'colorscale': 'Greys', 'zmin': 0, 'zmax': 255, 'name': 'Hillshade', 'colorbar': {'thickness': 0}, 'layer': 'below'},
            {'z': cumulative_deformation_map, 'type': 'heatmap', 'colorscale': cmap_plotly, 'name': 'Mean Deformation', 'opacity': transparency,
              'zmin': np.nanmin(cumulative_deformation_map),
              'zmax': np.nanmax(cumulative_deformation_map)}],
                'layout': {
                    'title': Fig_title,
                    'hovermode': 'closest',
                    'yaxis': {'autorange': 'reversed'},
                    'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50},
                    'height': '400px',
                    'resizable': True,
                    'colorway': ['black', 'blue'], 'colorbar': {'title': Fig_cbar_label}  # Add colorbar label
                }
            }

       
        
        
        if selection_type2=='Velocity':
            
            
            
                
            
            total_days = calculate_total_days(start_date, end_date)
            total_days=int(total_days)
            Aver_annual_VEL_Map=cumulative_deformation_map/total_days * 365
            fig_data = [ {'z': hillshade, 'type': 'heatmap', 'colorscale': 'Greys', 'zmin': 0, 'zmax': 255, 'name': 'Hillshade', 'colorbar': {'thickness': 0}, 'layer': 'below'},
            {'z': Aver_annual_VEL_Map, 'type': 'heatmap', 'colorscale': cmap_plotly, 'name': 'Mean-VEL', 'opacity': transparency, 'zmin': np.nanmin(Aver_annual_VEL_Map),
              'zmax': np.nanmax(Aver_annual_VEL_Map)}]
            
            

            layout = {
                'title': Fig_title,
                'hovermode': 'closest',
                'yaxis': {'autorange': 'reversed'},
                'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50},
                'height': '400px',
                'resizable': True,
                'colorway': ['black', 'blue'], 'colorbar': { 'title': Fig_cbar_label}  # Add colorbar label

            }
            
        elif selection_type2=='Deformation':
            
            
        
            fig_data = [
                {'z': hillshade, 'type': 'heatmap', 'colorscale': 'Greys', 'zmin': 0, 'zmax': 255, 'name': 'Hillshade', 'colorbar': {'thickness': 0}, 'layer': 'below' },
                {'z': cumulative_deformation_map, 'type': 'heatmap', 'colorscale': cmap_plotly, 'name': 'Mean-Defo', 'opacity': transparency, 'zmin': np.nanmin(cumulative_deformation_map),
                'zmax': np.nanmax(cumulative_deformation_map)}

            ]
            

            layout = {
                'title': Fig_title,
                'hovermode': 'closest',
                'yaxis': {'autorange': 'reversed'},
                'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50},
                'height': '400px',
                'resizable': True,
                'colorway': ['black', 'blue'], 'colorbar': {'title': Fig_cbar_label}  # Add colorbar label

            }

        if click_data:
            clicked_x = click_data['points'][0]['x']
            clicked_y = click_data['points'][0]['y']

            if selection_type == 'Point':
                fig_data.append({'x': [clicked_x], 'y': [clicked_y], 'mode': 'markers', 'marker': {'symbol': 'cross', 'color': 'red'}, 'name': 'Clicked Point'})
            elif selection_type == 'Circle':
                theta = np.linspace(0, 2*np.pi, 100)
                x = clicked_x + circle_size * np.cos(theta)
                y = clicked_y + circle_size * np.sin(theta)
                fig_data.append({'x': x, 'y': y, 'mode': 'lines', 'line': {'color': 'red'}, 'name': 'Circle'})
                layout['annotations'] = [{
                    'x': clicked_x,
                    'y': clicked_y,
                    'text': f"Circle (r={circle_size})",
                    'xref': 'x',
                    'yref': 'y',
                    'showarrow': False
                }]

        return {
            'data': fig_data,
            'layout': layout
        }

    @app.callback(Output("output-div", "n_clicks"),
            [
        Input('btn_download', 'n_clicks'), Input("Path_meanraster-input", "value"), Input('selection-type2', 'value'), Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date')])
    
    def export_mean_raster_callback(n_clicks, path_saveFile, selection_type2, start_date, end_date ):
        
        if n_clicks > 0:
           
        
            if selection_type2=='Deformation':
                # cumulative_deformation_map = create_cumulative_deformation_map(raster_stack[start_index:end_index + 1])
                export_mean_raster(cumulative_deformation_map, crs, transform_list[0], path_saveFile)
                save_layers_as_geotiff(raster_stack, transform_list, crs, path_saveFile, 'interpolated_', raster_files)
            elif selection_type2=='Velocity':
                # linear_velocity_map = create_linear_velocity_map(raster_stack[start_index:end_index + 1])
                total_days = calculate_total_days(start_date, end_date)
                total_days=int(total_days)
                Aver_annual_VEL_Map=cumulative_deformation_map/total_days *360 
                export_mean_raster(Aver_annual_VEL_Map, crs, transform_list[0], path_saveFile)
                save_layers_as_geotiff(raster_stack, transform_list, crs, path_saveFile, 'interpolated_', raster_files)
        
    @app.callback(
        Output('profile-plot', 'figure'),
        [Input('raster-plot', 'clickData'), Input('toggle-trendline', 'n_clicks'), Input('start-date-picker', 'date'),
        Input('end-date-picker', 'date'), Input('reset-button', 'n_clicks'), Input('selection-type', 'value'),
        Input('circle-size-slider', 'value'),
        Input('x-axis-input', 'value'), Input('y-axis-input', 'value'), Input('toggle-cum_sum', 'n_clicks'), Input('polyfit-slider', 'value')]  # Add inputs for the textbox values
    )


    def update_profile_plot(click_data, n_clicks, start_date, end_date, reset_clicks, selection_type, circle_size, x_label, y_label, cum_sum, polyfit_order):
        
        def subtract_cumulative(data):
            cumulative_changes = [0]  # Initialize the cumulative changes with 0

            # Calculate the cumulative changes
            for i in range(1, len(data)):
                change = data[i] - data[i-1]
                cumulative_change = cumulative_changes[i-1] + change
                cumulative_changes.append(cumulative_change)
            return cumulative_changes
        
        if reset_clicks:
            return {}

        if click_data is None:
            return {}

        current_x = int(click_data['points'][0]['x'])
        current_y = int(click_data['points'][0]['y'])

        start_index = raster_dates.index(datetime.strptime(start_date, "%Y-%m-%d"))
        end_index = raster_dates.index(datetime.strptime(end_date, "%Y-%m-%d"))
        
       

        if selection_type == 'Point':
            pixel_values = raster_stack[current_y, current_x, start_index:end_index + 1]

            pixel_values_cumsum=subtract_cumulative(pixel_values)
            #pixel_values = [pixel_values[i] - pixel_values[0] for i in range(len(pixel_values))]
           

            #pixel_values = [pixel_values[i] - pixel_values[0] for i in range(len(pixel_values))]
            pixel_values_cumsum=np.cumsum(pixel_values_cumsum)

            
            total_days = calculate_total_days(start_date, end_date)
            total_days=int(total_days)
            #calculate days difference
            #total_days = end_index - start_index + 1



        elif selection_type == 'Circle':
            pixel_values = calculate_mean_circle(raster_stack[:, :, start_index:end_index + 1], current_x, current_y, circle_size)
            
            pixel_values_cumsum=subtract_cumulative(pixel_values)
           
            #pixel_values = [pixel_values[i] - pixel_values[0] for i in range(len(pixel_values))]
            pixel_values_cumsum=np.cumsum(pixel_values_cumsum)

            

            
            total_days = calculate_total_days(start_date, end_date)
            total_days=int(total_days)
         # Calculate slope, std, and residuals
        linear_change, std, residuals=calculate_linear_change(pixel_values, polyfit_order)
       

        std_mean = calculate_std(pixel_values)
        annual_slope=linear_change/total_days *365
        annual_std=std/total_days *365
        Aver_Defo=np.nanmean(pixel_values)
        Aver_VEL=Aver_Defo/total_days
        Aver_annual_VEL=Aver_Defo/total_days *365

        

        show_trendline = n_clicks % 2 != 0
        show_cum_sumProfile= cum_sum % 2 != 0

        profile_figure = {
            'data': [
                {'x': raster_dates[start_index:end_index + 1], 'y': pixel_values, 'mode': 'lines+markers', 'name': 'Deformation'}
            ],
            'layout': {
                'title': f'Linear-VEL: {annual_slope:.4f} {y_label}/year,  Std: {annual_std:.4f}, Ave-VEL:{Aver_annual_VEL:.4f}{y_label}/year , Ave-std: {std_mean:.4f}',
                'xaxis': {'title': x_label, 'tickangle': 45},
                'yaxis': {'title': y_label},
                'annotations': [
                    {
                        'x': 0.5,
                        'y': 1.21,
                        'xref': 'paper',
                        'yref': 'paper',
                        'text': f'Total-Days: {total_days}, Linear-VEL: {linear_change:.4f}{y_label}/{total_days}days, Std: {std:.4f}, Aver_Defo:{Aver_Defo:.4f}{y_label}',
                        'showarrow': False,
                        'font': {'color': 'black', 'size': 14}
                    }
                ]
            }
        }

        if show_trendline:
            
            x = np.arange(len(pixel_values))
            coefficients = np.polyfit(x, pixel_values, polyfit_order)
            polynomial = np.poly1d(coefficients)
            profile_figure['data'].append({'x': raster_dates[start_index:end_index + 1], 'y': polynomial(x), 'mode': 'lines', 'name': 'Trendline-Deformation'})
            # profile_figure['data'].append({'x': raster_dates[start_index:end_index + 1], 'y': residuals, 'mode': 'lines+markers', 'name': 'Residuals-Deformation'})
            
            #Residual Error and Trendline
        if show_cum_sumProfile:
           
           
           
            linear_change, std, residuals=calculate_linear_change(pixel_values_cumsum, polyfit_order)
            std_mean = calculate_std(pixel_values_cumsum)
            annual_slope=linear_change/total_days *365
            annual_std=std/total_days *365
            Aver_Defo=np.nanmean(pixel_values_cumsum)
            Aver_VEL=Aver_Defo/total_days
            Aver_annual_VEL=Aver_Defo/total_days *365
            x = np.arange(len(pixel_values_cumsum))
            coefficients = np.polyfit(x, pixel_values_cumsum, polyfit_order)
            polynomial = np.poly1d(coefficients)
            

        ###################################
           
            profile_figure = {
            'data': [
                {'x': raster_dates[start_index:end_index + 1], 'y': pixel_values_cumsum, 'mode': 'lines+markers',  'name': 'Cummulative-Deformation'}
                
            ],
            'layout': {
                'title': f'Linear-VEL: {annual_slope:.4f} {y_label}/year,  Std: {annual_std:.4f}, Ave-VEL:{Aver_annual_VEL:.4f}{y_label}/year , Ave-std: {std_mean:.4f}',
                'xaxis': {'title': x_label, 'tickangle': 45},
                'yaxis': {'title': y_label},
                'annotations': [
                    {
                        'x': 0.5,
                        'y': 1.21,
                        'xref': 'paper',
                        'yref': 'paper',
                        'text': f'Total-Days: {total_days}, Linear-VEL: {linear_change:.4f}{y_label}/{total_days}days, Std: {std:.4f}, Aver_Defo:{Aver_Defo:.4f}{y_label}',
                        'showarrow': False,
                        'font': {'color': 'black', 'size': 14}
                    }
                ]
            }
        }

            if show_trendline:
                
                x = np.arange(len(pixel_values_cumsum))
                coefficients = np.polyfit(x, pixel_values_cumsum, polyfit_order)
                polynomial = np.poly1d(coefficients)
                profile_figure['data'].append({'x': raster_dates[start_index:end_index + 1], 'y': polynomial(x), 'mode': 'line', 'name': 'Trendline-Cummulative'})
                # profile_figure['data'].append({'x': raster_dates[start_index:end_index + 1], 'y': residuals, 'mode': 'lines+markers', 'name': 'Residuals-Deformation'})
       
        ######################

        return profile_figure
    
    
    app.run_server(port=port)

    return app.run_server(port=port)



    


            

    



    

