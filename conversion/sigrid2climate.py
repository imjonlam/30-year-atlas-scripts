#!/usr/bin/env python3.6
####################################################
#                                                  #
#                 SIGRID2Climate                   #
# Converts shapefile with SIGRID fields to climate #
#           Source: Climate/autoupdate             #
#     Note: modified. Use ONLY with ce002shp.py    #
#                                                  #
####################################################
import os
import sys
import json
import codecs
from osgeo import ogr
from math import ceil
import xml.etree.ElementTree as ElementTree

import Data.sigrid_to_manice as sigrid_to_manice

# GLOBAL
ROOT = os.path.dirname(os.path.realpath(__file__))
CONFIG = r'Common\config.json'

USAGE="""Sigrid2ClimateShp.py {SIGRID folder/tar/zip} {output folder}"""
    
def main(in_shp, out_path):
    """
    in_shp: Path to a SIGRID shapefile to convert or a directory containing 
        a shapefile with the same name as the directory
    out_path: Path to the directory where the converted shapefile will 
        be saved to
    """
    ## Initialization
    shp_driver = ogr.GetDriverByName('ESRI Shapefile')
    mem_driver = ogr.GetDriverByName('MEMORY')
    
    # Get the file's name
    if os.path.isdir(in_shp):
        # Assume the shapefile's name is the same as the folder
        shp_fn = os.path.split(os.path.normpath(in_shp))[1] + ".shp"
        in_shp_file = os.path.join(in_shp, shp_fn)
    else:
        in_shp_file = in_shp

    in_path, basename = os.path.split(in_shp_file)
    in_fn, in_ext = os.path.splitext(basename)
    
    # Initialize the memory datasource
    mem_path = 'Sigrid2ClimateShp_{}'.format(in_fn)
    mem_ds = mem_driver.CreateDataSource(mem_path)
    
    fn_split = in_fn.split("_")
    if len(fn_split) < 3:
        raise ValueError("Invalid file name {}".format(in_shp_file))

    # Determine the product type and region
    input_prd_id = fn_split[1]
    region = input_prd_id[5:]
    
    # We use a different set of manice fields for lake ice ('great lakes' region)
    if region.upper() == 'GL':
        is_sea = False
    else:
        is_sea = True
        
    # Determine the output file name (which is also the layer name)
    basename = os.path.basename(out_path)
    out_name = os.path.splitext(basename)[0]
        
    # Copy the layer to memory
    in_ds = shp_driver.Open(in_shp)
    in_lyr = in_ds.GetLayer()
    mem_lyr_name = "INPUT_{}".format(region)
    mem_layer = mem_ds.CopyLayer(
            in_lyr, mem_lyr_name, ['OVERWRITE=YES'])
    in_lyr = None
    in_ds = None
    
    ## Modify the in-memory copy of the input
    lyr_def = mem_layer.GetLayerDefn()
    
    # Add a REGION field to the memory copy of the layer
    field_def = ogr.FieldDefn('REGION', ogr.OFTString)
    field_def.SetWidth(2)
    mem_layer.CreateField(field_def)
    sql_query = """UPDATE "{}" SET REGION = '{}'""".format(
            mem_lyr_name, region)
    mem_ds.ExecuteSQL(sql_query, dialect="sqlite")
    
    # Fix width and precision of AREA and PERIMETER fields to stop warnings
    # ( https://trac.osgeo.org/gdal/ticket/6803 and https://bitbucket.org/natcap/invest/pull-requests/123/fixes-3462-manually-setting-the-widths-and/diff )
    field_idx = lyr_def.GetFieldIndex('AREA')
    field_def = lyr_def.GetFieldDefn(field_idx)
    field_def.SetWidth(26)
    field_def.SetPrecision(11)
    mem_layer.AlterFieldDefn(field_idx, field_def, 
            ogr.ALTER_WIDTH_PRECISION_FLAG)
            
    field_idx = lyr_def.GetFieldIndex('PERIMETER')
    field_def = lyr_def.GetFieldDefn(field_idx)
    field_def.SetWidth(26)
    field_def.SetPrecision(11)
    mem_layer.AlterFieldDefn(field_idx, field_def, 
            ogr.ALTER_WIDTH_PRECISION_FLAG)
    
    ## Create the final output shapefile
    out_shp_path = os.path.join(out_path, out_name + '.shp')
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    elif os.path.exists(out_shp_path):
        shp_driver.DeleteDataSource(out_shp_path)
    out_ds = shp_driver.CreateDataSource(out_shp_path)
    out_layer = out_ds.CopyLayer(
            mem_layer, out_name, ['OVERWRITE=YES'])
    
    ## Add and compute climate fields
    # Tuples represent field name and length of field 
    #  (all fields are character/TEXT fields)
    add_fields = [("PNT_TYPE", 3)]
    if is_sea:
        add_fields.extend(
                [("E_CT", 2), ("E_CA", 1), ("E_CB", 1), ("E_CC", 1), 
                ("E_CD", 1), ("E_SO", 2), ("E_SA", 2), ("E_SB", 2),
                ("E_SC", 2), ("E_SD", 2), ("E_SE", 2), ("E_FA", 1),
                ("E_FB", 1), ("E_FC", 1), ("E_FD", 1), ("E_FE", 1),
                ("E_CS", 2), ("R_CT", 2), ("R_CMY", 1), ("R_CSY", 1),
                ("R_CFY", 1), ("R_CGW", 1), ("R_CG", 1), ("R_CN", 1),
                ("R_PMY", 1), ("R_PSY", 1), ("R_PFY", 1), ("R_PGW", 1),
                ("R_PG", 1), ("R_PN", 1), ("R_CS", 2), ("R_SMY", 1),
                ("R_SSY", 1), ("R_SFY", 1), ("R_SGW", 1), ("R_SG", 1),
                ("R_SN", 1), ("N_CT", 4), ("N_COI", 4), ("N_CMY", 4),
                ("N_CSY", 4), ("N_CFY", 4), ("N_CFY_TK", 4),
                ("N_CFY_M", 4), ("N_CFY_TN", 4), ("N_CYI", 4),
                ("N_CGW", 4), ("N_CG", 4), ("N_CN", 4), ("N_CB", 4)])
    else:
        add_fields.extend(
                [("E_CT", 2), ("E_CA", 1), ("E_CB", 1), ("E_CC", 1), 
                ("E_CD", 1), ("E_SO", 2), ("E_SA", 2), ("E_SB", 2),
                ("E_SC", 2), ("E_SD", 2), ("E_SE", 2), ("E_FA", 1),
                ("E_FB", 1), ("E_FC", 1), ("E_FD", 1), ("E_FE", 1),
                ("E_CS", 2), ("R_CT", 2), ("R_CTK", 2), ("R_CM", 2),
                ("R_CTN", 2), ("R_CN", 2), ("R_N1", 2), ("R_N2", 2),
                ("R_N3", 2), ("R_CS", 2), ("N_CT", 4), ("N_CVTK", 4),
                ("N_CTK", 4), ("N_CM", 4), ("N_CTN", 4), ("N_CN", 4)])
        
    # All fields are type ogr.OFTString ('TEXT' in shapefiles)
    field_def = ogr.FieldDefn("UNSET", ogr.OFTString)
    for f_tuple in add_fields:
        field_def.SetWidth(f_tuple[1])
        field_def.SetName(f_tuple[0])
        out_layer.CreateField(field_def)
        
    # store conversion tables
    sgd_version = '2014'
    if sgd_version == '2014':
        conv_table = dict()
        conv_table['cct_regular'] = sigrid_to_manice.cct_regular
        conv_table['cct_special'] = sigrid_to_manice.cct_special
        conv_table['form_regular'] = sigrid_to_manice.form_regular
        conv_table['stage_regular'] = sigrid_to_manice.stage_regular
    else:
        raise ValueError("Unsupported SIGRID version '{}'".format(sgd_version))
    
    copied_climate_fields = [
            ("E_CT", 'CT', 'cct_regular'),
            ("E_CA", 'CA', 'cct_regular'),
            ("E_CB", 'CB', 'cct_regular'), # CONFIRM: CB > CA?
            ("E_CC", 'CC', 'cct_regular'),
            ("E_FA", 'FA', 'form_regular'),
            ("E_FB", 'FB', 'form_regular'),
            ("E_FC", 'FC', 'form_regular'),
            ("E_SO", 'CN', 'stage_regular'),
            ("E_SA", 'SA', 'stage_regular'),
            ("E_SB", 'SB', 'stage_regular'),
            ("E_SC", 'SC', 'stage_regular'),
            ("E_SD", 'CD', 'stage_regular')]
                    
    # Pairs represent an ice stage field and its corresponding concentration field
    stage_cct_pairs = [
            ('E_SA', 'E_CA'), ('E_SB', 'E_CB'),
            ('E_SC', 'E_CC'), ('E_SD', 'E_CD')]
    
    for cur_feat in out_layer:
        skip = False
        
        ## Check for specific ice types
        # Set specific field values for the feature types noted in
        # Appendix 3 & 4 of the flowchart.
        # Also set the PNT_TYPE field - needed for the area calculation 
        # and departure from normal steps in the autoupdate system.
        # - We will use the POLY_TYPE field from the SIGRID format first
        # - For POLY_TYPE="I", we will need to look at the 
        #   total concentration (CT) and ice form (FA) 
        #   to determine the PNT_TYPE.
        cur_ct = cur_feat.GetField('CT')
        cur_poly_type = cur_feat.GetField('POLY_TYPE')
        if cur_poly_type == "L":
            # Land
            new_pnt = '400'
            for field_t in add_fields:
                cur_feat.SetField(field_t[0], '')
            skip = True
        elif cur_poly_type == "N":
            # No data
            new_pnt = '123'
            for field_t in add_fields:
                cur_feat.SetField(field_t[0], '')
            skip = True
        elif cur_poly_type == "W":
            # Ice Free
            new_pnt = '115'
            for field_t in add_fields:
                cur_feat.SetField(field_t[0], '')
                cur_feat.SetField('N_CT', '0.0')
            skip = True
        elif cur_poly_type == "I":
            # Ice
            if cur_ct == '02': 
                # Bergy Water
                new_pnt = '101'
                for field_t in add_fields:
                    cur_feat.SetField(field_t[0], '')
                cur_feat.SetField('N_CT', '0.2')
                cur_feat.SetField('N_CB', '0.2')
                skip = True
            elif cur_ct == '01': 
                # Open water
                new_pnt = '107'
                for field_t in add_fields:
                    cur_feat.SetField(field_t[0], '')
                cur_feat.SetField('N_CT', '0.3')
                skip = True
            elif cur_feat.GetField('FA') == '08':
                # Fast Ice
                new_pnt = '106'
            else: 
                # (TODO: Should we use 120 or another valid egg PNT_TYPE?)
                # Attached egg label anchor 
                new_pnt = '120'
        elif cur_poly_type == "S": 
            # Ice Shelf
            new_pnt = '146'
            for field_t in add_fields:
                cur_feat.SetField(field_t[0], '')
            cur_feat.SetField('N_CT', '10.0')
            cur_feat.SetField('N_COI', '0.0')
            cur_feat.SetField('N_CFY', '0.0')
            cur_feat.SetField('N_CYI', '0.0')
            cur_feat.SetField('N_CN', '0.0')
            cur_feat.SetField('N_CB', '10.0')
            skip = True
        else:
            # No data (unverified)
            # POLY_TYPE is sometimes unset in image analysis shapefiles, 
            #  and we assume that represents 'No data' here
            new_pnt = '123'
            for field_t in add_fields:
                cur_feat.SetField(field_t[0], '')
            skip = True
            
        cur_feat.SetField("PNT_TYPE", new_pnt)
        
        # If the feature is a special case from Appendix 3 & 4, we will
        #  not manually convert the sigrid values to manice code.
        if skip:
            out_layer.SetFeature(cur_feat)
            continue
        
        ## Set E_* fields
        # Use conversion tables from sigrid_to_manice
        for c_tuple in copied_climate_fields:
            copied_val = cur_feat.GetField(c_tuple[1])
            try:
                conv_val = conv_table[c_tuple[2]][copied_val]
            except:
                print("Could not convert {} to {} using table {}".format(
                    c_tuple[1], c_tuple[0], c_tuple[2]))
                raise
            cur_feat.SetField(c_tuple[0], conv_val)
            
        # E_CD
        new_val = 0.0
        copied_val = cur_feat.GetField('E_SD')
        if copied_val:
            temp = cur_feat.GetField('E_CT')
            if temp:
                if temp == '9+':
                    new_val = 9.7
                else:
                    new_val = float(temp)
                for name in ['E_CA', 'E_CB', 'E_CC']:
                    temp = cur_feat.GetField(name)
                    if temp:
                        if temp == '9+':
                            temp = 9.7
                        new_val -= float(temp)
                new_val = ceil(new_val)
            cur_feat.SetField('E_CD', str(new_val))
        
        ## Set N_* fields
        # N_CT
        new_val = cur_feat.GetField('E_CT')
        if new_val == '9+':
            new_val = '9.7'
        else:
            temp = cur_feat.GetField('CT')
            if temp:
                if temp == '98':
                    new_val = '0.0'
                elif temp == '55':
                    new_val = '0.0'
                elif temp == '02':
                    new_val = '0.2'
                elif temp == '01':
                    new_val = '0.3'
                else:
                    new_val = new_val + '.0'
        if new_val == '':
            # Undefined ice, so we will skip this
            out_layer.SetFeature(cur_feat)
            continue
        
        cur_feat.SetField('N_CT', new_val)
        
        # N_COI, N_CFY, N_CYI, N_CN (sea ice only)
        # (Fields whose values are totaled from multiple ice types)
        if is_sea:
            totaled_N_fields = [('N_COI', ['7.', '8.', '9.']),
                                ('N_CFY', ['6', '7', '1.', '4.']),
                                ('N_CYI', ['5', '4', '3']),
                                ('N_CN', ['1', '2'])]
        else:
            totaled_N_fields = []
            
        for t in totaled_N_fields:
            new_val = 0.0
            for field in stage_cct_pairs:
                if cur_feat.GetField(field[0]) in t[1]:
                    # We'll use the un-converted sigrid values here 
                    #  for a more descriptive concentration
                    
                    temp = cur_feat.GetField(field[1])
                    if temp != '':
                        if temp == '9+':
                            new_val += 9.7
                        elif temp != 'unknown':
                            new_val += float(temp)
                    elif field[1] == 'E_CA': 
                        # Special case where 'E_CA' is left empty
                        temp = cur_feat.GetField('E_CT')
                        if temp:
                            if temp == '9+':
                                new_val += 9.7
                            elif temp != 'unknown':
                                new_val += float(temp)
                                
            # Check E_SO (Stage of ice with cct < 1/10 (0.3))
            if cur_feat.GetField("E_SO") in t[1]:
                new_val += 0.3

            # Ensure that new_val is <= 10.0 for N_COI, N_CFY, N_CYI, N_CN
            if new_val > 10.0:
                new_val = 10.0
                
            # If E_CT is 9+ and N_COI is 10.0, adjust N_COI down to 9.7
            temp = cur_feat.GetField('E_CT')
            if temp == '9+' and new_val == 10.0:
                new_val = 9.7
            cur_feat.SetField(t[0], str(new_val))
            
        # Fields containing values that are copied
        if is_sea:
            # CONFIRM: icebergs are Ice of Land Origin?
            # CONFIRM: not added together?
            copy_N_fields = [('N_CMY', '9.'), ('N_CSY', '8.'),
                             ('N_CFY_TK', '4.'), ('N_CFY_M', '1.'), 
                             ('N_CFY_TN', '7'), ('N_CGW', '5'),
                             ('N_CG', '4'), ('N_CB', 'L')]
        else:
            copy_N_fields = [('N_CVTK', '1.'), ('N_CTK', '7'),
                             ('N_CM', '5'), ('N_CTN', '4'),
                             ('N_CN', '1')]
                            
        for t in copy_N_fields:
            new_val = ''
            for field in stage_cct_pairs:
                stage = cur_feat.GetField(field[0])
                if stage == t[1]:
                    temp = cur_feat.GetField(field[1])
                    if temp:
                        if temp == '9+':
                            new_val = 9.7
                        elif temp != 'unknown':
                            new_val = float(temp)
                    elif field[1] == 'E_CA':
                        temp = cur_feat.GetField('E_CT')
                        if temp:
                            if temp == '9+':
                                new_val = 9.7
                            elif temp != 'unknown':
                                new_val = float(temp)
                if not is_sea: # For lake ice
                    temp = cur_feat.GetField('E_CT')
                    if temp and temp == '9+' and new_val == 10.0:
                        new_val = 9.7
                        
            # Check E_SO (Stage of ice with cct < 1/10 (0.3))
            if cur_feat.GetField("E_SO") == t[1]:
                new_val = 0.3
                
            cur_feat.SetField(t[0], str(new_val))
        
        # TODO: Verify that these fields are to be left empty
        # (Use CF)
        # E_SE
        # E_FD
        # E_FE
        # E_CS
        
        # Save changes
        out_layer.SetFeature(cur_feat)

    # create metadata
    if input_prd_id.startswith("SGRDR"):
        try:
            spref = out_layer.GetSpatialRef()
            prj = spref.GetAttrValue('PROJECTION')
        except Exception as e:
            prj = 'Lambert_Conformal_Conic'

        create_metadata(out_shp_path, prj)

    out_layer = None
    out_ds = None
    
    print("Input successfully converted to {}".format(out_shp_path))
    return 0

