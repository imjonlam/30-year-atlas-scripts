# Atlas Climate Chart

## 1. Running the Atlas Script

**Requirements**
1. Python 3.6+
2. QGIS Python Bindings

**Purpose**
* This script is used to create Atlas Charts as .png from existing Climate shapefiles or GEOTIFFS.

**Overview**
* [atlas.py](../atlas.py): produces an Atlas Chart specified by a provided configuration file (.json)

**Internal Configuration File modification**
* Depending on where these scripts are to be run the following lines in [config.json](../Common/config.json) will require modification:
  * `"logdir": [ "c:\\", "cis", "user_data", "{0}", "logs" ]`
  * `"tmpdir": ["c:\\", "cis", "user_data", "{0}", "temp"]`
  * where `"{0}"` is the account's username

**How to run on Windows?**
1. Download and Install QGIS (https://qgis.org/downloads/QGIS-OSGeo4W-3.18.2-1.msi)
2. Add to your PATH: `C:\Program Files\QGIS 3.18\bin`
3. Run  script from terminal:
     * `python-qgis atlas.py config.json` 

**How to run on Nanuk?**
* An environment has been set up by Benjamin on: `G:\Projects\2020_Climate_Atlas\Custom_Environment`
* Per Benjamin, some modifications are required:
```
The only modifications needed to the scripts were to add the following to: atlas.py and helper.py, after the other imports, to setup the proper environment. It’s possible that a few of those lines can be safely removed…

import sys
sys.path.append(r"C:\COTS\QGIS 3.16\apps\qgis-ltr\bin")
sys.path.append(r"C:\COTS\QGIS 3.16\apps\qgis-ltr\python")
sys.path.append(r"C:\COTS\QGIS 3.16\apps\qgis-ltr\python\qgis")
sys.path.append(r"C:\COTS\QGIS 3.16\apps\Python37\Lib\site-packages")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r"C:\COTS\QGIS 3.16\apps\qt5\plugins\platforms"
os.environ['PROJ_LIB'] = r"C:\COTS\QGIS 3.16\share\proj"
os.environ['GDAL_DATA'] = r"C:\COTS\QGIS 3.16\share\gdal"

and to move the ogseo imports (gdal, ogr, osr) to after the other imports.

You can see my modified scripts and config files here, though please don’t edit them in-place:
G:\Working\deschampsb\atlas_test\scripts
G:\Working\deschampsb\logs

Benjamin
```


**Example Configuration File**
* [sample.json](../Inputs/sample.json)
* *Explaination*:
  > I want to create `icfrq` **atlas** charts for the regions `EA` and `WA` for the historic dates `0101` and `0129`. These input charts are located in their respective directories and were made with a threshold of `1` from `1991 - 2020`.  
  Since `is_atlas` is `true`, if I want to make `EA` atlas charts, I need to include directory paths for both `EA` and `HB`.  
  Similarily for `WA`, I need to provide directory paths for both `WA` and `EA`.

**Available Chart Inputs**
* Depending on the input filetypes, the following products can be made:
* **Raster (.tif)**
  * ctmed, cpmed, oimed, prmed, icfrq, oifrq, ctfup, breakup
* **Vector (.shp)**
  * ctmed, cpmed, oimed, prmed, icfrq, fifrq, oifrq, ctfup, breakup, fifup, airss, mpi
* **Note:** these chart names are **very important**, they are used to get all required resources to produce their respective charts
  * For **vectors**, each stylesheet in `/Data/styles/vector/` has a specific field that is required to be present within the shapefile:
    * I.e.: `<renderer-v2 forceraster="0" symbollevels="0" type="categorizedSymbol" attr="ctmed" enableorderby="0">`
    * This becomes very important when dealing with charts that have multiple thresholds
      * I.e.: if `chart: oifrq, threshold: 1` target stylesheet is `Data\styles\vector\o1frq.qml` with `attr=oifrq`
      * I.e.: if `chart: oifrq, threshold: 4` target stylesheet is `Data\styles\vector\o4frq.qml` with `attr=o4frq`
  * Refer to [config.json](../Common/config.json) for mapping

**Configuration File Explaination**
* `outdir`: the output directory location
* `is_atlas`: boolean signifying if output is an Atlas Chart or a Climate Tool chart
  * If `true` the following will be displayed:
    * An analogues label will be displayed within the chart
    * If region is EC or GL, the years displayed will be `{start-1}/{start} - {end-1}/{end}` to accomodate for missing data (subject to change)
* `data`:
  * Each path in this dictionary is a directory containing valid shapefiles or GEOTIFFs in the following structure:
    * /`Directory`/
      * /`ea_ctmed0101`/
        * `ea_ctmed0101.tif`
      * or 
      * /`ea_ctmed0101`/
        * `ea_ctmed0101.shp`
        * `ea_ctmed0101.dbf`
        * `ea_ctmed0101.prj`
        * ...
  * if the `is_atlas` key is `false` you will only need to include the key for the specific region you are generating for
    * For example, if you would like to create a EA chart and `is_atlas` is `false`, the `data` key would be as follows:
      * ``` 
        "data": {
              "EA": "A/Path/To/EA/Directory",
        }
        ```
    * If `is_atlas` is `true`, then you would need to include for regional overlaps:
      * ``` 
        "data": {
              "EA": "A/Path/To/EA/Directory",
              "HB": "A/Path/To/HB/Directory",
        }
        ```
  * **Regional overlaps (if is_atlas is true)**:
    * `AR`: EA, HB, WA
    * `EA`: EA, HB
    * `WA`: EA, WA
    * `HB`: EA, HB
    * `EC`: EC
    * `GL`: GL
  * **NOTE: If the `AR` key is supplied, it does not require datapaths to `EA, HB, WA`** *(i.e.: you have `ar_ctmed0101.tif` files)*
* `chart`: the chart you are creating for *(refer to **Available Chart Inputs**)*
  * *Note: You can only have one chart per configuration file*
* `years`: the years of data this chart is corresponding to
* `regions`: a list of regions to produce charts for
  * **Valid regions:** AR, EA, WA, HB, EC, GL
* `historic dates`: the historic dates to create products for
* `threshold`: the threshold value associated with the specific chart
  * **Valid thresholds currently supported per chart:**
    * **oifrq**: 1, 4, 7
  * **Currently FIXED thresholds**:
    * **icfrq**: 1
    * **ctfup**: 1
    * **breakup**: 1
* `log_to_gitlab`:
  * If this key is provided, logging will be posted to GitLab if an error occurs during runtime
  * *Note: you must have the required CIS installations present*

**Output Image (.png)**
* The output follows the following file naming convention:
  * **ctmed**: `{region}_ctmed{date}.png`, 
  * **cpmed**: `{region}_cpmed{date}.png`,
  * **oimed**: `{region}_oimed{date}.png`,
  * **prmed**: `{region}_prmed{date}.png`,
  * **icfrq**: `{region}_icfrq{date}.png`,
  * **oifrq**: `{region}_o{threshold}frq{date}.png`, *if threshold=1, replaced with i*
  * **breakup**: `{region}_breakup_2_week.png`,
  * **ctfup**: `{region}_freezeup_2_week.png`,
  * **fifrq**: `{region}_fifrq{date}.png`,
  * **fifup**: `{region}_fifreezeup_2_week.png`,
  * **airss**: `{region}_medairss{date}.png`,
  * **mpi**: `{region}_mpi{date}.png`
  
<br />
<hr>
<br />

## 2. Creating a New Product (or Template)
* Read: [How to create a new template](./howto_create_template.pdf)  

<br />
<hr>
<br />

## 3. Modifying an Existing template
* Read: [How to modify an existing template](./howto_modify_template.pdf)

<br />
<hr>
<br />

## 4. Future Enhancements:
1) Currently if there are missing required files, a warning will be logged and the script continues to generate the next chart.
   * However, if an unexpected exception happens, the script will completely exit.
   * Enhancement: should catch error and continue onto generating next chart
2) Allow for dynamic thresholds. For example, you could create oifrq for any threshold from 1-10.
   * **Note:** This means that for vector inputs, we will need to create 10 stylesheets (where threshold is a value from 1-10) as each threshold requires a unique column in the shapefile

   * To *enable* dynamic thresholds:
     * Remove lines 140 - 142 in [AtlasChart.py](../AtlasChart.py)
     * Modify [config.json](../Common/config.json) `filenames` key similar to `oifrq`
     * Modify AtlasHandler.__filename()
     * Modify line 300 in [AtlasChart.py](../AtlasChart.py) if threshold is required in the chart title
     * If product is for vector inputs:
       * Modify [config.json](../Common/config.json) `vector_style` key similar to `oifrq`
       * Clone target stylesheet and modify the column name, for example:  
    
          ```
          <renderer-v2 forceraster="0" symbollevels="0" type="categorizedSymbol" 
          attr="o9frq" enableorderby="0">
          ```
          *This means that the input shapefiles will need a column named o9frq*
 3) Remove lines 300 - 319 in [AtlasChart.py](../AtlasChart.py) if necessary. This is currently used for atlas charts (`is_atlas` is `true`) since some climate shapefiles are missing in 1991-2020 and use 1990-2019 instead for EC and GL.
