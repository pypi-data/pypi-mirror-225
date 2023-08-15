from akhdefo_functions import utm_to_latlon
from akhdefo_functions import akhdefo_viewer
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import os
import rasterio as rio
import requests
from datetime import datetime
import planet
import json
from datetime import datetime
from planet import Session, data_filter
from planet import Session, OrdersClient
from pathlib import Path
import shutil
from osgeo import osr
import cmocean
import geopandas as gpd
import gstools as gs

def Akhdefo_resample(input_raster="", output_raster="" , xres=3.125 , yres=3.125, SavFig=False , convert_units=1000.0):
    """
    This program performs raster resampling for  rasters
   
    Parameters
    ----------

    input_raster: str
        path to input raster

    output_raster: str
        path to output raster


    xres: float
        horizontal resolution

    yres: float 
        vertical resolution

    SavFig: bool
        True to save output plot False to ignore exporting plot

    convert_units: float 
        if True converts raster value units from meter to mm: depends on your raster unit adjust this value
    
    """
    
   
    ds = gdal.Open(input_raster)

    # resample
    dsRes = gdal.Warp(output_raster, ds, xRes = xres, yRes = yres, 
                    resampleAlg = "bilinear")
    
    dsRes =None 
    ds = None
  
    # # visualize
    src=rasterio.open(output_raster)
    meta= src.meta
    meta.update({'nodata': np.nan})
    array=src.read(1, masked=True)
    # #array = dsRes.GetRasterBand(1).ReadAsArray()
    array[array==-32767.0]=np.nan
    array=array*convert_units

    basename=os.path.splitext(os.path.basename(input_raster))[0]
    def create_fancy_figure(array, basename, SavFig=SavFig, convert_units=convert_units):
       
        # Creating the figure
        fig, ax = plt.subplots()
        # Making sure 'north' is up, in case Y was flipped
        #ax.invert_yaxis()
        # Creating a colormap
        cmap = plt.get_cmap('viridis')
        # Creating the image
        img = ax.imshow(array, cmap=cmap)
        # Creating the colorbar
        cbar = fig.colorbar(img, ax=ax, orientation='vertical', pad=0.01)
        
        # Adding labels to the axes
        ax.set_xlabel('Easting')
        ax.set_ylabel('Northing')

        # Adding a title to the plot
        ax.set_title(basename)

        if SavFig==True:
        # Saving the figure
            fig.savefig(basename, dpi=300, bbox_inches='tight')

        plt.imshow()

        return fig
    
    a=create_fancy_figure(array, basename, SavFig=SavFig, convert_units=convert_units)
    if convert_units==True:
        
        src.close() # close the rasterio dataset
        os.remove(output_raster) # delete the file 
        
        rs=rasterio.open(output_raster, "w+", **meta)
        rs.write(array, indexes=1)
    plt.show()