# file_name convention: {ORGANIZATION_REGION_DATE_FT_TYPE_VERSION}
def create_metadata(out_shp_path, prj):
    """ Creates the metadata for SIGRID V3 (2014) """
    with open(CONFIG) as f:
        config = json.load(f)

    LCC = os.path.join(ROOT, *config['lcc_metadata'])
    PS = os.path.join(ROOT, *config['ps_metadata'])
    
    dirname, basename = os.path.split(out_shp_path)
    fn,_ = os.path.splitext(basename)
    org, region, date_str, ft_type, ver = fn.split('_')

    data = {
        'EA': {'region': 'East Arctic',
                'westbc': -91.171,
                'eastbc': -112.675,
                'northbc': 62.641,
                'southbc': 78.333},

        'EC': {'region': 'East Coast',
                'westbc': -70.387,
                'eastbc': -74.914,
                'northbc': 41.509,
                'southbc': 55.698},

        'GL': {'region': 'Great Lakes',
                'westbc': -92.767,
                'eastbc': -95.584,
                'northbc': 39.023,
                'southbc': 50.098},

        'HB': {'region': 'Hudson Bay',
                'westbc': -85.462,
                'eastbc': -99.237,
                'northbc': 53.765,
                'southbc': 68.243},

        'WA': {'region': 'West Arctic',
                'westbc': -138.02,
                'eastbc': -164.024,
                'northbc': 66.349,
                'southbc': 80.396}
    }
    template = LCC if 'Lambert_Conformal_Conic' in prj else PS
    info = data.get(region)

    if info is None:
        return
    
    print("Creating metadata")
    with codecs.open(template, 'r', 'utf-8') as xml_file:
        xml = ElementTree.parse(xml_file)

        xml.find(".//idinfo/citation/citeinfo/pubdate").text = u'{0}'.format(date_str)
        xml.find(".//idinfo/citation/citeinfo/title").text = fn
        xml.find(".//idinfo/timeperd/timeinfo/sngdate/caldate").text = u'{0}'.format(date_str)
        xml.find(".//idinfo/timeperd/timeinfo/sngdate/time").text =  u'{0}'.format('00:00:00 UTC')
        xml.find(".//idinfo/spdom/bounding/westbc").text = u'{0}'.format(info['westbc'])
        xml.find(".//idinfo/spdom/bounding/eastbc").text = u'{0}'.format(info['eastbc'])
        xml.find(".//idinfo/spdom/bounding/northbc").text = u'{0}'.format(info['northbc'])
        xml.find(".//idinfo/spdom/bounding/southbc").text = u'{0}'.format(info['southbc'])
        xml.find(".//idinfo/keywords/place//placekey[2]").text = u'{0}'.format(info['region'])
    
        metadata = os.path.join(dirname, fn + '.xml')
        xml.write(metadata, encoding='utf-8', xml_declaration=True)
    
