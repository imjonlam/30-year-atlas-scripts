'''
SIGRID-3
Retrieved from: SIGRID REPO 
Author: Fredric
'''

import json
from collections import OrderedDict

from . import sigrid_data_2014 as sigrid_data_json

version = sigrid_data_json.version

template_poly = sigrid_data_json.template_poly
    
# will contain mapped value
json_sigrid_value = sigrid_data_json.json_sigrid

parsed_json_concentration = json.loads(sigrid_data_json.json_concentration, object_pairs_hook=OrderedDict)
parsed_json_stage = json.loads(sigrid_data_json.json_stage, object_pairs_hook=OrderedDict)
parsed_json_form = json.loads(sigrid_data_json.json_form, object_pairs_hook=OrderedDict)
parsed_json_form_strip = json.loads(sigrid_data_json.json_form_strip, object_pairs_hook=OrderedDict)
parsed_json_sigrid = json.loads(sigrid_data_json.json_sigrid, object_pairs_hook=OrderedDict)

parsed_json_sigrid['CT'] = parsed_json_concentration
parsed_json_sigrid['CA'] = parsed_json_concentration
parsed_json_sigrid['CB'] = parsed_json_concentration
parsed_json_sigrid['CC'] = parsed_json_concentration

parsed_json_sigrid['CD'] = parsed_json_stage
parsed_json_sigrid['SA'] = parsed_json_stage
parsed_json_sigrid['SB'] = parsed_json_stage
parsed_json_sigrid['SC'] = parsed_json_stage
parsed_json_sigrid['CN'] = parsed_json_stage

parsed_json_sigrid['FA'] = parsed_json_form
parsed_json_sigrid['FB'] = parsed_json_form
parsed_json_sigrid['FC'] = parsed_json_form
    
null = '-9'
fastice_fa = '08'
fastice_fb = '08'
fastice_fc = '08'

# Ice shelf should be transposed to SIGRID
valid_poly_type = {'with data' : {'I', 'W'},
                   'without data': {'L','N'}}

# valid_poly_type = {'with data' : {'I', 'W'},
#                    'without data': {'L','S','N'}}