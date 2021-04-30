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

PREDOMINANTS = {'FI': 17,
                'ND': 123,
                'LD': 900,
                'NI': 0,
                '?': 16,
                'X': 16,
                'B': 7,
                'L': 15,
                '9.': 14,
                '8.': 13,
                '7.': 12,
                '4.': 11,
                '1.': 10
              }

def get_predom(const: dict, ft: ogr.Feature) -> int:
  '''Derive the predominant ice value'''
  # get fields
  e_ct = ft.GetField('E_CT')
  e_ca = ft.GetField('E_CA')
  e_cb = ft.GetField('E_CB')
  e_cc = ft.GetField('E_CC')
  e_sa = ft.GetField('E_SA')
  e_sb = ft.GetField('E_SB')
  e_sc = ft.GetField('E_SC')
  e_sd = ft.GetField('E_SD')
  pnt_type = ft.GetField('PNT_TYPE')

  # set icebergs to open water
  e_sa = '0' if e_sa == 'L' else e_sa
  e_sb = '0' if e_sb == 'L' else e_sb
  e_sc = '0' if e_sc == 'L' else e_sc

  # find predominant
  key = ''
  if pnt_type in ['123', '128', '133']: # nodata
    key = 'ND'
  elif pnt_type in ['900', '400']: # land
    key = 'LD'
  elif pnt_type in ['101', '107', '115', '146']:  # icefree/openwater/bergywater
    key = 'NI'
  else:
    # derive cd
    ca, cb, cc = 0, 0, 0
    cd = 10 if e_ct == '9+' else int(float(e_ct)) if e_ct else 0
    
    if e_ca is None:
      ca = 10 if e_ct == '9+' else int(float(e_ct))
    if e_cb:
      cb = int(float(e_cb))
    if e_cc:
      cc = int(float(e_cc))
    
    cd -= ca + cb + cc

    # 1x icetype
    e_ca = e_ct if e_ca is None else e_ca
    ca = 10 if e_ca == '9+' else int(float(e_ca))
    cb = 0 if e_cb is None else int(float(e_cb))
    cc = 0 if e_cc is None else int(float(e_cc))

    # 3x icetypes, pick the middle icetype
    if ca == cb and ca == cc:
      key = e_sa
    
    # choose predominance from column a to d
    elif ca >= cb and ca >= cc and ca >= cd:
      key = e_sa
    elif cb > ca and cb >= cc and cb >= cd:
      key = e_sb
    elif cc > ca and cc > cb and cc >= cd:
      key = e_sc
    elif cd > ca and cd > cb and cd > cc:
      key = e_sd

    # verify old ice predominance
    oipredom = False
    sypredom = False
    mypredom = False    
    oi = 0

    # check column a
    if e_sa in ['7.', '8.', '9.']:
      oi += ca
    if e_sa == '7.' and ca >= 4:
      oipredom = True
    elif e_sa == '8.' and ca >= 4:
      sypredom = True
    elif e_sa == '9.' and ca >= 4:
      mypredom = True
    
    # check colum b
    if e_sb in ['7.', '8.', '9.']:
      oi += cb
    if e_sb == '7.' and cb >= 4:
      oipredom = True
    elif e_sb == '8.' and cb >= 4:
      sypredom = True
    elif e_sb == '9.' and cb >= 4:
      mypredom = True
      
    # check colum c
    if e_sc in ['7.', '8.', '9.']:
      oi += cc
    if e_sc == '7.' and cc >= 4:
      oipredom = True
    elif e_sc == '8.' and cc >= 4:
      sypredom = True
    elif e_sc == '9.' and cc >= 4:
      mypredom = True

    # find predominant, order MY->SY->OLD.
    # preference given to oldice subcategories
    if oi >= 4:
      key = '7.'
    elif oipredom:
      key = '7.'
    elif sypredom:
      key = '8.'
    elif mypredom:
      key = '9.'
   
  # return predominant
  stage = PREDOMINANTS.get(key)
  if stage is None:
    try: 
      stage = int(float(key))
    except:
      stage = const['water']

  logging.info(f'predominant = {stage}')
  return stage

def set_median_predom(const: dict, layer: ogr.Layer, region: str, *unused):
  '''Set the Median Predominance burn-in value'''
  try:
    burn_field = const['burn_field']
    burn = ogr.FieldDefn(burn_field, ogr.OFTInteger)

    layer.CreateField(burn)

    # set burn-in values for each feature
    logging.info('setting median predominance')
    layer.ResetReading()
    for ft in layer:
      predominant = get_predom(const, ft)
      ft.SetField(burn_field, predominant)
      layer.SetFeature(ft)

  except Exception as e:
    raise baseException(f'could not set values in {layer.GetName()} for median predominance', 
                        baseException.ERR_CODE_LEVEL, e)

