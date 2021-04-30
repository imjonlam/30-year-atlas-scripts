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

def calc_freezeup(config: dict, ctmeds: str, region: str, threshold: int, out: str):
  '''
  Calculates Freezeup Dates
  
  Parameters:
    config: config file as JSON
    ctmeds: directory containing f'{region}_{chart}{date}.tif' files
    region: region to make chart for
    threshold: minimum concentration [0-10]
    out: output file path
  '''
  logging.info(f'calculating freezeup using threshold: {threshold} for {region}')

  const = config['constants']
  pixel_size = const['pixel_size']
  land, nodata = const['land'], const['nodata']

  dates = config['ctfup']
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
    raise baseException('error calculating freezeup.',
                        baseException.ERR_CODE_LEVEL, e)

  try:
    tif = create_tif(out, extent, spref, pixel_size)
    set_nodata(tif, nodata)
    save_array(tif, result)
    tif = None
  except Exception as e:
    raise baseException('error saving raster results for freezeup.', 
                        baseException.ERR_CODE_LEVEL, e)

def set_freezeup_colours(constants: dict, tif: str, region: str):
  '''Set the colours for a freezeup raster file'''
  ds = gdal.Open(tif, 1)
  band = ds.GetRasterBand(1)

  # set colors
  logging.info('setting freezeup colors')
  colors = gdal.ColorTable()
  colors.SetColorEntry(constants['water'], (150, 200, 255))
  colors.SetColorEntry(constants['land'], (211, 181, 141))
  colors.SetColorEntry(constants['nodata'], (255, 255, 255))

  if region == 'GL':
    colors.SetColorEntry(1218, (9, 9, 145))
    colors.SetColorEntry(101, (25, 44, 168))
    colors.SetColorEntry(115, (32, 76, 189))
    colors.SetColorEntry(129, (32, 114, 214))
    colors.SetColorEntry(212, (61, 144, 227))
    colors.SetColorEntry(226, (107, 174, 232))
  elif region == 'EC':
    colors.SetColorEntry(1204, (23, 39, 163))
    colors.SetColorEntry(1218, (23, 62, 181))
    colors.SetColorEntry(101, (34, 89, 199))
    colors.SetColorEntry(115, (33, 118, 217))
    colors.SetColorEntry(129, (54, 141, 227))
    colors.SetColorEntry(212, (92, 156, 227))
    colors.SetColorEntry(226, (145, 190, 233))
    colors.SetColorEntry(312, (180, 220, 255))
  else:
    colors.SetColorEntry(910, (76, 0, 115))
    colors.SetColorEntry(924, (0, 38, 115))
    colors.SetColorEntry(1008, (0, 77, 168))
    colors.SetColorEntry(1022, (0, 92, 230))
    colors.SetColorEntry(1105, (54, 121, 227))
    colors.SetColorEntry(1119, (92, 156, 227))
    colors.SetColorEntry(1204, (190, 232, 255))

  band.SetRasterColorTable(colors)
  band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)

  ds = None

def main():
  args = argparser_init()
  args.config = os.path.join(ROOT, args.config)

  with SpecialChart(args.inputs, args.config) as chart:
    chart.start_logging()
    chart.set_methods(calc_freezeup, set_freezeup_colours)
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