def Akhdefo_inversion(horizontal_InSAR="", Vertical_InSAR="", EW_Akhdefo="", NS_Akhdefo="", demFile="", output_folder=r""):
    """
    This program calculates 3D displacement velocity (East-West,North-South and vertical) using combined optical and InSAR products
   
    Parameters
    ----------

    horizontal_InSAR: str
        path to East Velocity InSAR product in geotif format

    Vertical_InSAR: str
        path to Vertical Velocity InSAR product in geotif format

    EW_Akhdefo: str 
        path to east-west velocity  akhdefo(optical) product in geotif format

    NS_Akhdefo: str
        path to north-south velocity  akhdefo(optical) product in geotif format

    demFile: str
        path to DEM raster in geotif format

    output_folder : str
        path to save raster products 

    
    Returns
    -------
    Three geotif rasters
        3D-Velocity (D3D in mm/year) raster
        Plunge raster in degrees
        Trend raster in degress


    """
    
    
    
    
    if not os.path.exists(output_folder ):
        os.makedirs(output_folder)
    #Load images with rasterio
    D_EW_InSAR=rio.open(horizontal_InSAR)
    D_vertical_insar=rio.open(Vertical_InSAR)
    D_EW_akhdefo=rio.open(EW_Akhdefo)
    D_NS_akhdefo=rio.open(NS_Akhdefo)
    #read images with rasterio
    DEW_insar=D_EW_InSAR.read(1, masked=True)
    DEW_insar[DEW_insar==-32767.0]=np.nan
    DEW_insar=DEW_insar*1000

    DEW_akhdefo=D_EW_akhdefo.read(1, masked=True)
    D_vertical=D_vertical_insar.read(1, masked=True)
    D_vertical[D_vertical==-32767.0]=np.nan
    D_vertical=D_vertical*1000

    DNS_akhdefo=D_NS_akhdefo.read(1, masked=True)

    print (DEW_akhdefo.shape)
    print(D_vertical.shape)
    print (DEW_akhdefo.shape)
    print(DEW_insar.shape)
    DH=np.hypot(DEW_akhdefo, DNS_akhdefo)
    D3D=np.hypot(DH, D_vertical )

    meta=D_EW_InSAR.meta

    trend_radians=np.arcsin(DNS_akhdefo/DH)
    trend_degrees=np.degrees(trend_radians)
    print ("Trend in degree raw data: ", trend_degrees.min(), trend_degrees.max())
    trend_degrees=(450 - trend_degrees ) % 360

    plung_radians=np.arcsin(D_vertical/D3D)
    plung_degree=np.degrees(plung_radians)
    #plung_degree=(90-plung_degree)% 90

    print ("DH: ", DH.max(), DH.min())
    print("D3D: ", D3D.max(), D3D.min())

    #Save products
    _3D_vel=output_folder + "/" + "D3D.tif"
    plung=output_folder+ "/" + "plung_degree.tif"
    trend=output_folder+ "/" + "trend_degrees.tif"
    # with rio.open("DH.tif", 'w', **meta) as dst:
    #         dst.write(DH, indexes=1)
    with rio.open(_3D_vel, 'w', **meta) as dst:
            dst.write(D3D, indexes=1)
    with rio.open(trend, 'w', **meta) as dst:
            dst.write(trend_degrees, indexes=1)
    with rio.open(plung, 'w', **meta) as dst:
            dst.write(plung_degree, indexes=1)


    
    p1=akhdefo_viewer(Path_to_DEMFile=demFile, rasterfile=_3D_vel , colorbar_label="mm/year", title="3D Velocity", pixel_resolution_meter=3.125, outputfolder=output_folder,
    outputfileName="3D_Disp.jpg",  cmap=cmocean.cm.speed, alpha=0.8, noDATA_Mask=True, normalize=True)
    p2=akhdefo_viewer(Path_to_DEMFile=demFile, rasterfile=plung , colorbar_label="degrees", title="Plunge of Dispalcement Velocity", pixel_resolution_meter=3.125, outputfolder=output_folder,
    outputfileName="plunge.jpg", cmap=cmocean.cm.delta, alpha=0.8, noDATA_Mask=True, normalize=True)
    p3=akhdefo_viewer(Path_to_DEMFile=demFile, rasterfile=trend , colorbar_label="degress", title="Trend of Dispalcement Velocity", pixel_resolution_meter=3.125, outputfolder=output_folder,
    outputfileName="trend.jpg", cmap=cmocean.cm.phase, alpha=0.8, noDATA_MAsk=True, normalize=True)


