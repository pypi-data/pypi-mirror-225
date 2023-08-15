def utm_to_latlon(easting, northing, zone_number, zone_letter):
    '''
    This program converts geographic projection of shapefiles from UTM to LATLONG
    
    Parameters
    ----------
    easting: Geopandas column with Easting 
    
    northing: Geopandas column with Northing
    
    zone_number: int
    
    zone_letter: "N" or "S"
    
    Returns
    -------
    [lon , lat ]: List

    '''
    import geopandas as gpd
    import utm
    easting = easting
    northing = northing
    lon, lat=utm.to_latlon(easting, northing, zone_number, zone_letter)
    
    return [lon, lat]

import os
import numpy as np
from osgeo import gdal, osr

import os
import rasterio
from rasterio.transform import Affine
import numpy as np

def flip_geotiff_180(directory):
    # List all files in the directory
    for filename in os.listdir(directory):
        # Only process files with the .tif extension
        if filename.endswith(".tif"):
            filepath = os.path.join(directory, filename)

            # Open the file
            with rasterio.open(filepath) as src:
                # Read the image data
                data = src.read()
                # Define the transform
                transform = src.transform

            # Flip the data array upside down (180 degree rotation)
            data = np.flipud(data)

            # Update the transform
            transform = Affine(transform.a, transform.b, transform.c, transform.d, -transform.e, src.height * transform.e + transform.f)

            # Write the data to the same file, overwriting the original
            with rasterio.open(filepath, 'w', driver='GTiff', height=data.shape[1], width=data.shape[2], count=data.shape[0], dtype=data.dtype, crs=src.crs, transform=transform) as dst:
                dst.write(data)


def assign_fake_projection(input_dir, output_dir):
    '''
    Note
    ====

    This program assigns fake latlon geographic coordinates to ground-based images 
    so that it can be ingest using gdal and rasterio geospatial libraries for further processing
    
    input_dir: str
        path to image directories without projection info
    
    output_dir: str
        output path image directory for images included projection info

    
    '''
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List of valid extensions
    valid_extensions = ['.tif', '.jpg', '.png', '.bmp']

    # # Create a "fake" Spatial Reference object for source
    # source_srs = osr.SpatialReference()
    # source_srs.SetWellKnownGeogCS('LOCAL_CS')  # 'LOCAL_CS' is a placeholder coordinate system
    # Create a Spatial Reference object for source
    source_srs = osr.SpatialReference()
    source_srs.SetWellKnownGeogCS('WGS84')  # WGS84 is a commonly used geodetic coordinate system
    from scipy import ndimage
    # Iterate over all files in the directory
    for filename in os.listdir(input_dir):
        # Check if the file has a valid extension
        if os.path.splitext(filename)[1] in valid_extensions:
            # Define the full path to the input raster
            input_raster_path = os.path.join(input_dir, filename)

            # Open the raster
            ds = gdal.Open(input_raster_path, gdal.GA_ReadOnly)

            # Read the raster data
            data = ds.ReadAsArray()

            # Rotate array by 45 degrees
            #data = ndimage.rotate(data, 180)

            # Define the full path to the output raster
            # We keep the original filename but put it into the output_dir
            output_raster_path = os.path.join(output_dir, filename[:-4]+".tif")

            # Create a new raster dataset with the same dimensions
            driver = gdal.GetDriverByName('GTiff')
            out_ds = driver.Create(output_raster_path, ds.RasterXSize, ds.RasterYSize, ds.RasterCount, ds.GetRasterBand(1).DataType)

            # Assign the "fake" projection and the same geotransform
            out_ds.SetProjection(source_srs.ExportToWkt())
            out_ds.SetGeoTransform(ds.GetGeoTransform())

             # Assign the WGS84 projection and the same geotransform
            out_ds.SetProjection(source_srs.ExportToWkt())
            out_ds.SetGeoTransform(ds.GetGeoTransform())

            # Write the data to the new raster
            for i in range(ds.RasterCount):
                out_band = out_ds.GetRasterBand(i+1)
                out_band.WriteArray(data[i])

            # Close the datasets
            ds = None
            out_ds = None
    for filename in os.listdir(output_dir):
        # Only process files with the .tif extension
        if filename.endswith(".tif"):
            filepath = os.path.join(output_dir, filename)

            # Open the file
            with rasterio.open(filepath) as src:
                # Read the image data
                data = src.read()
                # Define the transform
                transform = src.transform

            # Flip the data array upside down (180 degree rotation)
            data = np.flipud(data)

            # Update the transform
            transform = Affine(transform.a, transform.b, transform.c, transform.d, -transform.e, src.height * transform.e + transform.f)

            # Write the data to the same file, overwriting the original
            with rasterio.open(filepath, 'w', driver='GTiff', height=data.shape[1], width=data.shape[2], count=data.shape[0], dtype=data.dtype, crs=src.crs, transform=transform) as dst:
                dst.write(data)  
