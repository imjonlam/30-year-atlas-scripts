# !/usr/bin/env python3.6
########################################################
#                                                      # 
#                 CLIMATE TO SIGRID                    # 
#                  [ONE TIME USE]                      #
#       Converts climate E00 to climate shapefile      #
#                                                      # 
########################################################

import os
import sys
import json
import datetime
import argparse
import subprocess
from osgeo import ogr, osr

import sigrid as sigrid
from Common import *

# GLOBAL
ROOT = os.path.dirname(os.path.realpath(__file__))
CONFIG = r'Common\config.json'

SUCCESS = '0'
ERR_FILE = '1'
ERR_COVERAGE = '2'
ERR_MAPPING = '3'
ERR_UNKNOWN = '4'

ADD = [('POLY_TYPE', 1), ('CT', 2), ('CA', 2), ('CB', 2), ('CC', 2), ('CD', 2), ('SA', 2),
       ('SB', 2), ('SC', 2), ('CN', 2), ('FA', 2), ('FB', 2), ('FC', 2)
      ]
KEEP = ['AREA', 'PERIMETER', 'EGG_ID', 'EGG_NAME', 'EGG_ATTR', 'PNT_TYPE']
DROP = ['PNT_TYPE', 'EGG_ID', 'EGG_NAME', 'EGG_ATTR']

def to_coverage(fp, avcimport, out):
  # setup
  fn, _ = os.path.splitext(os.path.basename(fp))
  coverage = os.path.join(out, fn)
  
  # convert e00 -> coverage
  print('converting e00 to coverage')
  subprocess.Popen([avcimport, fp, coverage]).wait()

  # sanity check - AVCIMPORT does not throw error if conversion fails
  driver = ogr.GetDriverByName('AVCBIN')
  ds = driver.Open(coverage)
  ldefn = ds.GetLayerByName('PAL').GetLayerDefn()
  num_fields = ldefn.GetFieldCount()
  ds.Release()

  if num_fields < 2: # only ArcIDS present
    raise Exception(ERR_COVERAGE)
  else:
    return coverage

# method retrived from create_poly
# modified to use OSGEO (ogr)
def force_fix_coverage(ft, index):
  # setup
  print(f'*fixing FID {ft.GetFID()}')
  pnt_type = ft.GetField('PNT_TYPE')
  egg = ft.GetField('EGG_ATTR')

  # no_data
  if pnt_type == 0:
    ft.SetField('PNT_TYPE', 123)
  
  # attempt to fix poly_type
  fixed_poly = sigrid.try_fix_poly_type('I', ' ', pnt_type, ' ')
  ft.SetField('POLY_TYPE', fixed_poly)

  # attempt to fix empty eggs
  fixed_egg, force_overwrite_egg_attr = sigrid.try_fix_empty_egg(egg, '', fixed_poly, pnt_type, True, 'None')
  if force_overwrite_egg_attr or fixed_egg != ' ':
    ft.SetField('EGG_ATTR', fixed_egg)

  # map EGG to SIGRID(2014)
  sigrid_value = sigrid.map_egg_to_sigrid(fixed_egg, fixed_poly, None)

  # set SIGRID fields
  for key, value in sigrid_value.items():
    if not value:
      value = ' '

    ft.SetField(key, value)

def to_sigrid(fp, out, dsname):
  # setup
  drivers = {'BIN':   ogr.GetDriverByName('AVCBIN'),
             'SHAPE': ogr.GetDriverByName('ESRI Shapefile')
            }

  # open coverage and filter fields
  cov = drivers['BIN'].Open(fp)
  if cov is None:
    raise Exception(ERR_COVERAGE)

  print('converting coverage to shapefile')
  result = cov.ExecuteSQL('SELECT {} FROM PAL'.format(','.join(KEEP)))

  # create new shapefile
  shapefile = os.path.join(out, dsname)
  shp = drivers['SHAPE'].CreateDataSource(shapefile)
  spref = result.GetSpatialRef()
  layer = shp.CreateLayer(dsname, spref, ogr.wkbPolygon)

  # add fields
  ldefn = result.GetLayerDefn()
  for i in range(ldefn.GetFieldCount()):
    fdefn = ldefn.GetFieldDefn(i)

    # to avoid field width errors
    if fdefn.name in ['AREA', 'PERIMETER']:
      fdefn.SetWidth(26)
      fdefn.SetPrecision(11)
    
    layer.CreateField(fdefn)
  
  # add features
  result.ResetReading()
  for ft in result:
    layer.CreateFeature(ft)

  # add new fields
  fdefn = ogr.FieldDefn('UNSET', ogr.OFTString)
  for field in ADD:
    fdefn.SetName(field[0])
    fdefn.SetWidth(field[1])
    layer.CreateField(fdefn)

  # get fieldname list
  fields = []
  ldefn = layer.GetLayerDefn()
  for i in range(ldefn.GetFieldCount()):
    fdefn = ldefn.GetFieldDefn(i)
    fields.append(fdefn.name)
  
  # convert EGGs to SIGRID(2014)
  idx = {k: v for v, k in enumerate(fields)}
  layer.ResetReading()
  for ft in layer:
    try:
      force_fix_coverage(ft, idx)
      layer.SetFeature(ft)
    except Exception:
      cov.Release()
      shp.Release()
      cov = shp = None
      raise Exception(ERR_MAPPING)

  # reopen shapefile. DROP seems to crash otherwise
  shp.Release()
  shp = drivers['SHAPE'].Open(shapefile, 1)

  # drop unnecessary fields
  for field in DROP:
    shp.ExecuteSQL(f'ALTER TABLE {dsname} DROP COLUMN {field}')

  # cleanup
  cov.Release()
  shp.Release()
  cov = shp = None

  return shapefile
  
