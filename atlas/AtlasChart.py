import os
import json
import time
import logging
import calendar
from osgeo import gdal
from typing import List

from Common.utils import (
  logging_init,
  log_to_gitlab,
  del_dir
)
from Common.helper import (
  export,
  set_map,
  get_path,
  set_style,
  set_label,
  set_image,
  open_layer,
  set_legend,
  open_template,
  format_label,
  get_spref,
  reproject_raster,
  reproject_shapefile,
  hide_item
)

# pylint: disable=import-error
from qgis.core import ( 
  QgsApplication,
  QgsProject,
  QgsPrintLayout,
  QgsLayoutItem,
  QgsLayerTree
)

# ignore GDAL stdout errors
gdal.PushErrorHandler('CPLQuietErrorHandler')

# global
ROOT = os.path.dirname(os.path.realpath(__file__))

class AtlasHandler:
  def __init__(self, input_path: str, config_path: str): 
    self.input_path = input_path
    self.config_path = config_path

    self.qgis = QgsApplication([], False)
    self.qgis.initQgis()

  def __enter__(self):
    '''Open Streams'''
    self.input_stream = open(self.input_path)
    self.config_stream = open(self.config_path, encoding='utf-8')

    self.inputs = json.load(self.input_stream)
    self.config = json.load(self.config_stream)
    
    self.__prepare()
    return self

  def __prepare(self):
    now = time.strftime('%Y_%m_%d_%H%M%S')
    self.tmp_dir = os.path.join(*self.config['tmpdir'], 
                                'atlas_tmp_' + now
                               ).format(os.getenv('username'))

  def start_logging(self, config):
    '''Begin logging'''
    gitlab = self.inputs.get('log_to_gitlab', False)

    if gitlab:
      log_to_gitlab(self.config, self.inputs['chart'])
    else:
      logging_init(self.config, self.inputs['chart'])

  def start(self):
    '''Starts the creation of atlas chart(s)'''
    logging.info('initializing QGIS')

    self.chart = self.inputs['chart']
    special_charts = ['breakup', 'ctfup', 'fifup']

    for region in self.inputs['regions']:

      # create one special chart
      if self.chart in special_charts:
        # create temporary directory to hold reprojected files
        del_dir(self.tmp_dir, remake=True)

        fn = self.__filename(region)
        chart = AtlasChart(self.config, self.inputs, region)
        chart.create(self.tmp_dir, self.inputs['outdir'], fn)

      # create one chart per historic date
      else:
        for date in self.inputs['historic_dates']:
          # create temporary directory to hold reprojected files
          del_dir(self.tmp_dir, remake=True)

          fn = self.__filename(region, date)
          chart = AtlasChart(self.config, self.inputs, region, date)
          chart.create(self.tmp_dir, self.inputs['outdir'], fn)

  def __filename(self, region: str, date: str=None) -> str:
    '''Returns a filename'''
    chart = self.inputs['chart']
    fn = self.config['filenames'][chart]

    if chart == 'oifrq':
      threshold = self.inputs.get('threshold', 1)
      threshold = 'i' if threshold == 1 else threshold
      return fn.format(region.lower(), threshold, date)
    else:
      return fn.format(region.lower(), date)

  def __exit__(self, exc_type, exc_value, traceback):
    self.qgis.exitQgis()
    self.input_stream.close()
    self.config_stream.close()

    if os.path.exists(self.tmp_dir):
      del_dir(self.tmp_dir)

