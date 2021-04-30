import os
import sys
import logging
import warnings
import numpy as np
from osgeo import ogr, gdal

from BaseChart import BaseHandler
from Common.parse_args import argparser_init
from Common.ErrorHandler import baseException

# global
ROOT = os.path.dirname(os.path.realpath(__file__))

def set_median_ct(const: dict, layer: ogr.Layer, region: str, ice_type: str, *unused):
  '''Set the Median Concentration burn-in value'''
  try:
    water, land, nodata = const['water'], const['land'], const['nodata']
    burn_field = const['burn_field']
    burn = ogr.FieldDefn(burn_field, ogr.OFTInteger)

    layer.CreateField(burn)

    # set burn-in values for each feature
    logging.info('setting median ct')
    layer.ResetReading()
    for ft in layer:
      fa = ft.GetField('FA')
      fb = ft.GetField('FB')
      fc = ft.GetField('FC')
      concn = ft.GetField(ice_type)

      if concn is None or concn == '':
        concn = water
      elif '08' in [fa, fb, fc] and concn in ['9.7', '10.0']:
        concn = '11.0'
      elif '07' in [fa, fb, fc] and concn == '10.0':
        concn = '10.0'
      ft.SetField(burn_field, int(float(concn)))

      pnt_type = ft.GetField('PNT_TYPE')
      if pnt_type in ['101', '115', '107']:
        ft.SetField(burn_field, water)
      elif pnt_type in ['400', '900']:
        ft.SetField(burn_field, land)
      elif pnt_type in ['123', '128', '133', '143']:
        ft.SetField(burn_field, nodata)

      layer.SetFeature(ft)

  except Exception as e:
    raise baseException(f'could not set values in {layer.GetName()} for median concentration', 
                        baseException.ERR_CODE_LEVEL, e)

def calc_median_ct(const: dict, nparray: np.ndarray, region: str, is_cpmed: bool) -> np.ndarray:
  '''Calculate Median Concentration'''
  logging.info('calculating median ct')
  water, land, nodata = const['water'], const['land'], const['nodata']
  exclude = [water, land, nodata] if is_cpmed else [land, nodata]
  stack = np.dstack(nparray)
  stack = np.where(np.isin(stack, exclude), np.NaN, stack)

  # convert even lengthed stacks to odd
  # if stack is even length, force the median to be the higher of the two
  stack = np.sort(stack, axis=-1)
  non_nan = np.count_nonzero(~np.isnan(stack), axis=-1)
  idx = np.where(np.logical_and(non_nan % 2 == 0, non_nan != 0))
  stack[idx[0], idx[1], -1] = land

  # calculate median
  with warnings.catch_warnings():
    warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')
    result = np.nanmedian(stack, axis=-1)
  
  # remove NAN
  result[np.isnan(result)] = nodata

  return result.astype(int)

def set_median_ct_colours(const: dict, ds: gdal.Dataset):
  '''Set the Median Concentration colours'''
  band = ds.GetRasterBand(1)
  
  # set colors
  logging.info('setting median ct colors')
  colors = gdal.ColorTable()
  colors.SetColorEntry(const['water'], (150, 200, 255))
  colors.CreateColorRamp(1, (140, 255, 160), 3, (140, 255, 160))
  colors.CreateColorRamp(4, (255, 255, 0), 6, (255, 255, 0))
  colors.CreateColorRamp(7, (255, 125, 7), 8, (255, 125, 7))
  colors.CreateColorRamp(9, (255, 0, 0), 10, (255, 0, 0))
  colors.SetColorEntry(11, (150, 150, 150))
  colors.SetColorEntry(const['land'], (211, 181, 141))
  colors.SetColorEntry(const['nodata'], (255, 255, 255))

  band.SetRasterColorTable(colors)
  band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)

  ds = None

def main():
  args = argparser_init()
  args.config = os.path.join(ROOT, args.config)

  with BaseHandler(args.inputs, args.config) as chart:
    chart.start_logging()
    chart.set_methods(set_median_ct, calc_median_ct, set_median_ct_colours)
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