def calc_median_predom(const: dict, nparray: np.ndarray, region: str, *unused) -> np.ndarray:
  '''Calculate Median Predominance of Ice'''
  stack = np.dstack(nparray)
  water, land, nodata = const['water'], const['land'], const['nodata']

  logging.info('calculating median predominance')
  if region != 'GL':
    tmp_new = np.count_nonzero(np.isin(stack, [1,2]), axis=-1)
    tmp_grey = np.count_nonzero(np.isin(stack, [3,4]), axis=-1)
    tmp_gw = np.count_nonzero(stack == 5, axis=-1)
    tmp_fy = np.count_nonzero(stack == 6, axis=-1)
    tmp_fy_thn = np.count_nonzero(np.isin(stack, [7,8,9]), axis=-1)
    tmp_fy_med = np.count_nonzero(stack == 10, axis=-1)
    tmp_fy_thk = np.count_nonzero(stack == 11, axis=-1)
    tmp_old = np.count_nonzero(np.isin(stack, [12,13,14,15]), axis=-1)

    tmp_all = np.count_nonzero(np.isin(stack, [water, land, nodata], invert=True), axis=-1)
    tmp_mid = np.where(tmp_all % 2 == 0, (tmp_all + 2) // 2, (tmp_all + 1) // 2)
    del tmp_all

    result = np.where(tmp_new >= tmp_mid, 1,
              np.where(tmp_grey + tmp_new >= tmp_mid, 4,
                np.where(tmp_gw + tmp_grey + tmp_new >= tmp_mid, 5,
                  np.where(tmp_fy + tmp_gw + tmp_grey + tmp_new >= tmp_mid, 6,
                    np.where(tmp_fy_thn + tmp_fy + tmp_gw + tmp_grey + tmp_new >= tmp_mid, 7,
                      np.where(tmp_fy_med + tmp_fy_thn + tmp_fy + tmp_gw + tmp_grey + tmp_new >= tmp_mid, 10,
                        np.where(tmp_fy_thk + tmp_fy_med + tmp_fy_thn + tmp_fy + tmp_gw + tmp_grey + tmp_new >= tmp_mid, 11,
                          np.where(tmp_old + tmp_fy_thk + tmp_fy_med + tmp_fy_thn + tmp_fy + tmp_gw + tmp_grey + tmp_new >= tmp_mid, 12, water)
                        )
                      )
                    )
                  )
                )
              )
            )
          
    return(result)
    
  else:
    tmp_new = np.count_nonzero(np.isin(stack, [1,2]), axis=-1)
    tmp_thn = np.count_nonzero(stack == 4, axis=-1)
    tmp_med = np.count_nonzero(stack == 5, axis=-1)
    tmp_thk = np.count_nonzero(stack == 7, axis=-1)
    tmp_v_thk = np.count_nonzero(stack == 10, axis=-1)

    tmp_all = np.count_nonzero(np.isin(stack, [water, land, nodata], invert=True), axis=-1)
    tmp_mid = np.where(tmp_all % 2 == 0, (tmp_all + 2) // 2, (tmp_all + 1) // 2)
    del tmp_all

    result = np.where(tmp_new >= tmp_mid, 1,
              np.where(tmp_thn + tmp_new >= tmp_mid, 4,
                np.where(tmp_med + tmp_thn + tmp_new >= tmp_mid, 5,
                  np.where(tmp_thk + tmp_med + tmp_thn + tmp_new >= tmp_mid, 7,
                    np.where(tmp_v_thk + tmp_thk + tmp_med + tmp_thn + tmp_new >= tmp_mid, 10, water)
                  )
                )
              )
            )

    return result

def set_median_predom_colours(const: dict, ds: gdal.Dataset):
  '''Set the Median Predominance colours'''
  band = ds.GetRasterBand(1)

  # set colors
  logging.info('setting median predominance colors')
  colors = gdal.ColorTable()
  colors.SetColorEntry(const['water'], (150, 200, 255))
  colors.SetColorEntry(1, (240, 210, 250))
  colors.SetColorEntry(4, (135, 60, 215))
  colors.SetColorEntry(5, (220, 80, 215))
  colors.SetColorEntry(6, (255, 255, 0))
  colors.SetColorEntry(7, (155, 210, 0))
  colors.SetColorEntry(10, (0, 200, 20))
  colors.SetColorEntry(11, (0, 120, 0))
  colors.SetColorEntry(12, (180, 100, 50))
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
    chart.set_methods(set_median_predom, calc_median_predom, set_median_predom_colours)
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