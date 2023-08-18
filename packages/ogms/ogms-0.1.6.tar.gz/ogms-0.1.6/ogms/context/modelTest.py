#Data : 2018-10-15
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com

from modelservicecontext import EModelContextStatus
from modelservicecontext import ERequestResponseDataFlag
from modelservicecontext import ERequestResponseDataMIME
from modelservicecontext import ModelServiceContext
from modeldatahandler import ModelDataHandler
import sys

import gdal
import numpy as np

from sklearn.tree import DecisionTreeRegressor  
from sklearn.ensemble import RandomForestRegressor  

def makeupTarget(tifpath):
    dataset = gdal.Open(tifpath)
    if dataset == None:
        print('Can not open ' + tifpath)
        return None
    tif_width = dataset.RasterXSize
    tif_height = dataset.RasterYSize
    tif_bandsCount = dataset.RasterCount
    tif_data = dataset.ReadAsArray(0, 0, tif_width, tif_height)
    tif_geotrans = dataset.GetGeoTransform()
    tif_proj = dataset.GetProjection()
    target = [0] * tif_height * tif_width
    for index_y in range(0, tif_height):
        for index_x in range(0, tif_width):
            if tif_data[index_y][index_x] < 0:
                target[index_x + index_y * tif_width] = 0
            else:
                target[index_x + index_y * tif_width] = 1
            # for band in range(0, tif_bandsCount):
            #     target[index_x + index_y * tif_width][band] = tif_data[band][index_y][index_x]
    return target

def readGoal(tifpath):
    dataset = gdal.Open(tifpath)
    if dataset == None:
        print('Can not open ' + tifpath)
        return None
    tif_width = dataset.RasterXSize
    tif_height = dataset.RasterYSize
    tif_bandsCount = dataset.RasterCount
    tif_data = dataset.ReadAsArray(0, 0, tif_width, tif_height)
    tif_geotrans = dataset.GetGeoTransform()
    tif_proj = dataset.GetProjection()
    goal = np.array([[0] * tif_bandsCount] * tif_height * tif_width)
    for index_y in range(0, tif_height):
        for index_x in range(0, tif_width):
            for band in range(0, tif_bandsCount):
                goal[index_x + index_y * tif_width][band] = tif_data[band][index_y][index_x]
    return goal, tif_width, tif_height, tif_geotrans, tif_proj


def writeTiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
    else:
        im_bands, (im_height, im_width) = 1,im_data.shape
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, im_width, im_height, im_bands, datatype)
    if(dataset!= None):
        dataset.SetGeoTransform(im_geotrans) 
        dataset.SetProjection(im_proj) 
    for i in range(im_bands):
        dataset.GetRasterBand(i+1).WriteArray(im_data[i])
    del dataset

if len(sys.argv) < 4:
    exit()

ms = ModelServiceContext()
ms.onInitialize(sys.argv[1], sys.argv[2], sys.argv[3])
mdh = ModelDataHandler(ms)

ms.onEnterState('Training')

ms.onFireEvent('TrainSource')

ms.onRequestData()

data_source = None
if ms.getRequestDataFlag() == ERequestResponseDataFlag.ERDF_OK:
    if ms.getRequestDataMIME() == ERequestResponseDataMIME.ERDM_RAW_FILE:
        data_source = ms.getRequestDataBody()
else:
    ms.onFinalize()

ms.onFireEvent('TrainTarget')

ms.onRequestData()

data_target = None
if ms.getRequestDataFlag() == ERequestResponseDataFlag.ERDF_OK:
    if ms.getRequestDataMIME() == ERequestResponseDataMIME.ERDM_RAW_FILE:
        data_target = ms.getRequestDataBody()
else:
    ms.onFinalize()

ms.onLeaveState()

dataset = gdal.Open(data_source)
if dataset == None:
    print('Can not open ' + data_source)
    exit()
tif_width = dataset.RasterXSize
tif_height = dataset.RasterYSize
tif_bandsCount = dataset.RasterCount
tif_data = dataset.ReadAsArray(0, 0, tif_width, tif_height)
tif_geotrans = dataset.GetGeoTransform()
tif_proj = dataset.GetProjection()
if tif_bandsCount == 1:
    tif_grey = tif_data[0 : tif_width , 0 : tif_height]
else :
    tif_bands = [None]*tif_bandsCount
    for index in range(tif_bandsCount):
        tif_bands[index] = tif_data[index, 0 : tif_height, 0 : tif_width]

source = np.array([[0] * tif_bandsCount] * tif_height * tif_width)
for index_y in range(0, tif_height):
    for index_x in range(0, tif_width):
        for band in range(0, tif_bandsCount):
            source[index_x + index_y * tif_width][band] = tif_data[band][index_y][index_x]

target = np.array(makeupTarget(data_target))

rf = RandomForestRegressor(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
rf.fit(source, target)


ms.onEnterState('FitTraining')

ms.onFireEvent('LoadPredictData')

ms.onRequestData()

data_goal = None
if ms.getRequestDataFlag() == ERequestResponseDataFlag.ERDF_OK:
    if ms.getRequestDataMIME() == ERequestResponseDataMIME.ERDM_RAW_FILE:
        data_goal = ms.getRequestDataBody()
else:
    ms.onFinalize()

goalData, gWidth, gHeight, gTrans, gProj = readGoal(data_goal)

result = rf.predict(goalData)
iWritingData = np.array([[[0]* gWidth] * gHeight]*1)

for index_y in range(0, gHeight):
    for index_x in range(0, gWidth):
        iWritingData[0][index_y][index_x] = result[index_x + index_y * gWidth]

#TODO
ms.onFireEvent('GetResult')

ms.setResponseDataFlag(ERequestResponseDataFlag.ERDF_OK)

ms.setResponseDataMIME(ERequestResponseDataMIME.ERDM_RAW_FILE)

dir_data = ms.getCurrentDataDirectory() + '/ResultData.TIF'

writeTiff(iWritingData, gWidth, gHeight, 1, gTrans, gProj, dir_data)

ms.setResponseDataBody(dir_data)

ms.onResponseData()

ms.onLeaveState()

print('Start to finalize!')

ms.onFinalize()