def Auto_Variogram(path_to_shapefile=r"", column_attribute="", latlon=False):  
    '''
    This program automatically selects best variogram model which later 
    can be used to interpolate datapoints.
    
    Parameters
    ----------
    path_to_shapefile: str 
    type path to shapefile to include data (point data)
    the shapefile attribute must have x, y or lat, lon columns
    
    column_attribute: str
        Name of shapefile field attribute include data

    Returns
    -------
    str
        name of best variogram model
        also figure for plotted variogram models
    
    '''
    
    
    geodata=gpd.read_file(path_to_shapefile)
    
    
    ###############################################################################
    # Estimate the variogram of the field with automatic bins and plot the result.
    
    
    if latlon==True:
        geographic=utm_to_latlon(easting=geodata.x, northing=geodata.y, zone_number=10, zone_letter="N")
        x=geographic[0]
        y=geographic[1]
        z=geodata[column_attribute]
    else:
        x=geodata.x 
        y=geodata.y
        z=geodata[column_attribute]
    bin_center, gamma = gs.vario_estimate((x, y), z, latlon=latlon)

    ###############################################################################
    # Define a set of models to test.

    models = {
        "Gaussian": gs.Gaussian,
        "Exponential": gs.Exponential,
        "Matern": gs.Matern,
        "Stable": gs.Stable,
        "Rational": gs.Rational,
        "Circular": gs.Circular,
        "Spherical": gs.Spherical,
        "SuperSpherical": gs.SuperSpherical,
        "JBessel": gs.JBessel,
    }
    scores = {}

    ###############################################################################
    # Iterate over all models, fit their variogram and calculate the r2 score.
    fig, (ax1,ax2,ax3)=plt.subplots(ncols=1, nrows=3, figsize=(10,10))
    # plot the estimated variogram
    ax1.scatter(bin_center, gamma, color="k", label="data")
    #ax = plt.gca()

    # fit all models to the estimated variogram
    for idx, model in enumerate(models):
        fit_model = models[model](dim=2, len_scale=4, anis=0.2, angles=-0.5, var=0.5, nugget=0.1)
        para, pcov, r2 = fit_model.fit_variogram(bin_center, gamma, return_r2=True)
        fit_model.plot(x_max=max(bin_center), ax=ax1)
        scores[model] = r2
        ax1.legend()
        
                
    ###############################################################################
    # Create a ranking based on the score and determine the best models

    ranking = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    print("RANKING by Pseudo-r2 score", max(scores, key=scores.get))
    
    for i, (model, score) in enumerate(ranking, 1):
        print(f"{i:>6}. {model:>15}: {score:.5}")
       
    
    max_score=max(scores, key=scores.get)
    for idx, model in enumerate(models):
    
        if max_score==list(models)[idx]:
            fit_model = models[model](dim=2, len_scale=4, anis=0.2, angles=-0.5, var=0.5, nugget=0.1)
            fit_model.plot(x_max=max(bin_center), ax=ax2)
            ax2.set_title(max_score)
            ax2.legend()
            
            import pykrige.kriging_tools as kt
            from pykrige.ok import OrdinaryKriging

            # a GSTools based covariance model
            #model_var = gs.models[model](dim=2, len_scale=4, anis=0.2, angles=-0.5, var=0.5, nugget=0.1)
            if latlon==True: 
                gridx = np.arange((x.min()), x.max(), 0.2)
                gridy = np.arange(y.min(), y.max(), 0.2)
            else: 
                gridx = np.arange(geodata.x.min(),geodata.x.max(), 10)
                gridy = np.arange(geodata.y.min(), geodata.y.max(), 10)
            OK1 = OrdinaryKriging(geodata.x, geodata.y, geodata[column_attribute], fit_model)
            z1, ss1 = OK1.execute("grid", gridx, gridy)
            ax3.set_title((model))
            img=ax3.imshow(z1[z1!=0], origin="upper", cmap='Spectral')
            fig.colorbar(img, ax=ax3)
            
    fig.show()
    
    return (max(scores, key=scores.get),bin_center, gamma )




