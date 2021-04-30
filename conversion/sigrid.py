#!/usr/bin/env python3.6
##################################################
#                                                #
#                SIGRID Methods                  #
#         Retrieved and modified to GDAL         #
#      Source: SIGRID repo, Author: Fredric      #
#                                                #
##################################################
import os
import json
import math
from collections import OrderedDict

import Data.manice_data as manice_data
import Data.sigrid_data as sigrid_data

def try_fix_poly_type(poly_type, egg_name, point_type, coverage_type = ''):
  fixed_poly_type = poly_type

  if point_type in manice_data.parsed_json_point_poly['no_data']:
      fixed_poly_type = 'N'

  elif point_type in manice_data.parsed_json_point_poly['ice_glace']:
      fixed_poly_type = 'I'

  elif egg_name == 'SM':
      fixed_poly_type = 'N'

  elif point_type in manice_data.parsed_json_point_poly['land']:
      fixed_poly_type = 'L'

  elif point_type in manice_data.parsed_json_point_poly['bergy_water']:
      if coverage_type == 'AN-ICE' and egg_name == 'BF':
          fixed_poly_type = 'W'
      else:
          fixed_poly_type = 'I'

  elif point_type in manice_data.parsed_json_point_poly['open_water']:
      fixed_poly_type = 'I'

  elif point_type in manice_data.parsed_json_point_poly['fast_ice']:
      fixed_poly_type = 'I'

  elif point_type in manice_data.parsed_json_point_poly['ice_shelf']:
      fixed_poly_type = 'S'

  elif point_type in manice_data.parsed_json_point_poly['ice_free']:
      fixed_poly_type = 'W'

  return fixed_poly_type

def try_fix_empty_egg(egg_attr, egg_name, poly_type, point_type, force, saved_sigrid):
  fixed_egg = egg_attr
  force_overwrite = False
  can_be_sm = True

  if point_type in manice_data.parsed_json_point_poly['ice_glace']:
    can_be_sm = False

  if force or egg_attr == ' ':
    if point_type in manice_data.parsed_json_point_poly['bergy_water']:
      fixed_egg = manice_data.egg_attr_bergy_water

    elif point_type in manice_data.parsed_json_point_poly['open_water']:
      fixed_egg = manice_data.egg_attr_open_water

    elif point_type in manice_data.parsed_json_point_poly['ice_free']:
      fixed_egg = manice_data.egg_attr_ice_free

    elif point_type in manice_data.parsed_json_point_poly['ice_glace']:
      fixed_egg = manice_data.egg_attr_ice_glace

    elif point_type in manice_data.parsed_json_point_poly['ice_shelf']: # NEW
      fixed_egg = manice_data.egg_attr_ice_shelf

    elif point_type in manice_data.parsed_json_point_poly['fast_ice']:
      if fixed_egg not in manice_data.parsed_json_egg_attr_fast_ice:
          
        found = False

        for k,v in manice_data.parsed_json_egg_attr_fast_ice.items():
          if v == saved_sigrid:
            fixed_egg = k
            found = True
            break

        if not found:
          fixed_egg = manice_data.egg_attr_fast_ice_default

    elif point_type in manice_data.parsed_json_point_poly['land']:
      fixed_egg = ' '

    elif point_type in manice_data.parsed_json_point_poly['no_data']:
      fixed_egg = ' '

  if can_be_sm and (egg_name == 'SM' or poly_type == 'N'):
    fixed_egg = ' '
    force_overwrite = True

  return fixed_egg, force_overwrite

def map_egg_to_sigrid(egg, poly_type, report):	
  values = egg.split(manice_data.delimiter)
  parsed_json_sigrid_value = json.loads(sigrid_data.json_sigrid_value, object_pairs_hook=OrderedDict)

  if poly_type in sigrid_data.valid_poly_type['without data']:
    for item in parsed_json_sigrid_value:
      parsed_json_sigrid_value[item] = ' '

  elif len(values) == manice_data.field_count:   
    for idx, value in enumerate(values):
      map = manice_data.parsed_json_sigrid_mapping[str(idx)]
      
      if map:
        try:
          parsed_json_sigrid_value[map] = sigrid_data.parsed_json_sigrid[map][value]

        except KeyError:
          parsed_json_sigrid_value[map] = sigrid_data.null

  else:
    for item in parsed_json_sigrid_value:
      parsed_json_sigrid_value[item] = ' '

  return parsed_json_sigrid_value