import os
import shutil
import re

def move_files(base_directory):
    """
    This function reorganizes files in the specified directory. 
    It searches for timestamps in filenames, creates subdirectories based on the hour part of the timestamp,
    and moves files to the appropriate subdirectories. The files are renamed based on the year, month, and day of the timestamp.
    
    Args:
        base_directory (str): Path of the directory containing the files to be reorganized.

    """

    # List of regex patterns for different timestamp formats
    timestamp_patterns = [
        r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})\.',  # yyyymmddhhmmss
        r'(?P<year>\d{2})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})\.',  # yymmddhh
        r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})\.',  # yyyymmdd
        r'(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})\.',  # hhmmss
        r'(?P<hour>\d{2})\.'  # hh
        # Add more patterns as necessary
    ]

    for filename in os.listdir(base_directory):
        # If the file is not a file, skip
        if not os.path.isfile(os.path.join(base_directory, filename)):
            continue

        # Extract the timestamp from the filename
        for pattern in timestamp_patterns:
            match = re.search(pattern, filename)
            if match:
                year = match.groupdict().get('year', '0000')
                month = match.groupdict().get('month', '00')
                day = match.groupdict().get('day', '00')
                hour = match.group('hour')
                break
        else:
            print(f"No timestamp found in file {filename}.")
            continue

        # Construct new filename based on date and existing extension
        base, extension = os.path.splitext(filename)
        new_filename = f"{year}-{month}-{day}{extension}"

        # Make directory for this hour if it doesn't exist
        hour_dir = os.path.join(base_directory, hour)
        if not os.path.exists(hour_dir):
            os.makedirs(hour_dir)

        # Move and rename file to the corresponding hour folder
        shutil.move(os.path.join(base_directory, filename), os.path.join(hour_dir, new_filename))



from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras import backend as K

