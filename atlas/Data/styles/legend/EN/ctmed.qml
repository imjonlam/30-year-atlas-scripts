<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" version="3.13.0-Master" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer band="1" opacity="1" type="paletted" alphaBand="-1" nodataColor="">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <colorPalette>
        <paletteEntry color="#96c8ff" label="Less than 1/10" value="0" alpha="255"/>
        <paletteEntry color="#8cffa0" label="1 - 3/10" value="1" alpha="255"/>
        <paletteEntry color="#ffff00" label="4 - 6/10" value="2" alpha="255"/>
        <paletteEntry color="#ff7d07" label="7 - 8/10" value="3" alpha="255"/>
        <paletteEntry color="#ff0000" label="9 - 9+/10" value="4" alpha="255"/>
        <paletteEntry color="#969696" label="10/10" value="5" alpha="255"/>
        <paletteEntry color="#d3b58d" label="Land" value="6" alpha="255"/>
        <paletteEntry color="#ffffff" label="No Data" value="7" alpha="255"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation grayscaleMode="0" colorizeBlue="128" colorizeStrength="100" saturation="0" colorizeOn="0" colorizeRed="255" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