def to_climate(fp, out, sigrid2climate, dsname):
  print('converting shapefile to climate shapefile')
  climate = os.path.join(out, dsname)
  makeDir(climate)
  subprocess.Popen([sys.executable, sigrid2climate, fp, climate]).wait()

  return climate

def run(fp, out, isCov=False):
  # setup
  fn, _ = os.path.splitext(os.path.basename(fp))
  fn_split = fn.upper().split('_')
  now = datetime.datetime.now()

  with open(CONFIG) as f:
    config = json.load(f)

  print(f'converting {fn} to climate shapefile')
  tmp_dir = os.path.join(*config['tmp']).format(os.getenv('username'))
  removeDir(tmp_dir, recreate=True)
  
  # verify filename
  if len(fn_split) != 2:
    return ERR_FILE
  
  region, date = fn_split
  if region not in ['EA', 'WA', 'HB', 'EC', 'GL'] and len(date) != 6:
    return ERR_FILE

  # generate SIGRID filenames
  year = '19' if int(date[0:2]) > abs(now.year) % 100 else '20'
  date = year + date
  sName = '{0}_SGRDR{1}_{2}'.format('CIS', region, date)
  cName = '{0}_{1}_{2}_{3}_{4}'.format('CIS', region, date, 'pl', 'a')

  # convert
  try:
    avcimport = os.path.join(ROOT, *config['avcimport'])
    coverage = fp if isCov else to_coverage(fp, avcimport, tmp_dir)

    shapefile = to_sigrid(coverage, tmp_dir, sName)

    sigrid2climate = os.path.join(ROOT, *config['sigrid2climate'])
    climate = to_climate(shapefile, sigrid2climate, tmp_dir, cName)
  except Exception as e:
    removeDir(tmp_dir)
    return e

  # cleanup
  print(f'archiving {climate}')
  toTar(climate, out)
  removeDir(tmp_dir)

  return SUCCESS

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-e00', type=lambda x: is_valid_e00(parser, x), help='path to e00')
  parser.add_argument('-cov', type=lambda x: is_valid_directory(parser, x), help='path to coverage')
  parser.add_argument('-dir', type=lambda x: is_valid_directory(parser, x), help='path to directory of e00s')
  parser.add_argument('output', type=lambda x: is_valid_directory(parser, x), help='output directory')
  args = parser.parse_args()

  if sum(bool(choice) for choice in [args.e00, args.cov, args.dir]) != 1:
    parser.error('only one of -e00, -cov or -dir allowed')

  # setup  
  results = {el:[] for el in [SUCCESS, ERR_FILE, ERR_COVERAGE, ERR_MAPPING, ERR_UNKNOWN]}

  # convert
  if args.cov:
    status = run(args.cov, args.output, isCov=True)
    results.get(status, results[ERR_UNKNOWN]).append(args.cov)
  elif args.e00:
    status = run(args.e00, args.output, isCov=False)
    results.get(status, results[ERR_UNKNOWN]).append(args.e00)
  else:
    for f in os.listdir(args.dir):
      if f.endswith('.e00'):
        fp = os.path.join(args.dir, f)
        status = run(fp, args.output, isCov=False)
        results.get(status, results[ERR_UNKNOWN]).append(fp)

  # print results
  print(f'\nSuccess: {results[SUCCESS]}')
  print(f'Failed - FILENAME: {results[ERR_FILE]}')
  print(f'Failed - Coverage: {results[ERR_COVERAGE]}')
  print(f'Failed - Mapping: {results[ERR_MAPPING]}')
  print(f'Failed - Unknown: {results[ERR_UNKNOWN]}')

if __name__ == '__main__':
  main()