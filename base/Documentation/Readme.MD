# Base Climate Charts

## 1. Running the Base Climate Script

**Requirements**
1. Python 3.6+
2. QGIS Python Bindings

**Purpose**
* This collection of script is used to create Base Climate Charts as GeoTIFF (.tif) from existing Climate shapefiles
* These scripts are based off of Steve's 1981-2010 Avenue Code *(Steve_2010_Atlas_Final_Avenue_Code*)
  * *Note that there are minor deviations that were made during this decade's updates*

**Overview**
* [median_ct.py](../median_ct.py): produces median concentration related charts (ctmed, oimed, cpmed)
* [median_predom.py](../median_predom.py): produces median predominant of ice charts (prmed)
* [frequency.py](../frequency.py): produces frequency of ice related chart (icfrq, oifrq, o4frq)
* [ctfup.py](../ctfup.py): produces freeze-up dates chart (ctfup) *(only for regions: AR, EC, GL)*
* [breakup.py](../breakup.py): produces break-up dates chart (breakup) *(only for regions: AR, EC, GL)*

**Internal Configuration File modification**
* Depending on where these scripts are to be run the following lines in [config.json](../Common/config.json) will require modification:
  * `"logdir": [ "c:\\", "cis", "user_data", "{0}", "logs" ]`
  * `"tmpdir": ["c:\\", "cis", "user_data", "{0}", "temp"]`
  * where `"{0}"` is the account's username

**How to run on Nanuk?**
* An environment has been set up by Benjamin on: `G:\Projects\2020_Climate_Atlas\Custom_Environment`
* Follow step #3 below

**How to run on Windows?**
1. Download and Install QGIS (https://qgis.org/downloads/QGIS-OSGeo4W-3.18.2-1.msi)
2. Add to your PATH: `C:\Program Files\QGIS 3.18\bin`
3. Run  script from terminal:
     * **median_ct**: `python-qgis median_ct.py config.json` 
     * **frequency**: `python-qgis frequency config.json` 
     * **median_predom**: `python-qgis median_predom.py config.json` 
     * **ctfup**: `python-qgis ctfup.py config.json` 
     * **breakup**: `python-qgis breakup.py config.json` 
  
**Example Configuration File**
* [sample.json](../Inputs/sample.json)
* *Explaination*:
  > I want to create `icfrq` **atlas** base charts for the regions `EA` and `WA` for the historic dates `0101` and `0129`. These input shapefiles are located in their respective directories and were made with a threshold of `1` from `1991 - 2020`.  
  Since `is_atlas` is `true`, if I want to make `EA` atlas charts, I need to include directory paths for both `EA` and `HB`.  
  Similarily for `WA`, I need to provide directory paths for both `WA` and `EA`.

* [breakup_sample.json](../Inputs/breakup_sample.json)
  > I want to create `breakup` **atlas** base charts for the regions `AR`. Since `ctmeds_supplied` is `false`, I need to regenerate all required `ctmed` tifs first (`is_atlas` automaticaly `true`).  
  These input shapefiles are located in their respective directories and were made with a threshold of `1` from `1991 - 2020`.  
  Since the region is `AR` I need to include directory paths for `EA`, `HB` and `WA`

**Available Chart Inputs**
  * Depending on which script is run the following products can be made:
  * **median_ct**: ctmed, oimed, cpmed
  * **frequency**: icfrq, oifrq
  * **median_predom**: prmed
  * **ctfup**: ctfup
  * **breakup**: breakup 

**Configuration File Explaination**
* `outdir`: the output directory location
* `is_atlas`: boolean signifying if output is an Atlas Chart or a Climate Tool Chart
  * In such a case, overlaps will also be generated (i.e.: Overlaps between EA and HB)
* `data`:
  * Each path in this dictionary is a directory containing valid archived shapefiles in the following format:
    * I.E.: `CIS_EA_19900129_pl_a.tar`
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
* `chart`: the chart you are creating for *(refer to **Available Chart Inputs**)*
  * *Note: You can only have one chart per configuration file*
* `years`: the years of data this chart is corresponding to
* `regions`: a list of regions to produce charts for
  * **Valid regions:** AR, EA, WA, HB, EC, GL
* `historic dates`: the historic dates to create products for
* `threshold` [1-10]: the threshold value associated with the specific chart
  * **Valid thresholds currently supported per chart:**
    * **oifrq**: 1, 4, 7
  * **Currently FIXED thresholds**:
    * **icfrq**: 1
    * **ctfup**: 1
    * **breakup**: 1
* `log_to_gitlab`:
  * If this key is provided, logging will be posted to GitLab if an error occurs during runtime
  * *Note: you must have the required CIS installations present*
* `ctmeds_supplied`: boolean signifying that the path given by the key `data[REGION]` is a directory containing valid median concentration (ctmed) GEOTIFFS.
  * **For Freezeup/Breakup (ctfup, breakup) charts only**  
  * If `false`, will generate `ctmed` tifs before making `breakup/ctfup` tifs

**Output GEOTIFF (.tif)**
* The output follows the following file naming convention:
  * **ctmed**: `{region}_ctmed{date}.tif`, 
  * **cpmed**: `{region}_cpmed{date}.tif`,
  * **oimed**: `{region}_oimed{date}.tif`,
  * **prmed**: `{region}_prmed{date}.tif`,
  * **icfrq**: `{region}_icfrq{date}.tif`,
  * **oifrq**: `{region}_o{threshold}frq{date}.tif`, *if threshold=1, replaced with i*
  * **breakup**: `{region}_breakup_2_week.tif`,
  * **ctfup**: `{region}_freezeup_2_week.tif`,

* The output is projected to LCC100 with the following Central Meridian: -100

<br />
<hr>
<br />

## 2. Future Enhancements:
1) Currently if there are missing required files, a warning will be logged and the script continues to generate the next chart.
   * However, if an unexpected exception happens, the script will completely exit.
   * Enhancement: should catch error and continue onto generating next chart
2) Since these scripts are to be used for the climate tool, it is to be expected that following requirements be met:
   * We must expand on these scripts to include Angela's new products
   * We must compare against Angela's scripts to find and fix deviations

3) Allow for dynamic thresholds for charts other than oifrq. The code already has the flexibility to use dynamic thresholds for icfrq, oifrq, ctfup and breakup. However, output filenames configured in [config.json](../Common/config.json) will need to be modified.
   * It is currently limited only to align with the atlas scripts.
   * To *enable* dynamic thresholds:
     * Modify [config.json](../Common/config.json) `filenames` key similar to `oifrq`
     * For freezeup or breakup in [SpecialChart.py](../SpecialChart.py):
         * Modify SpecialChart.__filename()
         * Remove line 39
     * Otherwise in [BaseChart.py](../BaseChart.py):
         * Modify BaseHandler.__filename()
         * Remove lines 165 - 167