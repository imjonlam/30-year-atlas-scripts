'''
MANICE mapping
Retrieved from: SIGRID REPO 
Author: Fredric
'''
#   0   1    2    3    4    5    6    7     8    9    10  11    12   13   14  15    16
#   C   C    C    C     X  S(CN) S    S     S    S    X   F     F    F    X   X     X
# %ct%_%ca%_%cb%_%cc%_%cd%_%so%_%sa%_%sb%_%sc%_%sd%_%se%_%fa%_%fb%_%fc%_%fd%_%fe%_%csp%	
#	CT(String)  
#	CA(String)  
#	SA(String)  
#	FA(String)  
#	CB(String)  
#	SB(String)  
#	FB(String)  
#	CC(String)  
#	SC(String)  
#	FC(String)  
#	CN(String)  ?
#	CD(String)  
#	CF(String)  ?

#	EGG_ATTR(String) 6_1_4_1_@_@_5_4_1_@_@_@_@_@_@_@_~9+
#	CT(String) 60 -
#	CA(String) 10 -
#	SA(String) 85 -
#	FA(String) -9 -
#	CB(String) 40 -
#	SB(String) 84 -
#	FB(String) -9 -
#	CC(String) 10 -
#	SC(String) 81 -
#	FC(String) -9 -
#	CN(String) -9 -
#	CD(String) 81 -
#	CF(String) 20-9 ?

import json
from collections import OrderedDict

# constant that define the egg
delimiter = '_'
csp_trim = '~'
null = '@'

# hardcoded egg
egg_attr_bergy_water = "02_@_@_@_@_@_L_@_@_@_@_9_@_@_@_@_@"
egg_attr_open_water = "01_@_@_@_@_@_X_@_@_@_@_X_@_@_@_@_@"
egg_attr_ice_free = "00_@_@_@_@_@_@_@_@_@_@_@_@_@_@_@_@"
egg_attr_ice_glace = "X_@_@_@_@_@_X_@_@_@_@_X_@_@_@_@_@"
egg_attr_fast_ice_default = "10_@_@_@_@_@_@_@_@_@_@_8_@_@_@_@_@"
egg_attr_ice_shelf = "10_@_@_@_@_@_L_@_@_@_@_9_@_@_@_@_@" # new
#TODO: FIX ICE SHELF L-> 7.

# null will be converted into sigrid value at runtime
json_egg_attr_fast_ice = '{"10_@_@_@_@_@_@_@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_1_@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_4_@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_5_@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_7_@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_1._@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_4._@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_7._@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_8._@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_9._@_@_@_@_8_@_@_@_@_@" : null, \
                            "10_@_@_@_@_@_X_@_@_@_@_8_@_@_@_@_@" : null}'

parsed_json_egg_attr_fast_ice = json.loads(json_egg_attr_fast_ice, object_pairs_hook=OrderedDict)

# point used to create polygon
# added 900 to land #new
json_point_poly = '{ "bergy_water" : [101, 127], \
                    "open_water" : [107, 126], \
                    "ice_free" : [115, 125], \
                    "ice_glace" : [144, 145], \
                    "fast_ice" : [106, 124], \
                    "ice_shelf" : [146], \
                    "no_data" : [123, 128, 133, 143, 147], \
                    "land" : [400, 900], \
                    "skip" : [934] \
                }'

parsed_json_point_poly = json.loads(json_point_poly, object_pairs_hook=OrderedDict)

# manice fields index
json_egg = '{ "CT" : 0, \
                "CA" : 1, \
                "CB" : 2, \
                "CC" : 3, \
                "CD" : 4, \
                "SO" : 5, \
                "SA" : 6, \
                "SB" : 7, \
                "SC" : 8, \
                "SD" : 9, \
                "SE" : 10, \
                "FA" : 11, \
                "FB" : 12, \
                "FC" : 13, \
                "FD" : 14, \
                "FE" : 15, \
                "CSP" : 16 \
            }'

