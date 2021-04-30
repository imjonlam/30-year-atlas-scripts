import os
import json
import time
import logging
from typing import List

from BaseChart import BaseHandler
from Common.utils import logging_init, log_to_gitlab, del_dir
from median_ct import set_median_ct, calc_median_ct, set_median_ct_colours

# global
ROOT = os.path.dirname(os.path.realpath(__file__))

class SpecialChart:
  def __init__(self, input_path: str, config_path: str):
    self.input_path = input_path
    self.config_path = config_path

  def __enter__(self):
    '''Open Streams'''
    self.input_stream = open(self.input_path)
    self.config_stream = open(self.config_path)

    self.inputs = json.load(self.input_stream)
    self.config = json.load(self.config_stream)
    
    self.__prepare()
    return self

  def __prepare(self):
    '''Set additional class members'''
    self.const = self.config['constants']

    self.chart = self.inputs['chart']
    self.outdir = self.inputs['outdir']
    self.supplied = self.inputs.get('ctmeds_supplied', False)

    self.threshold = self.inputs.get('threshold', 1)
    self.threshold = 1 # remove this line to allow for dynamic thresholds

    now = time.strftime('%Y_%m_%d_%H%M%S')
    self.tmp_dir = os.path.join(*self.config['tmpdir'], 
                                'ctmeds_' + now
                               ).format(os.getenv('username'))

  def start_logging(self):
    '''Begin logging'''
    gitlab = self.inputs.get('log_to_gitlab', False)

    if gitlab:
      log_to_gitlab(self.config, self.inputs['chart'])
    else:
      logging_init(self.config, self.inputs['chart'])
  
  def set_methods(self, calc, colour):
    '''Set class methods'''
    self.calc = calc
    self.colour = colour

  def start(self):
    '''Creates new special charts''' 
    logging.info(f'creating {self.chart} charts')

    for region in self.inputs['regions']:
      ctmeds = self.__ctmeds(region)
      fn = self.__filename(region) + '.tif'
      out = os.path.join(self.outdir, fn)
      self.calc(self.config, ctmeds, region, self.threshold, out)
      self.colour(self.const, out, region)

  def __ctmeds(self, region: str) -> str:
    '''Retrieves ctmed directory'''
    if not self.supplied:
      logging.info(f'none supplied. Creating ctmeds for {region}')
      
      # make temporary directory to create ctmeds
      del_dir(self.tmp_dir, remake=True)
      self.__create_ctmeds(region, 
                            self.tmp_dir,
                            self.__historic_dates(region))
      return self.tmp_dir
    else:
      return self.inputs['data'][region]

  def __create_ctmeds(self, region: str, outdir: str, dates: List[str]):
    '''Creates ctmed charts''' 
    with BaseHandler(self.input_path, self.config_path) as base:
      base.inputs['chart'] = 'ctmed'
      base.inputs['outdir'] = outdir
      base.inputs['is_atlas'] = True
      base.inputs['regions'] = [region]
      base.inputs['historic_dates'] = dates

      base.set_methods(set_median_ct, calc_median_ct, set_median_ct_colours)
      base.start()

  def __historic_dates(self, region: str) -> List[str]:
    '''Retrieves historic dates needed'''
    historic_dates = self.config[self.chart].get(region)
    if historic_dates is None:
      historic_dates = self.config[self.chart]['default']

    return historic_dates

  def __filename(self, region: str):
    '''Returns a filename'''
    fn = self.config['filenames'][self.chart]
    return fn.format(region.lower())

  def __exit__(self, exc_type, exc_value, traceback):
    if os.path.exists(self.tmp_dir):
      del_dir(self.tmp_dir)

    self.input_stream.close()
    self.config_stream.close()