import os
import time
import tarfile
import logging
import calendar
import subprocess
import numpy as np
from datetime import date
from typing import List, Tuple

from Common.utils import del_dir
from Common.ErrorHandler import baseException
from osgeo import ogr, gdal, osr

'''''''''''''''
GENERIC METHODS
'''''''''''''''
def get_pixels(extent: List[float], pixel_size: int) -> Tuple:
  '''Returns the resolution of an extent'''
  xmin, xmax, ymin, ymax = extent
  xres = int((xmax - xmin) / pixel_size)
  yres = int((ymax - ymin) / pixel_size)

  return (xres, yres)

def expand_extent(extent: List[float], offset: int) -> Tuple:
  '''Returns a new extent expanded with offset'''
  xmin, xmax, ymin, ymax = extent
  return (xmin - offset, xmax + offset, ymin - offset, ymax + offset)

def isHD(cd: date, hd: date):
  '''Returns True if a given date is a historic date'''
  nov26 = hd.month == 11 and hd.day == 26
  feb26 = hd.month == 2 and hd.day == 26 and calendar.isleap(cd.year)
  ahead = 3 if not (nov26 or feb26) else 4
  diff = (hd - cd).days
  behind = -3

  return (behind <= diff <= ahead)

def get_shapefiles(folder: str, years: List[int], hd: str) -> List[str]:
  '''Returns a list of shapefile paths matching historic date and years'''
  logging.info(f'retrieving shapefiles in {folder} for {hd}')
  shapefiles = []
  mo, d = int(hd[:2]), int(hd[2:4]) 

  for fn in os.listdir(folder):
    fd = os.path.splitext(fn)[0].split('_')[2]
    yr = int(fd[0:4])
    cd = date(yr, int(fd[4:6]), int(fd[6:8]))
    hd = date(yr, mo, d)

    if isHD(cd, hd) and cd.year in years:
      try:
        yrMo = fd[0:6]
        found = next(f for f in shapefiles if yrMo in f)
        fd = os.path.splitext(found)[0].split('_')[2]
        md = date(int(fd[0:4]), int(fd[4:6]), int(fd[6:8]))

        if abs((cd - hd).days) < abs((md - hd).days):
          idx = shapefiles.index(found)
          shapefiles[idx] = fn
      except:
        shapefiles.append(fn)

  return [os.path.join(folder, v) for v in shapefiles]  

'''''''''''
OGR METHODS
'''''''''''
def get_fields(ldefn: ogr.FeatureDefn) -> List[str]:
  ''''Get a list of fields in the shapefile'''
  return [ldefn.GetFieldDefn(n).name for n in range(ldefn.GetFieldCount())]

def get_spref(wkt: str, deg: int) -> osr.SpatialReference:
  '''Returns an osr SpatialReference with a Central Meridian of degree'''
  with open(wkt) as w:
    srs = osr.SpatialReference()
    srs.ImportFromWkt(w.read())
    srs.SetProjParm(osr.SRS_PP_CENTRAL_MERIDIAN, deg)

  return srs

def round_extent(ds: ogr.DataSource, pixel_size: int) -> List[float]:
  '''Gets the rounded extent'''
  layer = ds.GetLayer()
  extent = layer.GetExtent()
  return [round(e / pixel_size) * pixel_size for e in extent]

def create_shapefile(fp: str, name: str) -> ogr.DataSource:
  '''Returns an ogr DataSource with name'''
  logging.info(f'creating shapefile {fp}')
  driver = ogr.GetDriverByName(name)
  return driver.CreateDataSource(fp)

def open_shapefile(fp: str, edit: bool=False) -> ogr.DataSource:
  '''Returns an opened ogr DataSource in r/w mode'''
  logging.info(f'opening shapefile {fp}')
  try:
    driver = ogr.GetDriverByName('ESRI Shapefile')
    return driver.Open(fp, int(edit))
  except Exception as e:
    raise baseException(f'shapefile: {fp} could not be opened.', 
                        baseException.ERR_CODE_LEVEL, e)

def close_shapefile(shp: ogr.DataSource) -> str:
  '''Closes the shapefile'''
  logging.info(f'closing shapefile {shp.GetName()}')
  try:
    shp.Release()
    shp = None
  except Exception as e:
    raise baseException(f'shapefile: {shp.GetName()} could not be closed',
                        baseException.ERR_CODE_LEVEL, e)

def make_dummy(ds: ogr.DataSource, name: str, burn: Tuple) -> ogr.DataSource:
  '''Returns a dummy layer for CTMED populated with burn[1] values'''
  logging.info(f'creating dummy: {name} layer')

  try:
    # create dummy layer
    mem = create_shapefile('memory', 'MEMORY')
    dummy = mem.CopyLayer(ds.GetLayer(), name, ['OVERWRITE=YES'])

    # add burn field and populate
    fdefn = ogr.FieldDefn(burn[0], ogr.OFTInteger)
    dummy.CreateField(fdefn)

    dummy.ResetReading()
    for ft in dummy:
      ft.SetField(burn[0], burn[1])
      dummy.SetFeature(ft)

    return mem

  except Exception as e:
    close_shapefile(ds)
    raise baseException(f'dummy: {name} layer could not be created.',
                        baseException.ERR_CODE_LEVEL, e)

