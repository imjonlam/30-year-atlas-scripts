# #!/usr/bin/env python2.7
########################################################
#                                                      # 
#                  E00 TO Coverage                     # 
#                 [Requires: Arcpy]                    #
#                                                      # 
########################################################

import os
import sys  
import argparse

sys.path.append('..')
from Common import makeDir

def extract(e00, dest, fn):
  print(r'extracting {} to {}\{}'.format(e00, dest, fn))
  import arcpy
  arcpy.ImportFromE00_conversion(e00, dest, fn)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input', type=str, help='directory of e00s OR path to 1x e00')
  parser.add_argument('output', type=str, help='output directory')
  args = parser.parse_args()
  
  if not os.path.isdir(args.input) and not args.input.endswith('.e00'):
    parser.error('invalid input')

  # setup
  if os.path.isfile(args.input):
    e00s = [args.input]
  else:
    e00s = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith('.e00')]

  # begin
  for fp in e00s:
    fn, _ = os.path.splitext(os.path.basename(fp))
    coverage = os.path.join(args.output, fn)

    if not os.path.exists(coverage):
      makeDir(coverage)

    extract(fp, coverage, fn)

if __name__ == '__main__':
  main()