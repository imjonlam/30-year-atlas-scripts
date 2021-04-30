import os
import json
import math
import logging
from typing import List
from osgeo import ogr, gdal

from oct01 import patchOct01
from Common.utils import logging_init, log_to_gitlab
from Common.helper import (
  get_spref,
  get_pixels,
  round_extent,
  get_shapefiles,
  open_shapefile,
  close_shapefile,
  create_shapefile,
  make_dummy,
  reproject,
  rasterize,
  create_tif,
  set_nodata,
  set_mask,
  read_band,
  save_array,
  clip,
  unlink
)

# global
ROOT = os.path.dirname(os.path.realpath(__file__))

class BaseHandler:
  def __init__(self, input_path: str, config_path: str):
    self.input_path = input_path
    self.config_path = config_path
    self.gdal_driver = gdal.GetDriverByName('GTiff')

  def __enter__(self):
    '''Open Streams'''
    self.input_stream = open(self.input_path)
    self.config_stream = open(self.config_path)

    self.inputs = json.load(self.input_stream)
    self.config = json.load(self.config_stream)
    
    return self

  def start_logging(self):
    '''Begin logging'''
    gitlab = self.inputs.get('log_to_gitlab', False)

    if gitlab:
      log_to_gitlab(self.config, self.inputs['chart'])
    else:
      logging_init(self.config, self.inputs['chart'])

  def set_methods(self, calc, colour, set_=None):
    '''Set class methods'''
    self.set = set_
    self.calc = calc
    self.colour = colour

  def start(self):
    '''Starts the creation of base chart(s)'''
    is_atlas = self.inputs.get('is_atlas', False)

    for date in self.inputs['historic_dates']:
      for region in self.inputs['regions']:
        if (region == 'AR' or 
          is_atlas and region not in ['EC', 'GL']):
          self.__create_atlas(region, date)
        else:
          self.__create(region, date)
   
  def __create(self, region: str, date: str):
    '''Creates a base chart'''
    fn = self.__filename(region, date)
    out = os.path.join(self.inputs['outdir'], fn + '.tif')

    # create in-memory raster
    chart = BaseChart(self.config, self.inputs, region, date)
    chart.set_methods(self.calc, self.colour, self.set)
    mem = chart.create(self.inputs['data'][region], fn)
    
    # save to output
    if mem:
      self.gdal_driver.CreateCopy(out, mem, options=['COMPRESS=LZW'])
      unlink([mem])

      logging.info(f'success: base chart stored in {out}')

  def __create_atlas(self, region: str, date: str):
    '''Creates an atlas base chart'''
    fn = self.__filename(region, date)
    out = os.path.join(self.inputs['outdir'], fn + '.tif')
    logging.info(f'creating atlas chart {out}')

    # define overlaps (bottom <-> top)
    if region == 'EA':
      regions = ['HB', 'EA']
    elif region == 'WA':
      regions = ['WA', 'EA']
    elif region == 'HB':
      regions = ['HB', 'EA']
    else:
      regions = ['HB', 'WA', 'EA']

    # create in-memory rasters (one per sub_region)
    datasets = []
    for sub_region in regions:
      chart = BaseChart(self.config, self.inputs, sub_region, date)
      chart.set_methods(self.calc, self.colour, self.set)

      sub_fn = self.__filename(sub_region, date)
      mem = chart.create(self.inputs['data'][sub_region], sub_fn)
      datasets.append(mem)

      # one of the required sub-charts could not be made, skip
      if mem is None:
        unlink(datasets)
        logging.warning(f'unable to create {fn}.tif, one or more required subcharts could not be made')
        return

    # clip
    pixel_size = self.config['constants']['pixel_size']
    aoi_path = os.path.join(ROOT, *self.config[region]['aoi'])
    clip(datasets, aoi_path, pixel_size, f'/vsimem/{out}')

    # save to output
    clipped = gdal.Open(f'/vsimem/{out}')
    self.gdal_driver.CreateCopy(out, clipped, options=['COMPRESS=LZW'])

    # clean
    unlink(datasets + [clipped])
    logging.info(f'success: base chart stored in {out}')

  def __filename(self, region: str, date: str) -> str:
    '''Returns a filename'''
    chart = self.inputs['chart']
    fn = self.config['filenames'][chart]

    if chart == 'oifrq':
      threshold = self.inputs.get('threshold', 1)
      threshold = 'i' if threshold == 1 else threshold
      return fn.format(region.lower(), threshold, date)
    else:
      return fn.format(region.lower(), date)

  def __exit__(self, exc_type, exc_value, traceback):
    self.input_stream.close()
    self.config_stream.close()