class AtlasChart:
  def __init__(self, config: dict, inputs: dict, region: str, date: str=None):
    self.date = date
    self.config = config
    self.region = region

    self.data = inputs['data']
    self.years = inputs['years']
    self.chart = inputs['chart']
    self.is_atlas = inputs.get('is_atlas', False)

    self.threshold = inputs.get('threshold', 1)
    # remove these lines to allow for dynamic thresholds
    if self.chart != 'oifrq':
      self.threshold = 1

  def create(self, tmp_dir: str, out_dir: str, fn: str):
    '''Create an Atlas Chart'''
    # setup QGS
    self.project = QgsProject()
    self.layout = QgsPrintLayout(self.project)
    en, fr = QgsLayerTree(), QgsLayerTree()

    chart = self.chart
    region = self.region

    # get output path
    out = os.path.join(out_dir, fn)
    logging.info(f'creating atlas chart: {fn}')

    # load template
    template = get_path(self.config['templates'][chart], region.lower())
    open_template(self.layout, template)

    # set image sources
    set_image(self.layout, 'canada', get_path(self.config['canada']))
    set_image(self.layout, 'environment_canada', get_path(self.config['environmentcanada']))

    # load base layers
    paths = self.__get_base_paths(fn)
    if len(paths) == 0:
      logging.warning(f'insufficient files found to create {out}, skipping')
      return

    paths = self.__reproject(paths, tmp_dir)
    self.__set_base(paths)

    # add layers to map
    self.__set_latlong()
    self.__set_land()
    self.__set_legend(en, fr)
    self.__set_map()

    # set text
    self.__format_title_label()
    self.__set_date_label()

    if self.is_atlas:
      self.__set_analogues_label()
    else:
      self.__hide_analogue_items()

    # export
    export(self.layout, out)

  def __reproject(self, paths: List[str], out_dir: str) -> List[str]:
    '''Reprojects and returns a list of reprojected file paths'''
    wkt = os.path.join(ROOT, *self.config['wkt'])
    spref = get_spref(wkt, self.config['projections'][self.region])

    reprojected = []
    for fp in paths:
      if fp.endswith('.tif') or fp.endswith('.tiff'):
        reprojected.append(reproject_raster(fp, spref, out_dir))
      else:
        reprojected.append(reproject_shapefile(fp, spref, out_dir))

    return reprojected

  def __set_legend(self, en: QgsLayerTree, fr: QgsLayerTree):
    '''Add legend layers'''
    self.legend = open_layer(self.project, get_path(self.config['legend']))
    set_style(self.legend, get_path(self.config['legend_style'][self.chart], ['EN', self.region]))
    set_legend(self.layout, en, self.legend, 'l_color')
    
    set_style(self.legend, get_path(self.config['legend_style'][self.chart], ['FR', self.region]))
    set_legend(self.layout, fr, self.legend, 'r_color')

  def __get_base_paths(self, fn: str) -> List[str]:
    '''Returns a list of base file paths'''
    logging.info(f'getting required base files to make {fn}')

    # define overlaps (bottom <-> top)
    if self.region == 'AR':
      if self.data.get('AR'):
        regions = ['AR']
      else:
        regions = ['HB', 'WA', 'EA']
    elif self.is_atlas:
      if self.region == 'EA':
        regions = ['HB', 'EA']
      elif self.region == 'WA':
        regions = ['WA', 'EA']
      elif self.region == 'HB':
        regions = ['HB', 'EA']
      else:
        regions = [self.region]
    else:
      regions = [self.region]

    # get all sub-region charts
    basename, _ = os.path.splitext(fn[2:])
    paths = []
    for sub_region in regions:
      sub_fn = sub_region.lower() + basename
      path = os.path.join(self.data[sub_region], sub_fn, sub_fn)

      # find files
      if os.path.exists(path + '.shp'):
        paths.append(path + '.shp')
      elif os.path.exists(path + '.tif'):
        paths.append(path + '.tif')
      else:
        paths.clear()
        logging.warning(f'could not find required file: {path}.shp or {path}.tif')

    return paths

  def __set_base(self, paths: List[str]):
    '''Set base layers from a list of chart paths'''
    # get style path
    key = 'vector_style' if paths[0].endswith('.shp') else 'raster_style'
    params = [self.threshold] if self.chart == 'oifrq' else [self.region, self.threshold]
    style = get_path(self.config[key][self.chart], params)

    # open layers
    self.base_maps = []
    for fp in paths:
      base = open_layer(self.project, fp)
      set_style(base, style)

      self.base_maps.append(base)

  def __set_land(self):
    '''Set land layers'''
    fp = os.path.join(ROOT, *self.config['land'])
    style = get_path(self.config['land_style'])

    self.land = open_layer(self.project, fp)
    set_style(self.land, style)

  def __set_latlong(self):
    '''Set latlong layers'''
    style = get_path(self.config['latlong_style'][self.region])

    fp = get_path(self.config['latlong_minor'])
    self.minor = open_layer(self.project, fp)
    set_style(self.minor, style)
    
    fp = get_path(self.config['latlong_major'])
    self.major = open_layer(self.project, fp)
    set_style(self.major, style)

  def __set_map(self):
    '''Add layers to the map'''
    set_map(self.layout, 'colormap',
            [self.major, self.minor, *self.base_maps])
    set_map(self.layout, 'landmap', [self.land])
    set_map(self.layout, 'legendmap', [self.legend])

  def __format_title_label(self):
    '''Formats title in template'''
    if self.chart in ['oifrq', 'ctfup', 'breakup']:
      params = [self.threshold, self.threshold]
      format_label(self.layout, 'title', params)

  def __set_date_label(self):
    '''Sets date label in template'''
    start, end = self.years[0], self.years[-1]
    label = f'{start} - {end}'

    # need to include historic_date if it's not a special chart
    if self.chart not in ['breakup', 'ctfup', 'fifup']:
      month, day = int(self.date[0:2]), self.date[2:4]
      en_month = calendar.month_abbr[month].upper()
      fr_month = self.config['translation'][en_month]

      # SUBJECT TO CHANGE
      # some climate shapefiles are missing in 1991-2020 
      # and use 1990-2019 instead for EC and GL
      if self.region in ['EC', 'GL'] and self.is_atlas:
        label = f'{start-1}/{start} - {end-1}/{end}'

      label = f'{en_month} {day} / {day} {fr_month}\n {label}'
    
    set_label(self.layout, 'date_text', label)
        
  def __set_analogues_label(self):
    '''Sets analogues label in template'''
    if self.chart not in ['breakup', 'ctfup', 'fifup']:
      analogues = self.config['analogue'].get(self.date)
      if analogues is None:
        analogues = self.config['analogue']['default']
      
      if self.region == 'AR':
        params = [analogues['EA'], analogues['WA'], analogues['HB']]
      else:
        params = [analogues[self.region]]
      
      format_label(self.layout, 'info_subtext', params)

  def __hide_analogue_items(self):
    '''Hides all related analogue items'''
    ids = ['info_title', 'info_text', 'info_subtext', 'info_box']
    for item_id in ids:
      hide_item(self.layout, item_id)