def delete_files(file_names, folder):
    """ Attempts to delete all files under `folder` with names
    in `file_names` before deleting `folder`, if empty
    """
    if folder is None:
        return
    for item in file_names:
        try:
            os.remove(os.path.join(folder, item))
        except:
            pass
    os.rmdir(folder)
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(USAGE)
        exit(1)
    
    print("Converting {} to {}".format(sys.argv[1], sys.argv[2]))

    extracted_files = []
    in_folder = None
    shp_list = []
    if os.path.isdir(sys.argv[1]):
        # Run the main function on the first .shp file found in the folder
        for item in os.listdir(sys.argv[1]):
            if item.endswith(".shp"):
                status = main(os.path.join(sys.argv[1], item), sys.argv[2])
                break
    else:
        if sys.argv[1].endswith(".shp"):
            status = main(sys.argv[1], sys.argv[2])
        elif sys.argv[1].endswith(".zip"):
            import zipfile
            try:
                # Extract the zip to a temp folder `in_folder`
                in_folder = os.path.splitext(
                        os.path.normpath(sys.argv[1]))[0] + "_zip_tmp"
                if not os.path.isdir(in_folder):
                    os.mkdir(in_folder)
                # Open tar and extract
                with zipfile.ZipFile(sys.argv[1], 'r') as myzip:
                    extracted_files = myzip.namelist()
                    myzip.extractall(path=in_folder)
            except:
                delete_files(extracted_files, in_folder)
                raise
        elif sys.argv[1].endswith('.tar'):
            import tarfile
            try:
                # Extract the tar to a temp folder `in_folder`
                in_folder = os.path.splitext(
                        os.path.normpath(sys.argv[1]))[0] +  "_tar_tmp"
                if not os.path.isdir(in_folder):
                    os.mkdir(in_folder)
                # Open tar and extract
                with tarfile.TarFile(sys.argv[1], 'r') as mytar:
                    extracted_files = mytar.getnames()
                    if '.' in extracted_files:
                        extracted_files.remove('.')
                    mytar.extractall(path=in_folder)
            except:
                delete_files(extracted_files, in_folder)
                raise
        else:
            print("Unrecognized input type")
            status = 1
        # Run the main function on the first extracted .shp file found
        for item in extracted_files:
            if item.endswith(".shp"):
                status = main(os.path.join(in_folder, item), sys.argv[2])
                break
                
    if extracted_files: # if files were extracted
        delete_files(extracted_files, in_folder)
    
    exit(status)