async def akhdefo_download_planet(planet_api_key="", AOI="plinth.json", start_date= "May 1, 2016", end_date= "", limit=5, 
                           item_type="PSOrthoTile", product_bundle="analytic_sr_udm2", clear_percent=90, cloud_filter=0.1, output_folder="raw_data", clip_flag=True, download_data=False):

    ''' Parameters
        ==========
        Note: To use this function need to call await as below:
        =======================================================
        await akhdefo_download_planet()
        ===============================
        planet_api_key: str = "  "
            input planet labs api 

        AOI: str = "plinth.json"
            input area of interest in json file format

        start_date: str = "May 1, 2016"
            input start date as the following format "Month Day, Year"

        end_date: str = "May 31, 2017"
            input end date as the following format "Month day, Year"


        limit: int = 5
            input Maxumum number of images want to download; type None if you want to download images daily into the future but need to set the end_date empty as follow end_date=""

        item_type: str = "PSOrthoTile"
            input item type to downoload please refere to planet labs website for further detalis: 
            PSScene:	PlanetScope 3, 4, and 8 band scenes captured by the Dove satellite constellation
            REOrthoTile:	RapidEye OrthoTiles captured by the RapidEye satellite constellation
            REScene:	Unorthorectified strips captured by the RapidEye satellite constellation
            SkySatScene:	SkySat Scenes captured by the SkySat satellite constellation
            SkySatCollect:	Orthorectified scene composite of a SkySat collection
            SkySatVideo:	Full motion videos collected by a single camera from any of the active SkySats
            Landsat8L1G	Landsat8 Scenes: provided by USGS Landsat8 satellite
            Sentinel2L1C:	Copernicus Sentinel-2 Scenes provided by ESA Sentinel-2 satellite

        product_bundle: str = "analytic_sr_udm2"
            please refer to planetlabs website for further details and different options of product_bundle: default is analytic_sr_udm2
            (analytic,analytic_udm2, analytic_3b_udm2, analytic_5b , analytic_5b_udm2 , analytic_8b_udm2, visual, uncalibrated_dn, 
            uncalibrated_dn_udm2, basic_analytic, basic_analytic_udm2, basic_analytic_8b_udm2, basic_uncalibrated_dn,
            basic_uncalibrated_dn_udm2, analytic_sr, analytic_sr_udm2, analytic_8b_sr_udm2, basic_analytic_nitf, 
            basic_panchromatic, basic_panchromatic_dn, panchromatic, panchromatic_dn, panchromatic_dn_udm2,
            pansharpened, pansharpened_udm2 , basic_l1a_dn)

        clear_percent: int = 90
            Quality of the scene, if you need to download best images keep this value min 90. although, it will end up with less image acquistion 

        cloud_filter: float = 0.1
            cloud percentage

        output_folder: str = "raw_data"
            output directory to save the orders

        clip_flag: bool
            True to clip the downloads to Area of interest json file format provided above
             

        download_data: bool 
            True to download the data or False to preview the data


    '''
    
    

    #############
    # if your Planet API Key is not set as an environment variable, you can paste it below

    planet_api_key=planet_api_key
    if planet_api_key in os.environ:
        API_KEY = os.environ[planet_api_key]
    else:
        API_KEY = planet_api_key
        os.environ['PL_API_KEY'] = API_KEY
        
        
    # Setup the session
    session = requests.Session()

    # Authenticate


    #client = Auth.from_key(API_KEY)
    session.auth = (API_KEY, "")

    #########
    #orders_url = 'https://api.planet.com/compute/ops/orders/v2' 

    ############
    # response = requests.get(orders_url, auth=session.auth)
    # response
    # orders = response.json()['orders']
    # len(orders)


    ############



    # We will also create a small helper function to print out JSON with proper indentation.
    def indent(data):
        print(json.dumps(data, indent=2))

    #Searching
    #We can search for items that are interesting by using the quick_search member function. Searches,
    #however, always require a proper request that includes a filter that selects the specific items to return as seach results.
    
    with open(AOI) as f:
        geom = json.loads(f.read())
    base_name = os.path.basename(AOI)
    task_name = os.path.splitext(base_name)[0]
    #Shapefile AOI

    ######

    # Define the filters we'll use to find our data

    #item_types = [ "PSOrthoTile"]

    geom_filter = data_filter.geometry_filter(geom)
    clear_percent_filter = data_filter.range_filter('clear_percent', clear_percent)
    date_string_start = start_date  # Example string representing a date in "month, day, year" format
    format_string = "%B %d, %Y"  # Format of the input string
    datetime_object_start = datetime.strptime(date_string_start, format_string)

    
    if end_date=="":
        date_range_filter = data_filter.date_range_filter("acquired", gte=  datetime_object_start)
    else:
        date_string_end = end_date  # Example string representing a date in "month, day, year" format
        format_string = "%B %d, %Y"  # Format of the input string
        datetime_object_end = datetime.strptime(date_string_end, format_string)

        date_range_filter = data_filter.date_range_filter("acquired",  gt=  datetime_object_start, lte=datetime_object_end)

    #Date Filter range
    Date_Range_Filter2={
    "type":"DateRangeFilter",
    "field_name":"acquired",
    "config":{
        "gt":"2019-12-31T00:00:00Z",
        "lte":"2020-05-05T00:00:00Z"
    }
    }
    cloud_cover_filter = data_filter.range_filter('cloud_cover', None, cloud_filter)

    combined_filter = data_filter.and_filter([geom_filter, clear_percent_filter, date_range_filter, cloud_cover_filter])

    async with Session() as sess:
        cl = sess.client('data')
        request = await cl.create_search(name='planet_client_demo',search_filter=combined_filter, item_types=[item_type])
        
    async with Session() as sess:
        cl = sess.client('data')
        items = cl.run_search(search_id=request['id'], limit=limit)
        item_list = [i async for i in items]
        
    #####################################
    
    item_ids=[item['id'] for item in item_list]

    print ("\033[1m Number of Items to Download: \033[1m", len(item_ids),  "\n" +" \033[1m Set download_data=True to download the results...\033[1m")
    for item in item_list:
            print(item['id'], item['properties']['item_type'])


    

    print ("\033[1m Number of Items to Download: \033[1m", len(item_ids),  "\n" +" \033[1m Strat Downloading...\033[1m")

    


    #########################

    ################
    # define the clip tool
    clip = {
        "clip": {
            "aoi": geom
        }
    }

    single_product = [
        {
        "item_ids": item_ids,
        "item_type": "PSScene",
        "product_bundle": "analytic_sr_udm2"
        }
    ]
    same_src_products = [
        {
        "item_ids":item_ids,
        "item_type": item_type,
        "product_bundle": product_bundle
        }
    ]
    multi_src_products = [
        {
        "item_ids": item_ids,
        "item_type": "PSScene",
        "product_bundle": "analytic_udm2"
        },
        {
        "item_ids": item_ids,
        "item_type": "PSOrthoTile",
        "product_bundle": "analytic_sr_udm2"
        },
        
    ]
    # create an order request with the clipping tool
    if clip_flag==False:
        request_clip = {
    "name": "just clip",
    "products": same_src_products,
    "delivery": {  
        "archive_type": "zip",
        "archive_filename": "{{name}}_{{order_id}}.zip"
    }
    }

    else:
            
        request_clip = {
        "name": task_name,
        "products": same_src_products,
        "tools": [clip], "delivery": {  
            "archive_type": "zip",
            "archive_filename": "{{name}}_{{order_id}}.zip"
        }
        }

    output_folder=output_folder+"_"+task_name
    from planet import Auth, reporting
    async def poll_and_download(order):
        async with Session() as sess:
            cl = OrdersClient(sess)

            # Use "reporting" to manage polling for order status
            with reporting.StateBar(state='creating') as bar:
                # Grab the order ID
                bar.update(state='created', order_id=order['id'])

                # poll...poll...poll...
                
                try:

                    await cl.wait(order['id'], callback=bar.update_state, max_attempts=2000)
                except:
                    pass
                try:

                # if we get here that means the order completed. Yay! Download the files.
                    filenames = await cl.download_order( order_id=order['id'], directory=output_folder, overwrite=False,  progress_bar=True)
                except:
                    pass

    async with Session() as sess:

        max_attempts = len(item_ids)
        print("Check for bad items...")
        errors_list= []
        cl = OrdersClient(sess)
        for attempt in range(max_attempts):

            try:
                
                # Setup the session
                # session = requests.Session()
                # # # set content type to json
                # headers = {'content-type': 'application/json'}
                # orders_url = 'https://api.planet.com/compute/ops/orders/v2'
                # response = requests.post(orders_url, data=json.dumps(request_clip), auth=session.auth, headers=headers)
                # print(response)
                # order = response.json()['id']

                order = await cl.create_order(request_clip)

                #download =  await poll_and_download(order)
            except planet.exceptions.APIError as e:
                print(e)
                errors_list.append(str(e))
                # Remove the items from the list that are present in the assets_in_errors list
                

                #print ("new_list", len(errors_list_dict), print(errors_list_dict))
            
                pass
        
            # Extract the assets from the error messages
            
            print(errors_list)
            
            # Convert the JSON string to a Python object
            #error_dicts = [json.loads(s) for s in errors_list]

            
            # Convert the JSON strings to Python dictionaries
            dictionaries = [json.loads(json_string) for json_string in errors_list]

            # Function to recursively extract all values from a dictionary
            def extract_values(obj):
                if isinstance(obj, dict):
                    for value in obj.values():
                        if value is not None:
                            yield from extract_values(value)
                elif isinstance(obj, list):
                    for item in obj:
                        if item is not None:
                            yield from extract_values(item)
                else:
                    yield obj

            # Extract all values from the dictionaries
            all_values = []
            for dictionary in dictionaries:
                all_values.extend(list(extract_values(dictionary)))

            # Check if any keyword is in any of the values
            bad_ids = [keyword for keyword in item_ids if any(keyword in value for value in all_values)]

            print('Matches found:', bad_ids)

                # # Initialize an empty list to store the IDs
                # bad_ids = []

                # # Go through each error message in each dictionary
                # for error_dict in error_dicts:
                #     for detail in error_dict["field"]["Details"]:
                #         message = detail["message"]
                #         # Extract the ID from the message
                #         id = message.split('Bundle type/')[1].split('/')[0]
                #         # Add the ID to the list
                #         bad_ids.append(id)
                

            print("bad items has been removed from the item list to avoid api error: \n", bad_ids)
            item_ids_updated = [item for item in item_ids if item not in bad_ids]

            print("Below is list of final items to be downloaded \n " "Number of Items: ", len(item_ids_updated), "\n",  item_ids_updated)


            same_src_products = [
            {
            "item_ids":item_ids_updated,
            "item_type": item_type,
            "product_bundle": product_bundle
            }
                ]

            
            if clip_flag==False:
                request_clip = {
            "name": "just clip",
            "products": same_src_products,
            "delivery": {  
                "archive_type": "zip",
                "archive_filename": "{{name}}_{{order_id}}.zip"
            }
            }

            else:
                    
                request_clip = {
                "name": task_name,
                "products": same_src_products,
                "tools": [clip], "delivery": {  
                    "archive_type": "zip",
                    "archive_filename": "{{name}}_{{order_id}}.zip"
                }
                }


                
        order = await cl.create_order(request_clip)

        if download_data==True:
            download =  await poll_and_download(order)
            
            
        print("Downloading Data is Completed :D")
    #task1=asyncio.current_task(await download_planet())
       

        def search_and_move_zip_files(source_folder, destination_folder):
            # Iterate through all files and directories within the source folder
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    # Check if the file is a zip file
                    if file.endswith('.zip'):
                        # Get the full path of the zip file
                        zip_file_path = os.path.join(root, file)
                        
                        # Move the zip file to the destination folder
                        shutil.move(zip_file_path, destination_folder)

    
        

        # Specify the directory path
        directory_path = Path("zip_folders")

        # Create the directory
        directory_path.mkdir(parents=True, exist_ok=True)
        # Specify the source folder to search for zip files
        source_folder = output_folder

        # Specify the destination folder to move the zip files
        destination_folder = directory_path

        # Call the function to search and move zip files
        search_and_move_zip_files(source_folder, destination_folder)


