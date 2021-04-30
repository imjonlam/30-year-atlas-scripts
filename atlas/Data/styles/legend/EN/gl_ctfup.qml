<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+08" version="3.13.0-Master" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0">
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
    <rasterrenderer band="1" opacity="1" nodataColor="" type="paletted" alphaBand="-1">
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
        <paletteEntry label="Dec 18" alpha="255" value="1218" color="#090991"/>
        <paletteEntry label="Jan 01" alpha="255" value="101" color="#192ca8"/>
        <paletteEntry label="Jan 15" alpha="255" value="115" color="#204cbd"/>
        <paletteEntry label="Jan 29" alpha="255" value="129" color="#2072d6"/>
        <paletteEntry label="Feb 12" alpha="255" value="212" color="#3d90e3"/>
        <paletteEntry label="Feb 26" alpha="255" value="226" color="#6baee8"/>
        <paletteEntry label="No Ice - Feb 26" alpha="255" value="0" color="#96c8ff"/>
        <paletteEntry label="Land" alpha="255" value="900" color="#d3b58d"/>
        <paletteEntry label="No Data" alpha="255" value="123" color="#ffffff"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeRed="255" colorizeBlue="128" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" saturation="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
