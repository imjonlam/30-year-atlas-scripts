'''
SIGRID-3 2014 mapping
Retrieved from: SIGRID REPO 
Author: Fredric
'''

version = '2014'

template_poly = 'template\\{0}\\poly\\'.format(version)

# sigrid 2014 table 1
json_concentration = '{"00" : "98", \
                        "0" : "01", \
                        "0.3" : "01", \
                        "01" : "01", \
                        "02" : "02", \
                        "1" : "10", \
                        "2" : "20", \
                        "3" : "30", \
                        "4" : "40", \
                        "5" : "50", \
                        "6" : "60", \
                        "7" : "70", \
                        "8" : "80", \
                        "9" : "90", \
                        "10" : "92", \
                        "9+" : "91", \
                        "9-10" : "91", \
                        "8-9" : "89", \
                        "8-1" : "81", \
                        "7-9" : "79", \
                        "7-8" : "78", \
                        "6-8" : "68", \
                        "6-7" : "67", \
                        "5-7" : "57", \
                        "5-6" : "56", \
                        "4-6" : "46", \
                        "4-5" : "45", \
                        "3-5" : "35", \
                        "3-4" : "34", \
                        "2-4" : "24", \
                        "2-3" : "23", \
                        "1-3" : "13", \
                        "1-2" : "12", \
                        "X" : "99", \
                        "@" : "-9", \
                        "" : "-9", \
                        " " : "-9" \
                        }'

# sigrid 2014 table 2
json_stage = '{"UNDEF00" : "01", \
                    "UNDEF80" : "80", \
                    "1" : "81", \
                    "2" : "82", \
                    "3" : "83", \
                    "4" : "84", \
                    "5" : "85", \
                    "6" : "86", \
                    "B" : "79", \
                    "7" : "87", \
                    "8" : "88", \
                    "9" : "89", \
                    "UNDEF90" : "90", \
                    "1." : "91", \
                    "UNDEF92" : "92", \
                    "4." : "93", \
                    "UNDEF94" : "94", \
                    "7." : "95", \
                    "8." : "96", \
                    "9." : "97", \
                    "L" : "98", \
                    "X" : "99", \
                    "@" : "-9", \
                    "" : "-9", \
                    " " : "-9" \
                }'

# sigrid 2014 table 3
json_form = '{"00" : "22", \
                    "01" : "01", \
                    "02" : "02", \
                    "03" : "03", \
                    "04" : "04", \
                    "05" : "05", \
                    "06" : "06", \
                    "07" : "07", \
                    "08" : "08", \
                    "UNDEF9" : "09", \
                    "9" : "10", \
                    "0" : "22", \
                    "1" : "01", \
                    "2" : "02", \
                    "3" : "03", \
                    "4" : "04", \
                    "5" : "05", \
                    "6" : "06", \
                    "7" : "07", \
                    "8" : "08", \
                    "UNDEF09" : "09", \
                    "09" : "10", \
                    "X" : "99", \
                    "@" : "-9", \
                    "" : "-9", \
                    " " : "-9" \
                }'		

# sigrid 2014 table 3
json_form_strip = '{"01" : "11", \
                        "02" : "12", \
                        "03" : "13", \
                        "04" : "14", \
                        "05" : "15", \
                        "06" : "16", \
                        "07" : "17", \
                        "08" : "18", \
                        "09" : "19", \
                        "1" : "11", \
                        "2" : "12", \
                        "3" : "13", \
                        "4" : "14", \
                        "5" : "15", \
                        "6" : "16", \
                        "7" : "17", \
                        "8" : "18", \
                        "9" : "19", \
                        "9+" : "91", \
                        "10" : "20", \
                        "UNDEF21" : "21", \
                        "X" : "99", \
                        "@" : "-9", \
                        "" : "-9", \
                        " " : "-9" \
                    }'
                        
# sigrid 2014 used for mapping
json_sigrid = '{"CT" : null, \
                        "CA" : null, \
                        "SA" : null, \
                        "FA" : null, \
                        "CB" : null, \
                        "SB" : null, \
                        "FB" : null, \
                        "CC" : null, \
                        "SC" : null, \
                        "FC" : null, \
                        "CN" : null, \
                        "CD" : null \
                    }'