def akhdefo_orthorectify(input_Dir: str, dem_path: str, output_path: str, ortho_usingRpc: bool, file_ex=".tif"):
    
    ''' 
    Parameteres
    ===========
    input_Dir: str
        input unortho image directory path
    
    dem_path: str 
        input path to DEM file
    
    output_path: str
        input path to output directory
    
    ortho_usingRpc: bool
        Use of RPC file for raw none-georectified satallite images
     
    
    '''
    

    # Define the paths to your image, DEM, and output
    #input_Dir = glob.glob(input_Dir +"/"+ "*.tif")

    

    def get_file_paths(directory):
        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(file_ex):
                    file_paths.append(os.path.join(root, file))
        return file_paths

    # replace 'your_directory_path' with the path to the directory you want to iterate through
    input_Dir = get_file_paths(input_Dir)
    if not os.path.exists(output_path):
            os.makedirs(output_path)
    
    for n in range(len(input_Dir)):
        image_path=input_Dir
        print(image_path[n], n)
        file_name = os.path.basename(image_path[n])
        
        output_path1 = output_path +"/"+ file_name
        print(output_path)

        # Open the DEM
        dem_ds = gdal.Open(dem_path)

        # Get the coordinate system of the DEM
        dem_srs = osr.SpatialReference()
        dem_srs.ImportFromWkt(dem_ds.GetProjectionRef())

        # Define the gdalwarp options
        warp_options = gdal.WarpOptions(
            format='GTiff',
            rpc=ortho_usingRpc,
            outputType=gdal.GDT_UInt16,
            multithread=True,
            creationOptions=['COMPRESS=DEFLATE', 'TILED=YES'],
            dstSRS=dem_srs.ExportToProj4(),
            srcNodata=0,
            dstNodata=0,
            resampleAlg='cubic',
        )

        # Open the source image
        src_ds = gdal.Open(image_path[n])

        # Perform the orthorectification
        dst_ds = gdal.Warp(output_path1, src_ds, options=warp_options, cutlineDSName=dem_path)

    #Clean up
    src_ds = None
    dem_ds = None
    dst_ds = None