parsed_json_egg = json.loads(json_egg, object_pairs_hook=OrderedDict)

# fews fields to reduce the amount of code
field_count = len(parsed_json_egg)
ca_index = parsed_json_egg["CA"]
cb_index = parsed_json_egg["CB"]
cc_index = parsed_json_egg["CC"]
fa_index = parsed_json_egg["FA"]
fb_index = parsed_json_egg["FB"]
fc_index = parsed_json_egg["FC"]
csp_index = parsed_json_egg["CSP"]

# mapping of manice index to sigrid (also work for IOC)
json_sigrid_mapping = '{ "0" : "CT", \
                            "1" : "CA", \
                            "2" : "CB", \
                            "3" : "CC", \
                            "4" : null, \
                            "5" : "CN", \
                            "6" : "SA", \
                            "7" : "SB", \
                            "8" : "SC", \
                            "9" : "CD", \
                            "10" : null, \
                            "11" : "FA", \
                            "12" : "FB", \
                            "13" : "FC", \
                            "14" : null, \
                            "15" : null, \
                            "16" : null \
                        }'

parsed_json_sigrid_mapping = json.loads(json_sigrid_mapping, object_pairs_hook=OrderedDict)

# point and line used to create polygon, if this chage for 2004, it can be moved into the individual sigrid data files
json_sigrid_poly = '{ "Line" : [8,117,122,128,140,141,150,162,183,201,218,222], \
                        "Point" : [101,106,107,115,117,118,120,122,123,128,133,143,144,146,147,400] \
                    }'

parsed_json_sigrid_poly = json.loads(json_sigrid_poly, object_pairs_hook=OrderedDict)

# used to show on the log/screen what it is
json_point = '{ "100" : "ice drift", \
                "101" : "bergy water", \
                "102" : "diverging", \
                "103" : "converging", \
                "104" : "est thickness", \
                "105" : "thickness", \
                "106" : "fastice", \
                "107" : "open water", \
                "108" : "melting stage", \
                "109" : "rafting", \
                "110" : "ridges", \
                "111" : "shearing", \
                "112" : "strips patches", \
                "113" : "snow cover", \
                "114" : "zero ice drift", \
                "115" : "ice free", \
                "116" : "freetext", \
                "117" : "inside egg", \
                "118" : "remote egg", \
                "119" : "att label", \
                "120" : "att label anchor", \
                "121" : "att egg", \
                "122" : "att egg anchor", \
                "123" : "nodata 1", \
                "124" : "fastice label", \
                "125" : "ice free label", \
                "126" : "open water label", \
                "127" : "bergy water label", \
                "128" : "nodata 2", \
                "129" : "freetext label", \
                "130" : "roughness", \
                "131" : "roughness label", \
                "132" : "ship", \
                "133" : "nodata 3", \
                "134" : "double egg", \
                "135" : "ethickness label", \
                "136" : "mthickness label", \
                "137" : "ice island", \
                "138" : "ice island label", \
                "139" : "crack", \
                "143" : "never data", \
                "144" : "ice glace", \
                "145" : "ice glace label", \
                "146" : "ice shelf", \
                "147" : "auto nodata", \
                "148" : "lpressure", \
                "149" : "lpressure label", \
                "150" : "mpressure", \
                "151" : "mpressure label", \
                "152" : "spressure", \
                "153" : "spressure label", \
                "154" : "leadclose", \
                "155" : "leadclose label", \
                "156" : "ridging", \
                "157" : "ridging label", \
                "158" : "unlpresence", \
                "159" : "unlpresence label", \
                "200" : "chartt ll", \
                "201" : "chartt ul", \
                "202" : "chartt ur", \
                "203" : "chartt lr", \
                "204" : "chartt rem eggs", \
                "300" : "anno egg", \
                "400" : "land", \
                "900" : "egg centroid", \
                "934" : "inside eggedge", \
                "935" : "outside eggedge" \
            }'

parsed_json_point = json.loads(json_point, object_pairs_hook=OrderedDict)