import os
import sys
import logging
import numpy as np
from osgeo import osr, gdal

from SpecialChart import SpecialChart
from Common.parse_args import argparser_init
from Common.ErrorHandler import baseException
from Common.helper import (
  open_shapefile,
  close_shapefile,
  round_extent,
  create_tif, 
  set_nodata,
  save_array
)

# global
ROOT = os.path.dirname(os.path.realpath(__file__))

def calc_breakup(config: dict, ctmeds: str, region: str, threshold: int, out: str):
  '''
  Calculates Breakup Dates
  
  Parameters:
    config: config file as JSON
    ctmeds: directory containing f'{region}_{chart}{date}.tif' files
    region: region to make chart for
    threshold: minimum concentration [0-10]
    out: output file path
  '''
  logging.info(f'calculating breakup using threshold: {threshold} for {region}')

  const = config['constants']
  pixel_size = const['pixel_size']
  land, nodata = const['land'], const['nodata']

  dates = config['breakup']
  hd = dates.get(region, dates['default'])

  # retrieve relevant rasters
  # reason: AddBand is not supported. Cannot add bands dynamically
  rasters, missing = [], []
  for date in hd:
    found = False
    pattern = f'{region.lower()}_ctmed{date}'
    
    for f in os.listdir(ctmeds):
      fn, ext = os.path.splitext(f)

      if fn.startswith(pattern) and ext == '.tif':
        rasters.append(os.path.join(ctmeds, f))
        found = True

    if not found:
      missing.append(date)
  
  # ensure all ctmeds present
  if missing:
    fn = os.path.splitext(os.path.basename(out))[0]
    raise baseException(f'unable to create {fn} - insufficient ctmed charts, missing {missing}', 
                        baseException.ERR_CODE_LEVEL)
  
  try:
    # get aoi info
    aoi = open_shapefile(os.path.join(*config[region]['aoi']))
    spref = aoi.GetLayer().GetSpatialRef()
    extent = round_extent(aoi, pixel_size)
    close_shapefile(aoi)
    
    # stack all bands
    stack = []
    for r in rasters:
      tmp_ds = gdal.Open(r)
      tmp_band = tmp_ds.GetRasterBand(1).ReadAsArray()
      stack.append(tmp_band)
      tmp_ds = None
    stack = np.array(stack)

    # create land grid from band = 1
    band = stack[0]
    land = np.where(band < land, nodata, land)
    
    # create zero grid
    zero = np.where(np.logical_or(band > (land - 1), band == nodata), nodata, 0)

    # add historic date attributes
    tmp_grid1 = (np.logical_and(stack >= threshold * 10, stack <= 100)).astype(int)
    tmp_grid2 = np.full(tmp_grid1.shape, nodata, dtype=int)

    for i in range(stack.shape[0]):
      tmp_grid2[i] = np.where(tmp_grid1[i] == 1, int(hd[i]), nodata)

    # merge - for each column, retrieve the index of first non-null
    tmp_grid3 = np.vstack((land[None], tmp_grid2, zero[None]))

    mask = tmp_grid3 != nodata
    index = np.where(mask.any(axis=0), mask.argmax(axis=0), -1)
    idx, idy = np.ogrid[0:index.shape[0], 0:index.shape[1]]
    result = tmp_grid3[index[idx,idy], idx, idy]

  except Exception as e:
    raise baseException('error calculating breakup.',
                        baseException.ERR_CODE_LEVEL, e)

  try:
    tif = create_tif(out, extent, spref, pixel_size)
    set_nodata(tif, nodata)
    save_array(tif, result)
    tif = None
  except Exception as e:
    raise baseException('error saving raster results for breakup.', 
                        baseException.ERR_CODE_LEVEL, e)

def set_breakup_colours(constants: dict, tif: str, region: str):
  '''Set the colours for a breakup raster file'''
  ds = gdal.Open(tif, 1)
  band = ds.GetRasterBand(1)

  # set colors
  logging.info('setting breakup colors')
  colors = gdal.ColorTable()
  colors.SetColorEntry(constants['water'], (150, 200, 255))
  colors.SetColorEntry(constants['land'], (211, 181, 141))
  colors.SetColorEntry(constants['nodata'], (255, 255, 255))

  if region == 'GL':
    colors.SetColorEntry(430, (7, 29, 173))
    colors.SetColorEntry(416, (176, 7, 237))
    colors.SetColorEntry(402, (255, 0, 0))
    colors.SetColorEntry(319, (255, 255, 0))
    colors.SetColorEntry(305, (242, 241, 162))
  elif region == 'EC':
    colors.SetColorEntry(625, (7, 29, 113))
    colors.SetColorEntry(611, (111, 25, 209))
    colors.SetColorEntry(528, (206, 7, 237))
    colors.SetColorEntry(514, (247, 5, 138))
    colors.SetColorEntry(430, (255, 28, 0))
    colors.SetColorEntry(416, (255, 255, 0))
    colors.SetColorEntry(402, (252, 250, 88))
    colors.SetColorEntry(319, (242, 241, 162))
  else:
    colors.SetColorEntry(910, (7, 29, 113))
    colors.SetColorEntry(827, (111, 25, 209))
    colors.SetColorEntry(813, (206, 7, 237))
    colors.SetColorEntry(730, (247, 5, 138))
    colors.SetColorEntry(716, (255, 28, 0))
    colors.SetColorEntry(702, (250, 170, 0))
    colors.SetColorEntry(618, (255, 255, 0))
    colors.SetColorEntry(604, (242, 241, 162))

  band.SetRasterColorTable(colors)
  band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)

  ds = None

def main():
  args = argparser_init()
  args.config = os.path.join(ROOT, args.config)
  
  with SpecialChart(args.inputs, args.config) as chart:
    chart.start_logging()
    chart.set_methods(calc_breakup, set_breakup_colours)
    chart.start()
  
  return 0

if __name__ == '__main__':
  try:
    status = main()
  except Exception as e:
    status = 1
    # pylint: disable=no-member
    if isinstance(e, baseException):
      print(e.to_json())
    else:
      if hasattr(e, 'message'):
        print(baseException(e.message, 
              baseException.ERR_UNK_LEVEL, e).to_json())
      else:
        print(baseException('', 
              baseException.ERR_UNK_LEVEL, e).to_json()) 
  finally:
    sys.exit(status)