import asf_search as asf
import hyp3_sdk as sdk
import pandas as pd

def download_RTC(username: str = '', password: str = '', prompt=False, asf_datapool_results_file: str = '', save_dir: str = '',
                 job_name: str = 'rtc-test', dem_matching: bool = True, include_dem: bool = True,
                 include_inc_map: bool = True, include_rgb: bool = False, 
                 include_scattering_area: bool = False, scale: str = 'amplitude',
                 resolution: int = 10, speckle_filter: bool = True, radiometry='gamma0', dem_name='copernicus',
                   download: bool=False):
    """
    Downloads RTC from a provided ASF datapool results file.
    
    Args:
        username (str): ASF Hyp3 username.
        password (str): ASF Hyp3 password.
        asf_datapool_results_file (str): Path to ASF datapool results CSV file.
        save_dir (str): Directory where downloaded files will be saved.
        job_name (str, optional): Name for the job. Default is 'rtc-test'.
        dem_matching (bool, optional): Coregisters SAR data to the DEM, rather than using dead reckoning based on orbit files. If True, perform DEM matching. Default is True.
        include_dem (bool, optional): If True, include Digital Elevation Model. Default is True.
        include_inc_map (bool, optional): If True, include incidence angle map. Default is True.
        include_rgb (bool, optional): If True, include RGB decomposition. Default is True.
        include_scattering_area (bool, optional): If True, include scattering area. Default is True.
        scale (str, optional): Scale for the image. Default is 'amplitude'.
        resolution (int, optional): Desired resolution. Default is 10.
        speckle_filter (bool, optional): Apply an Enhanced Lee speckle filter. If True, apply speckle filter. Default is True.
        radiometry: Backscatter coefficient normalization, either by ground area (sigma0) or illuminated area projected into the look direction (gamma0)
        dem_name (str): Name of the DEM to use for processing. copernicus will use the Copernicus GLO-30 Public DEM, while legacy will use the DEM with the best coverage from ASF's legacy SRTM/NED datasets.

    Returns:
        A Batch object containing the RTC job

   
    """

    if prompt==True:
        if not asf_datapool_results_file or not save_dir:
            raise ValueError("asf_datapool_results_file, and save_dir are required.")

        hyp3 = sdk.HyP3(prompt=prompt)
    else:
            
        # Check if required parameters are provided
        if not username or not password or not asf_datapool_results_file or not save_dir:
            raise ValueError("Username, password, asf_datapool_results_file, and save_dir are required.")

        # Establish connection
        hyp3 = sdk.HyP3(username=username, password=password)

    # Read ASF datapool results file
    df = pd.read_csv(asf_datapool_results_file)
    granule_names = df['Granule Name'].tolist()

    # Select first two granules
    granules_to_download = granule_names
    

    # Initialize job batch
    rtc_jobs = sdk.Batch()
    
    if download==True:
        print(f"Downloading granules: {granules_to_download}")

        # Submit jobs for each granule
        for granule in granules_to_download:
            rtc_jobs += hyp3.submit_rtc_job(granule, name=job_name, dem_matching=dem_matching, 
                                            include_dem=include_dem, include_inc_map=include_inc_map,
                                            include_rgb=include_rgb, 
                                            include_scattering_area=include_scattering_area,
                                            scale=scale, resolution=resolution, 
                                            speckle_filter=speckle_filter, radiometry=radiometry, dem_name=dem_name)
        print(f"Submitted jobs: {rtc_jobs}")

        # Monitor job progress and wait until completion
        rtc_jobs = hyp3.watch(rtc_jobs)

        # Download completed jobs to the specified location
        rtc_jobs.download_files(location=save_dir, create=True)
    else:
        print(f"set value download= {download} to True to submit the jobs and download RTC data")
        print(f"List of granules: {granules_to_download}")
    
    
    return rtc_jobs


