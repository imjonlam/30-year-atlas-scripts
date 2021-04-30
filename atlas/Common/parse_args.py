import os
from argparse import ArgumentParser

CONFIG = r'Common\config.json'

def is_valid_file(parser: ArgumentParser, arg: str, meta: str) -> str:
  '''Returns arg if it is a valid file'''
  if not os.path.isfile(arg):
    parser.error(f'The {meta} file: {arg} does not exist!')
  return arg

def argparser_init():
  '''Initialize argument parser'''
  parser = ArgumentParser()
  parser.add_argument('inputs', type=lambda x: is_valid_file(parser, x, 'config'), metavar='config', help="path to config file")
  args = parser.parse_args()
  
  args.config = CONFIG

  return args