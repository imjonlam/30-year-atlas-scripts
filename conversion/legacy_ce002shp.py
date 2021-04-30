#!/usr/bin/env python3.6
########################################################
#                                                      # 
#                CLIMATE E00 TO SIGRID                 # 
#                [Manual Conversion]                   #
#  Fred -> Raghavan -> modify shapefile -> + metadata  #
#           ONLY use when ce002shp.py fails            # 
#                                                      # 
########################################################

'''
Purpose of this file is to run manual conversion of Climate E00->Sigrid compliant Climate
- Used in cases where ce002shp.py fails
- Uses: Fred -> Raghavan -> modify shapefile + add metadata
'''

import os
import sys
import json
import argparse
import datetime
import subprocess
import os.path as op

sys.path.append('..')
from Common.helper import makeDir, toTar, removeDir

# GLOBAL
ROOT = op.abspath(op.join(__file__, op.pardir, op.pardir))
CONFIG = r'..\Common\config.json'

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input', help='path to .e00')
  parser.add_argument('output', help='output directory')
  parser.add_argument('metadata', help='path to metadata')
  args = parser.parse_args()

  if not os.path.isdir(args.output):
    parser.error('invalid output directory')
  
  if not os.path.isfile(args.input) or not args.input.endswith('.e00'):
    parser.error('invalid e00 provided')

  # setup
  e00, out, meta = args.input, args.output, args.metadata
  fn, _ = os.path.splitext(os.path.basename(e00))
  fn_split = fn.upper().split('_')
  region, date = fn_split

  if len(fn_split) != 2:
    parser.error('invalid e00 format provided')

  if region not in ['EA', 'WA', 'HB', 'EC', 'GL'] and len(date) != 6:
    parser.error('invalid e00 format provided')

  with open(CONFIG) as f:
    config = json.load(f)

  now = datetime.datetime.now()
  year = '19' if int(date[0:2]) > abs(now.year) % 100 else '20'
  date = year + date
  sigrid_name = '{0}_SGRDR{1}_{2}'.format('CIS', region, date)
  climate_name = '{0}_{1}_{2}_{3}_{4}'.format('CIS', region, date, 'pl', 'a')
  
  # Run Fred's script
  sigrid = os.path.join(out, sigrid_name)
  script = os.path.join(*config['create_poly'])
  subprocess.Popen(['py -2', script, e00, '-o', sigrid, '-m', meta, '-zip', 'y' ,'-sigrid-version', '2014']).wait()
  zipped = os.path.join(out, sigrid_name +'.zip')

  # Run Raghavan's script
  climate = os.path.join(out, climate_name)
  script = os.path.join(ROOT, *config['sigrid2climate]'])
  subprocess.Popen(['py -3', script, zipped, climate]).wait()

  # archive and cleanup
  toTar(climate, out)
  removeDir(climate)
  os.remove(zipped)

if __name__ == '__main__':
  main()