import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterio.mask import mask
from skimage import exposure

def reproject_raster_to_match_shapefile(src_path, dst_path, dst_crs):

    """
    Reproject a raster to match the coordinate reference system (CRS) of a shapefile.

    Parameters:
    - src_path (str): Path to the source raster file that needs to be reprojected.
    - dst_path (str): Path to save the reprojected raster.
    - dst_crs (CRS or str): Target coordinate reference system.

    Returns:
    None. The reprojected raster is written to dst_path.
    """

    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(dst_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)

def create_vegetation_mask(red_band_path, nir_band_path, output_path, shapefile_path, threshold=0.3, save_plot=False, plot_path="plot.png"):
    
    """
    Create a binary vegetation mask based on the NDVI (Normalized Difference Vegetation Index) calculation.

    Parameters:
    - red_band_path (str): Path to the raster file containing the red band.
    - nir_band_path (str): Path to the raster file containing the near-infrared (NIR) band.
    - output_path (str): Path to save the generated vegetation mask raster.
    - shapefile_path (str): Path to the shapefile that defines the area of interest (AOI).
    - threshold (float, optional): NDVI threshold for determining vegetation. Pixels with NDVI less than this threshold are considered vegetation. Default is 0.3.
    - save_plot (bool, optional): Whether to save a plot of the vegetation mask. Default is False.
    - plot_path (str, optional): Path to save the plot if save_plot is True. Default is "plot.png".

    Returns:
    None. The vegetation mask is written to output_path, and optionally a plot is saved.

    Note:
    The function assumes that the shapefile contains only one geometry.
    """

    # Read the AOI from the shapefile
    aoi_gdf = gpd.read_file(shapefile_path)
    geometry = aoi_gdf.geometry[0]  # Assuming only one geometry in the shapefile

    target_crs = aoi_gdf.crs

    # Reproject the rasters to match the CRS of the shapefile
    reprojected_red_band_path = "reprojected_red.tif"
    reprojected_nir_band_path = "reprojected_nir.tif"

    reproject_raster_to_match_shapefile(red_band_path, reprojected_red_band_path, target_crs)
    reproject_raster_to_match_shapefile(nir_band_path, reprojected_nir_band_path, target_crs)

    # Open and crop the reprojected red band using the AOI
    with rasterio.open(reprojected_red_band_path) as red_src:
        red_crop, red_transform = mask(red_src, [geometry], crop=True)

    # Open and crop the reprojected near-infrared band using the AOI
    with rasterio.open(reprojected_nir_band_path) as nir_src:
        nir_crop, _ = mask(nir_src, [geometry], crop=True)

    # Calculate NDVI
    # Using a small value (1e-8) in the denominator to prevent division by zero
    ndvi = (nir_crop - red_crop) / (nir_crop + red_crop )

   # Use the rescale_intensity function from skimage's exposure module
    #ndvi = exposure.rescale_intensity(ndvi, out_range=(-1, 1))


    # Create a binary vegetation mask
    vegetation_mask = (ndvi < threshold)
    
    

    # Prepare metadata for the output raster
    meta = red_src.meta.copy()
    meta.update({
        "height": red_crop.shape[1],
        "width": red_crop.shape[2],
        "transform": red_transform
    })

    # Save the vegetation mask raster
    with rasterio.open(output_path, 'w', **meta) as dest:
        dest.write(vegetation_mask)

    if save_plot:
        plt.colorbar(plt.imshow(vegetation_mask[0], cmap='gray'))
        plt.axis('off')
        plt.savefig(plot_path, bbox_inches='tight', pad_inches=0)
        plt.show()

    print(f"Vegetation mask created and saved to {output_path}")