class LeNet:
    @staticmethod
    def build(width, height, depth, classes):
        # initialize the model
        model = Sequential()
        inputShape = (height, width, depth)

        # if we are using "channels first", update the input shape
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)

        # first set of CONV => RELU => POOL layers
        model.add(Conv2D(20, (5, 5), padding="same",
            input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # second set of CONV => RELU => POOL layers
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        # return the constructed network architecture
        return model

def Lenet_Model_training(dataset="DataForTraining", model_out="foggy_not_foggy.model", plot="Model_stat_plot.png", EPOCHS = 100,
    INIT_LR = 1e-3,  BS = 32):

    '''

    This function, Lenet_Model_train(), is designed to train a convolutional neural network (CNN) using the LeNet architecture. The network is trained on a dataset of images to classify whether they are "foggy" or "not foggy".

    Parameters:
    -----------

    dataset: str
      (default="DataForTraining") Path to the directory containing the image data for training. The images are expected to be in separate directories named after their corresponding class ("foggy" or "not foggy").
    model_out: str
      (default="foggy_not_foggy.model") The name or path for the output file where the trained model will be saved in the h5 format.
    plot: str
     (default="Model_stat_plot.png") The name or path for the output image file where a plot of the training loss and accuracy will be saved.
    EPOCHS: int
      (default=100)The number of epochs to use for training.
    INIT_LR: float
      (default=1e-3)The initial learning rate for the Adam optimizer.
    BS: int
      (default=32)The batch size for training.

    Returns:
    --------
    - Trains a LeNet model on the given dataset.
    - Saves the trained model to disk in the h5 format.
    - Plots the training and validation loss and accuracy as a function of epoch number, and saves the plot to disk. The plot also includes the model summary.
    - Note: The function uses data augmentation techniques during training, including random rotations, width and height shifts, shearing, zooming, and horizontal flipping.
    - This function uses the TensorFlow, Keras, OpenCV, and matplotlib libraries.

    '''
            
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.optimizers import Adam
    from sklearn.model_selection import train_test_split
    from tensorflow.keras.preprocessing.image import img_to_array
    from tensorflow.keras.utils import to_categorical
    import matplotlib.pyplot as plt
    import numpy as np
    import argparse
    import random
    import cv2
    import os
    from imutils import paths
    #from mahmud_ml.lenet import LeNet

    

    dataset=dataset
    model=model_out
    plot=plot
    

    # initialize the number of epochs to train for, initial learning rate, and batch size
    EPOCHS = EPOCHS
    INIT_LR = INIT_LR
    BS = BS

    # initialize the data and labels
    print("[INFO] loading images...")
    data = []
    labels = []

    # grab the image paths and randomly shuffle
    imagePaths = sorted(list(paths.list_images(dataset)))
    random.seed(42)
    random.shuffle(imagePaths)

    # loop over the input images
    for imagePath in imagePaths:
        # load the image, pre-process it, and store it in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (28, 28))
        image = img_to_array(image)
        data.append(image)

        # extract the class label from the image path and update the labels list
        label = imagePath.split(os.path.sep)[-2]
        label = 1 if label == "foggy" else 0
        labels.append(label)

    # scale the raw pixel intensities to the range [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # partition the data into training and testing splits using 75% of the data for training and the remaining 25% for testing
    (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)

    # convert the labels from integers to vectors
    trainY = to_categorical(trainY, num_classes=2)
    testY = to_categorical(testY, num_classes=2)

    # construct the image generator for data augmentation
    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")

    # initialize the model
    print("[INFO] compiling model...")
    model = LeNet.build(width=28, height=28, depth=3, classes=2)
    opt = Adam(learning_rate=INIT_LR)
    model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

    # train the network
    print("[INFO] training network...")
    H = model.fit(x=aug.flow(trainX, trainY, batch_size=BS), validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS, epochs=EPOCHS, verbose=1)

    # save the model to disk
    print("[INFO] serializing network...")
    model.save(model_out, save_format="h5")

    #############

    from tensorflow.keras.models import load_model

    # Load the model
    model = load_model(model_out)

    # # Print model summary
    # print("\nModel Summary:")
    #model.summary()

    import matplotlib.pyplot as plt
    import io
    import re

    # Save the summary to a string
    stream = io.StringIO()
    model.summary(print_fn=lambda x: stream.write(x + '\n'))
    summary_string = stream.getvalue()
    stream.close()

    # Preprocess the string to remove unwanted characters
    summary_string = re.sub('_+', '', summary_string)
    summary_string = re.sub('=+', '', summary_string)


    ###############

    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure(figsize=(15,5))
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy on fog/Not fog")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")


    # Add the summary string as a textbox
    # Add text to figure with a bounding box
    bbox_props = dict(boxstyle="round, pad=0.3", fc="white", ec="k", lw=2, alpha=0.6)
    plt.figtext(0.75, 0.5, summary_string, horizontalalignment='left', verticalalignment='center', fontsize=6, bbox=bbox_props)

    plt.tight_layout()

    plt.savefig(plot)

    plt.show()


from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from os import listdir, makedirs
from os.path import isfile, join
from PIL import Image
from tqdm import tqdm
from os.path import isfile, isdir, join


def classification(input_dir="dataset_imagery", trained_model="foggy_not_foggy.model"):
    """
    Classifies images in the specified directory using a trained model.

    Inputs:
    -------
        - input_dir (str, optional): Path to the directory containing the input images. Defaults to "dataset_imagery".
        - trained_model (str, optional): Path to the trained model file. Defaults to "foggy_not_foggy.model".

    

    Returns:
    --------
        - The function assumes that the input directory contains image files in JPG format.
        - The function uses a trained convolutional neural network model to classify the images.
        - It saves the classified images into separate directories based on their classification.

    
    """
    # Setting required file directories
    dir_list = ['filtered_images_noFog', 'filtered_images_Fog', 'ClearImages_daily']
    for directory in dir_list:
        if not isdir(directory):
            try:
                makedirs(directory)
            except OSError as e:
                raise OSError(f"Error creating directory '{directory}': {e}")

    No_Fogg_path = "filtered_images_noFog"
    Foggy_Path = "filtered_images_Fog"
    dailyimages = "ClearImages_daily"
    mypath = input_dir

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    images = np.empty(len(onlyfiles), dtype=object)

    # Load the trained convolutional neural network outside of loop
    model = load_model(trained_model)

    # Loop through each image and use tqdm for progress bar
    pbar = tqdm(range(len(onlyfiles)), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', colour='#00ff00', dynamic_ncols=True)

    for n in pbar:
        pbar.set_description(f"Processing image {n + 1}")
        image_path = join(mypath, onlyfiles[n])

        image = cv2.imread(image_path)
        orig = image.copy()

        # Pre-process the image for classification
        image = cv2.resize(image, (28, 28))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = image.astype("float") / 255.0

        # Classify the input image
        (not_foggy, foggy) = model.predict(image)[0]
        label = "NotFoggy" if not_foggy > foggy else "Foggy"
        proba = not_foggy if not_foggy > foggy else foggy
        label = f"{label}: {proba * 100:.2f}%"

        cv2.putText(orig, label, (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        im = Image.fromarray(orig)

        file = str(onlyfiles[n])
        position = file.index(".jpg")
        filename = file[:position]

        if proba > 0.95 and not_foggy > foggy:
            label = "Not Foggy"
            im.save(join(No_Fogg_path, f"{proba}-{filename}.jpg"))
            im.save(join(dailyimages, f"{filename}.jpg"))
        else:
            label = "Foggy"
            im.save(join(Foggy_Path, f"{proba}-{filename}.jpg"))

    print("\nNo more files left to process")  # Print final message on a new line


import numpy as np
import rasterio
from rasterio.transform import Affine
import matplotlib.pyplot as plt

def calculate_volume(elevation_map, slope_map, cell_size, output_file, plot_map=False, plot_file=None):
    """
    Calculate the volume based on an elevation map and a slope map,
    and save the volume map as a GeoTIFF file. Optionally, plot the volume map as a figure and save it.

    Args:
        elevation_map (str): File path to the elevation map raster.
        slope_map (ndarray): 2D array representing the slope values.
        cell_size (float): Size of each cell in the map (e.g., length of one side of a square cell).
        output_file (str): Output file path for saving the volume map as a GeoTIFF.
        plot_map (bool, optional): Whether to plot the volume map as a figure. Default is False.
        plot_file (str, optional): Output file path for saving the volume map plot. Required if plot_map is True.

    Returns:
        ndarray: The calculated volume map.

    """
    # Read elevation map raster using rasterio
    src= rasterio.open(elevation_map)
    # Get CRS from elevation_map
    crs = src.crs

    # Get transform from elevation_map
    transform = src.transform

     # Read elevation map data
    elevation_data = src.read(1)

     # Read elevation map raster using rasterio
    src1= rasterio.open(slope_map)
        
     # Read slope_map data
    slope_data = src.read(1)

    # Calculate the dimensions of the maps
    rows, cols = elevation_data.shape

    # Initialize the volume map
    volume_map = np.zeros_like(elevation_data, dtype=float)

    # Iterate over each cell in the maps
    for i in range(rows):
        for j in range(cols):
            # Calculate the cell area
            area = cell_size ** 2

            # Calculate the cell volume contribution
            volume_map[i, j] += elevation_data[i, j] * area

            # Calculate the slope gradient
            slope_gradient = np.tan(np.radians(slope_data[i, j]))

            # Calculate the additional volume due to the slope
            volume_map[i, j] += 0.5 * slope_gradient * area

    # Save volume map as GeoTIFF
    with rasterio.open(output_file, "w", driver="GTiff", height=volume_map.shape[0], width=volume_map.shape[1], count=1, dtype=volume_map.dtype, crs=crs, transform=transform) as dst:
        dst.write(volume_map, 1)

    # Plot and save volume map if desired
    if plot_map:
        plt.imshow(volume_map, cmap='viridis')
        plt.colorbar(label='Volume')
        plt.title('Volume Map')
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.show()

    return volume_map




# def ts_plot(df, plot_number, save_plot=False , output_dir="", plot_filename="" , VEL_Scale='year'):


#     import plotly.graph_objects as go
#     import plotly.express as px
#     import plotly.express as px_temp
#     import pandas as pd
#     import numpy as np
#     import matplotlib.pyplot as plt
#     import geopandas as gpd 
#     import pandas as pd  
#     import seaborn as sns  
#     import plotly.offline as py_offline
#     import os   
#     import statsmodels.api as sm
#     from sklearn.metrics import mean_squared_error, r2_score
#     import numpy as np
#     from sklearn.linear_model import LinearRegression
#     from datetime import datetime
#     import math
    
#     py_offline.init_notebook_mode()
#     #%matplotlib widget
#     #df=pd.read_csv("temp.csv")
#     df.rename(columns={ df.columns[0]: "dd" }, inplace = True)
#     df['dd_str']=df['dd'].astype(str)
#     df['dd_str'] = df['dd_str'].astype(str)
#     df.rename(columns={ df.columns[1]: "val" }, inplace = True)
#     df['dd']= pd.to_datetime(df['dd'].astype(str), format='%Y%m%d')
    
#     df=df.set_index('dd')
    
#     ########################
#     df=df.dropna()
#     # Make index pd.DatetimeIndex
#     df.index = pd.DatetimeIndex(df.index)
#     # Make new index
#     idx = pd.date_range(df.index.min(), df.index.max())
#     # Replace original index with idx
#     df = df.reindex(index = idx)
#     # Insert row count
#     df.insert(df.shape[1],
#             'row_count',
#             df.index.value_counts().sort_index().cumsum())

#     df=df.dropna()
    
#     #df=df.set_index(df['row_count'], inplace=True)

#     df.sort_index(ascending=True, inplace=True)
    

#     def best_fit_slope_and_intercept(xs,ys):
#         from statistics import mean
#         xs = np.array(xs, dtype=np.float64)
#         ys = np.array(ys, dtype=np.float64)
#         m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
#             ((mean(xs)*mean(xs)) - mean(xs*xs)))
        
#         b = mean(ys) - m*mean(xs)
        
#         return m, b

    

#     #convert dattime to number of days per year
    
    
    

#     dates_list=([datetime.strptime(x, '%Y%m%d') for x in df.dd_str])
#     days_num=[( ((x) - (pd.Timestamp(year=x.year, month=1, day=1))).days + 1) for x in dates_list]
#     time2=days_num[len(days_num)-1]
#     time1=days_num[0]
#     delta=time2-time1
#     delta=float(delta)
#     print(days_num, delta)
    
#     m, b = best_fit_slope_and_intercept(df.row_count, df.val)
#     print("m:", math.ceil(m*100)/100, "b:",math.ceil(b*100)/100)
#     regression_model = LinearRegression()
#     val_dates_res = regression_model.fit(np.array(days_num).reshape(-1,1), np.array(df.val))
#     y_predicted = regression_model.predict(np.array(days_num).reshape(-1,1))
    
#     if VEL_Scale=='year':
#         rate_change=regression_model.coef_[0]/delta * 365.0
#     elif VEL_Scale=='month':
#         rate_change=regression_model.coef_[0]/delta * 30
        
#     # model evaluation
#     mse=mean_squared_error(np.array(df.val),y_predicted)
#     rmse = np.sqrt(mean_squared_error(np.array(df.val), y_predicted))
#     r2 = r2_score(np.array(df.val), y_predicted)
    
#     # printing values
#     print('Slope(linear deformation rate):' + str(math.ceil(regression_model.coef_[0]*100)/100/delta) + " mm/day")
#     print('Intercept:', math.ceil(b*100)/100)
#     #print('MSE:',mse)
#     print('Root mean squared error: ', math.ceil(rmse*100)/100)
#     print('R2 score: ', r2)
#     print("STD: ",math.ceil(np.std(y_predicted)*100)/100) 
#     # Create figure
#     #fig = go.Figure()
    
#     fig = go.FigureWidget()
    
#     plot_number="Plot Number:"+str(plot_number)

#     fig.add_trace(go.Scatter(x=list(df.index), y=list(df.val)))
#     fig = px.scatter(df, x=list(df.index), y=list(df.val),
#                 color="val", hover_name="val"
#                     , labels=dict(x="Dates", y="mm/"+VEL_Scale , color="mm/"+VEL_Scale))
    
#     # fig.add_trace(
#     # go.Scatter(x=list(df.index), y=list(val_fit), mode = "lines",name="trendline", marker_color = "red"))
    
    
    
#     fig.add_trace(go.Scatter(x=list(df.index), y=list(df.val),mode = 'lines',
#                             name = 'draw lines', line = dict(shape = 'linear', color = 'rgb(0, 0, 0)', dash = 'dash'), connectgaps = True))
    
#     fig.add_trace(
#         go.Scatter(x=list(df.index), y=list(y_predicted), mode = "lines",name="trendline", marker_color = "black", line_color='red'))
    
    

#     # Add range slider
#     fig.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1,
#                         label="1m",
#                         step="month",
#                         stepmode="backward"),
#                     dict(count=6,
#                         label="6m",
#                         step="month",
#                         stepmode="backward"),
#                     dict(count=1,
#                         label="YTD",
#                         step="year",
#                         stepmode="todate"),
#                     dict(count=1,
#                         label="1y",
#                         step="year",
#                         stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(
#                 visible=True
#             ),
#             type="date"
#         ) 
#     )
#     fig.update_xaxes(rangeslider_thickness = 0.05)
#     #fig.update_layout(showlegend=True)

#     #fig.data[0].update(line_color='black')
#     tt= "Defo-Rate:"+str(round(rate_change,2))+":"+ "Defo-Rate-STD:"+str(round(np.std(y_predicted), 2))+ ":" +plot_number
    
#     # make space for explanation / annotation
#     fig.update_layout(margin=dict(l=20, r=20, t=20, b=60),paper_bgcolor="LightSteelBlue")

    
#     fig.update_layout(
        
#     title_text=tt, title_font_family="Sitka Small",
#     title_font_color="red", title_x=0.5 , legend_title="Legend",
#     font=dict(
#         family="Courier New, monospace",
#         size=15,
#         color="RebeccaPurple" ))
    
#     fig.update_layout(legend=dict(
#     yanchor="top",
#     y=-0,
#     xanchor="left",
#     x=1.01
# ))

#     # fig.update_layout(
#     # updatemenus=[
#     #     dict(
#     #         type="buttons",
#     #         direction="right",
#     #         active=0,
#     #         x=0.57,
#     #         y=1.2,
#     #         buttons=list([
#     #             dict(
#     #                 args=["colorscale", "Viridis"],
#     #                 label="Viridis",
#     #                 method="restyle"
#     #             ),
#     #             dict(
#     #                 args=["colorscale", "turbo"],
#     #                 label="turbo",
#     #                 method="restyle"
#     #             )
#     #         ]),
#     #     )
#     # ])

    
#     fig.update_xaxes(showspikes=True, spikemode='toaxis' , spikesnap='cursor', spikedash='dot', spikecolor='blue', scaleanchor='y', title_font_family="Arial", 
#                     title_font=dict(size=15))
#     fig.update_yaxes(showspikes=True, spikemode='toaxis' , spikesnap='cursor', spikedash='dot', spikecolor='blue', scaleanchor='x', title_font_family="Arial",
#                     title_font=dict(size=15))

    
    
#     if save_plot==True:
    
#         if not os.path.exists(output_dir):
#             os.mkdir(output_dir)

#         fig.write_html(output_dir + "/" + plot_filename + ".html" )
#         fig.write_image(output_dir + "/" + plot_filename + ".jpeg", scale=1, width=1080, height=300 )
        
    
#     def zoom(layout, xrange):
#         in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
#         fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

#     fig.layout.on_change(zoom, 'xaxis.range')
    
#     fig.show()
    
    




    
#     start=int(start.timestamp() * 1000)
#     end=int(end.timestamp() * 1000)

#     #df=pd.read_csv('temp2.csv')
    
#     df.rename(columns={ df.columns[0]: "dd" }, inplace = True)
#     df['dd_str']=df['dd'].astype(str)
#     df['dd_str'] = df['dd_str'].astype(str)
#     df.rename(columns={ df.columns[1]: "val" }, inplace = True)
#     df['dd']= pd.to_datetime(df['dd'].astype(str), format='%Y-%m-%d')
#     df.insert(df.shape[1],
#             'row_count',
#             df.index.value_counts().sort_index().cumsum())
#     #df=df.set_index('dd')
#     #df.index = pd.DatetimeIndex(df.index)
#     df.dd_str = pd.DatetimeIndex(df.dd_str)
#     df['dd_int'] = [int(i.timestamp()*1000) for i in df.dd_str]
#     import numpy as np 
#     def find_nearest(array, value):
#         array = np.asarray(array)
#         idx = (np.abs(array - value)).argmin()
#         return array[idx]
#     s=find_nearest(np.array(df.dd_int), start)
#     e=find_nearest(np.array(df.dd_int), end)

#     s=(df[df['dd_int']==s].index)
#     e=(df[df['dd_int']==e].index)

#     df_filter=df[s[0]:e[0]]
#     print(df_filter)

#     df=df_filter  
    
# import pandas as pd
# import ipywidgets as widgets
# from IPython.display import display

# class DateRangePicker(object):
#     def __init__(self,start,end,freq='D',fmt='%Y-%m-%d'):
#         """
#         Parameters
#         ----------
#         start : string or datetime-like
#             Left bound of the period
#         end : string or datetime-like
#             Left bound of the period
#         freq : string or pandas.DateOffset, default='D'
#             Frequency strings can have multiples, e.g. '5H' 
#         fmt : string, defauly = '%Y-%m-%d'
#             Format to use to display the selected period

#         """
#         self.date_range=pd.date_range(start=start,end=end,freq=freq)
#         options = [(item.strftime(fmt),item) for item in self.date_range]
#         self.slider_start = widgets.SelectionSlider(
#             description='start',
#             options=options,
#             continuous_update=False
#         )
#         self.slider_end = widgets.SelectionSlider(
#             description='end',
#             options=options,
#             continuous_update=False,
#             value=options[-1][1]
#         )

#         self.slider_start.on_trait_change(self.slider_start_changed, 'value')
#         self.slider_end.on_trait_change(self.slider_end_changed, 'value')

#         self.widget = widgets.Box(children=[self.slider_start,self.slider_end])

#     def slider_start_changed(self,key,value):
#         self.slider_end.value=max(self.slider_start.value,self.slider_end.value)
#         self._observe(start=self.slider_start.value,end=self.slider_end.value)

#     def slider_end_changed(self,key,value):
#         self.slider_start.value=min(self.slider_start.value,self.slider_end.value)
#         self._observe(start=self.slider_start.value,end=self.slider_end.value)

#     def display(self):
#         display(self.slider_start,self.slider_end)

#     def _observe(self,**kwargs):
#         if hasattr(self,'observe'):
#             self.observe(**kwargs)

# def fct(start,end):
#     print (start,end)
    
#     start=int(start.timestamp() * 1000)
#     end=int(end.timestamp() * 1000)

#     df=pd.read_csv('temp2.csv')

#     df.rename(columns={ df.columns[0]: "dd" }, inplace = True)
#     df['dd_str']=df['dd'].astype(str)
#     df['dd_str'] = df['dd_str'].astype(str)
#     df.rename(columns={ df.columns[1]: "val" }, inplace = True)
#     df['dd']= pd.to_datetime(df['dd'].astype(str), format='%Y-%m-%d')
#     df.insert(df.shape[1],
#             'row_count',
#             df.index.value_counts().sort_index().cumsum())
#     #df=df.set_index('dd')
#     #df.index = pd.DatetimeIndex(df.index)
#     df.dd_str = pd.DatetimeIndex(df.dd_str)
#     df['dd_int'] = [int(i.timestamp()*1000) for i in df.dd_str]
#     import numpy as np 
#     def find_nearest(array, value):
#         array = np.asarray(array)
#         idx = (np.abs(array - value)).argmin()
#         return array[idx]
#     s=find_nearest(np.array(df.dd_int), start)
#     e=find_nearest(np.array(df.dd_int), end)

#     s=(df[df['dd_int']==s].index)
#     e=(df[df['dd_int']==e].index)

#     df_filter=df[s[0]:e[0]]
#     print(df_filter)
#     return (start, end)
    
# w=DateRangePicker(start='2022-08-02',end="2022-09-02",freq='D',fmt='%Y-%m-%d')
# w.observe=fct
# w.display()

# #a=fct[0]
# print(w.observe[0])