def reproject(layer: ogr.Layer, srs: osr.SpatialReference):
  '''Reprojects an existing layer given a spatial reference'''
  layer_name = layer.GetName()
  logging.info(f'reprojecting {layer_name}')

  projection = layer.GetSpatialRef()
  if projection is None:
    raise baseException(f'layer: {layer_name} does not have a spatial reference.',
                        baseException.ERR_INPUT_LEVEL)

  # no action needed
  if projection.IsSame(srs):
    logging.info('no reprojection required')
    return

  try:
    # transform
    coordTrans = osr.CoordinateTransformation(projection, srs)

    # copy features
    layer.ResetReading()

    for ft in layer:
      geom = ft.GetGeometryRef()
      geom.Transform(coordTrans)
      ft.SetGeometry(geom)
  except Exception as e:
    raise baseException(f'layer: {layer_name} could not be reprojected.',
                        baseException.ERR_CODE_LEVEL, e)

'''''''''''''''
GDAL METHODS
'''''''''''''''
def create_tif(fp: str, extent: List[float], srs: osr.SpatialReference, pixel_size: int, num_bands: int=1) -> gdal.Dataset:
  '''Returns a new .tif file'''
  logging.info(f'creating .tif : {fp}')
  driver = gdal.GetDriverByName('GTiff')

  # delete if exists
  if os.path.exists(fp):
    logging.info('deleting existing .tif')
    driver.Delete(fp)

  res = get_pixels(extent, pixel_size)
  
  # create tif
  ds = driver.Create(fp, *res, num_bands, gdal.GDT_UInt16)
  ds.SetGeoTransform((extent[0], pixel_size, 0, extent[3], 0, -pixel_size))
  ds.SetProjection(srs.ExportToWkt())

  return ds

def set_nodata(ds: gdal.Dataset, nodata: int):
  '''Sets and fills NoDataValue in RasterBand(s)'''
  logging.info('setting nodata values in raster across all bands')
  for idx in range(0, ds.RasterCount):
    idx += 1
    band = ds.GetRasterBand(idx)
    band.Fill(nodata)
    band.SetNoDataValue(nodata)

def read_band(band: gdal.Band, full=True, offset=None, chunk=None) -> List[int]:
  '''
  Returns an array of a raster band

  Parameters:
    band: a gdal band
    full: to open the entirety of the raster
    offset: row offset
    chunk: chunk size of opening partially

  Returns:
    an array of pixels
  '''
  logging.info(f'reading raster band: full={full}, offset={offset}')

  if full:
    arr = band.ReadAsArray()
  else:
    nrows = band.YSize
    ncols = band.XSize
    chunk = (nrows - offset) if (nrows - offset) < chunk else chunk
    arr = band.ReadAsArray(0, offset, ncols, chunk)
    
  return arr

def rasterize(layer: ogr.Layer, ds: gdal.Dataset, idx: int, burn_field: str):
  '''Rasterizes a layer and adds to an existing dataset'''
  logging.info(f'rasterizing {layer.GetName()}')
  gdal.RasterizeLayer(ds, [idx], layer, options=['attribute={}'.format(burn_field)])

def save_array(raster: gdal.Dataset, result: List[int], offset: int=0):
  '''
  Store the array into a raster file

  Parameters:
    raster: raster file to save data into
    result: array of pixels to store
    offset: location to begin storing array
  '''
  logging.info(f'saving raster results')
  band = raster.GetRasterBand(1)
  band.WriteArray(result, 0, offset)
  band = None

def clip(rasters: List[gdal.Dataset], aoi_path: str, pixel_size: int, dest: str):
  '''
  Clip raster datasets by AOI bounds

  Parameters:
    rasters: raster dataset(s)
    aoi_path: path to AOI shapefile
    pixel_size: size of 1 pixel in KM
    dest: output path
  '''
  if len(rasters) > 1:
    logging.info(f'merging and clipping boundary with {aoi_path}')
  else:
    logging.info(f'clipping boundary with {aoi_path}')

  driver = ogr.GetDriverByName('ESRI Shapefile')
  bnd = driver.Open(aoi_path)
  extent = round_extent(bnd, pixel_size)

  opt = gdal.WarpOptions(
    outputBounds = extent,
    targetAlignedPixels = False,
    cutlineDSName = aoi_path,
    cutlineLayer = bnd.GetLayer().GetName(),
    cropToCutline = True
  )

  bnd.Release()
  bnd = None

  gdal.Warp(dest, rasters, options=opt)

def unlink(rasters: List[gdal.Dataset]):
  '''Unlinks an in-memory raster'''
  for r in rasters:
    gdal.Unlink(r.GetDescription())
    r = None

'''''''''''''''
NUMPY METHODS
'''''''''''''''
def set_mask(const: dict, base: np.ndarray, data: np.ndarray, has_dummy: bool=False) -> np.ndarray:
  '''Returns a mask of land, water and nodata'''
  logging.info('applying mask')
  stack = np.dstack(data)
  depth = stack.shape[2]

  # set minimum parameters
  min_land = 1 if has_dummy else 0
  min_water = depth - 1 if has_dummy else depth

  # count number of occurences
  nodata, water, land = const['nodata'], const['water'], const['land']
  land_count = np.count_nonzero(stack == land, axis=-1)
  water_count = np.count_nonzero(stack == water, axis=-1)

  # create mask
  mask = np.where(land_count > min_land, land,
          np.where(water_count == min_water, water, nodata)
        )

  return np.where(mask != nodata, mask, base).astype(int)