class BaseChart:
  def __init__(self, config: dict, inputs: dict, region: str, date: str=None):
    self.date = date
    self.config = config
    self.const = config['constants']
    self.pixel_size = self.const['pixel_size']

    self.chart = inputs['chart']
    self.years = inputs['years']

    self.threshold = inputs.get('threshold', 1)
    # remove these lines to allow for dynamic thresholds
    if self.chart != 'oifrq':
      self.threshold = 1

    self.__set_region(region)

  def set_methods(self, set_, calc, colour):
    '''Set class methods'''
    self.set = set_
    self.calc = calc
    self.colour = colour

  def __set_region(self, region):
    '''Sets the region and related params'''
    self.region = region
    self.info = self.config[region]
    self.aoi = self.__get_aoi()
    self.extent = round_extent(self.aoi, self.pixel_size)
    self.yres = get_pixels(self.extent, self.pixel_size)[1]

    wkt = os.path.join(ROOT, *self.config['wkt'])
    self.srs = get_spref(wkt, self.info['projection'])

  def create(self, folder: str, fn: str) -> gdal.Dataset:
    '''Returns a new base chart in-memory''' 
    logging.info(f'creating base chart: {fn}.tif')

    # process shapefiles
    archived = get_shapefiles(folder, self.years, self.date)
    if len(archived) == 0:
      logging.warning(f'could not find valid shapefiles to make {fn}.tif, skipping')
      return None

    shps = self.__open_archives(archived)
    self.__patch(shps)
    self.__set_burn(shps)
    self.__add_dummy(shps)

    # convert to raster
    tifs = self.__rasterize(shps)
    close_shapefile(shps)
    close_shapefile(self.aoi)

    # create tmp result
    tif = create_tif(f'/vsimem/{fn}_raw.tif', self.extent, self.srs, self.pixel_size)
    set_nodata(tif, self.const['nodata'])
    self.__calculate(tifs, tif)
    unlink([tifs])

    # colour
    self.colour(self.const, tif)

    # clip
    aoi_path = os.path.join(ROOT, *self.info['aoi'])
    clip([tif], aoi_path, self.pixel_size, f'/vsimem/{fn}.tif')
    unlink([tif])

    return gdal.Open(f'/vsimem/{fn}.tif')

  def __calculate(self, ds: gdal.Dataset, out: gdal.Dataset):
    '''Calculates resulting raster'''
    # chunk rasters for memory efficiency
    chunk = math.floor(self.yres / self.const['chunk'])

    for o in range(0, self.yres, chunk):
      arr = []
      for idx in range(ds.RasterCount):
        idx += 1
        band = ds.GetRasterBand(idx)
        arr.append(read_band(band, False, o, chunk))
      
      # calculate chunk
      result = self.calc(self.const, arr, self.region, self.chart=='cpmed')
      result = set_mask(self.const, result, arr, self.need_dummy)
      save_array(out, result, o)
      result = None
  
  def __rasterize(self, ds: ogr.DataSource) -> gdal.Dataset:
    '''Rasterize and reprojects all layers into bands'''
    num_bands = 1
    tif = create_tif('/vsimem/rasters.tif', self.extent, self.srs, self.pixel_size, ds.GetLayerCount())
    set_nodata(tif, self.const['nodata'])

    for layer in ds:
      reproject(layer, self.srs)
      rasterize(layer, tif, num_bands, self.const['burn_field'])
      num_bands += 1

    return tif

  def __open_archives(self, folder: str) -> ogr.DataSource:
    '''
    Opens all archived shapefiles.
    Returns as one datasource with 1 or more layers
    '''
    ds = None
    for fp in folder:
      fn = os.path.basename(fp).replace('.tar', '.shp')
      fp = os.path.join('/vsitar/'+fp, fn)

      tmp = open_shapefile(fp)
      layer = tmp.GetLayer()

      if ds is None:
        ds = create_shapefile('/vsimem/'+fn, 'ESRI Shapefile')
      ds.CopyLayer(layer, layer.GetName(), ['OVERWRITE=YES'])
      
      tmp.Release()
      tmp = None

    return ds
  
  def __set_burn(self, ds: ogr.DataSource):
    '''Inserts the burn value column into all layers'''
    ice_type = self.__get_icetype()
    
    for layer in ds:
      self.set(self.const, layer, self.region, ice_type, self.threshold)

  def __patch(self, ds: ogr.DataSource):
    '''Attempts to patch all layers in ds'''
    for layer in ds:
      patchOct01(layer)

  def __add_dummy(self, ds: ogr.DataSource):
    '''Adds a dummy layer if needed'''
    if (ds.GetLayerCount() % 2 == 0 and 
        self.chart in ['ctmed', 'cpmed', 'oimed']):
      self.need_dummy = True        
      params = (self.const['burn_field'], self.const['land'])
      ds_dummy = make_dummy(self.aoi, 'LAND_DUMMY', params)
      layer = ds_dummy.GetLayer()

      ds.CopyLayer(layer, layer.GetName(), ['OVERWRITE=YES'])
      ds_dummy = None
    else:
      self.need_dummy = False

  def __get_icetype(self) -> str:
    '''Gets the icetype by chart'''
    if self.chart in ['oimed', 'oifrq']:
      return 'N_COI'
    else:
      return 'N_CT'

  def __get_aoi(self) -> ogr.DataSource:
    '''Returns an opend datasource for aoi'''
    aoi = os.path.join(ROOT, *self.info['aoi'])
    return open_shapefile(aoi, edit=True)