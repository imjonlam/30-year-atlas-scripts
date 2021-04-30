import os
import sys
import logging
import numpy as np
from osgeo import ogr, gdal

from BaseChart import BaseHandler
from Common.parse_args import argparser_init
from Common.ErrorHandler import baseException

# global
ROOT = os.path.dirname(os.path.realpath(__file__))

def set_frequency(const: dict, layer: ogr.Layer, region: str, ice_type: str, threshold: int=1):
  '''Set the Frequency burn-in value'''
  try:
    water, nodata = const['water'], const['nodata']
    burn_field = const['burn_field']
    burn = ogr.FieldDefn(burn_field, ogr.OFTInteger)

    layer.CreateField(burn)
    
    # set burn-in values for each feature
    logging.info(f'setting frequency using threshold: {threshold}')
    layer.ResetReading()
    for ft in layer:
      pnt_type = ft.GetField('PNT_TYPE')
      concn = ft.GetField(ice_type)
      concn = 0.0 if not concn else float(concn)

      if pnt_type in ['101', '107', '115', '400', '900']:
        ft.SetField(burn_field, water)
      elif pnt_type in ['123', '128', '133', '143']:
        ft.SetField(burn_field, nodata)
      elif pnt_type in ['106', '117', '118', '120', '122', '144'] and concn >= float(threshold):
        ft.SetField(burn_field, 1)
      elif pnt_type in ['106', '117', '118', '120', '122', '144'] and concn < float(threshold):
        ft.SetField(burn_field, water)
      else:
        ft.SetField(burn_field, nodata)

      layer.SetFeature(ft)
    
  except Exception as e:
    raise baseException(f'could not set values in {layer.GetName()} for frequency', 
                        baseException.ERR_CODE_LEVEL, e)

def calc_frequency(const: dict, nparray: np.ndarray, *unused) -> np.ndarray:
  '''Calculate Frequency of Ice'''
  # setup
  logging.info('calculating frequency')
  nodata = const['nodata']
  stack = np.dstack(nparray)
  tmp_numobs = np.sum(stack == 1, axis=-1)
  tmp_total = np.sum(stack != nodata, axis=-1)
  tmp_freq1 = np.divide(tmp_numobs, tmp_total, out=np.full(tmp_total.shape, nodata/100), 
                        where=tmp_total!=0) * 100

  # set values [0.1-0.9] = 1
  tmp_freq2 = np.copy(tmp_freq1)
  tmp_freq2[np.logical_and(tmp_freq2>0, tmp_freq2<1)] = 1

  # set values [99.1 - 99.9] = 99
  tmp_freq3 = np.copy(tmp_freq2)
  tmp_freq3[np.logical_and(tmp_freq3>99, tmp_freq3<100)] = 1

  # +0.5 if elem < 99.5
  tmp_freq_4 = np.copy(tmp_freq3)
  tmp_freq_4[tmp_freq_4 < 99.5] += 0.5  

  return tmp_freq_4.astype(int)

def set_frequency_colours(const: dict, ds: gdal.Dataset):
  '''Set the Frequency colours'''
  band = ds.GetRasterBand(1)

  # set colors
  logging.info('setting frequency colors')
  colors = gdal.ColorTable()
  colors.SetColorEntry(const['water'], (150, 200, 255))
  colors.CreateColorRamp(1, (255, 242, 0), 15, (255, 242, 0))
  colors.CreateColorRamp(16, (255, 200, 0), 33, (255, 200, 0))
  colors.CreateColorRamp(34, (255, 125, 3), 50, (255, 125, 3))
  colors.CreateColorRamp(51, (255, 0, 112), 66, (255, 0, 112))
  colors.CreateColorRamp(67, (204, 0, 184), 84, (204, 0, 184))
  colors.CreateColorRamp(85, (0, 0, 255), 99, (0, 0, 255))
  colors.SetColorEntry(100, (75, 75, 75))
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
    chart.set_methods(set_frequency, calc_frequency, set_frequency_colours)
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