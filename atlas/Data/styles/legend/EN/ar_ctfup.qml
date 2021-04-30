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
        <paletteEntry label="Minimal Ice Extent - Sep 10" alpha="255" value="910" color="#4c0073"/>
        <paletteEntry label="Sep 24" alpha="255" value="924" color="#002673"/>
        <paletteEntry label="Oct 08" alpha="255" value="1008" color="#004da8"/>
        <paletteEntry label="Oct 22" alpha="255" value="1022" color="#005ce6"/>
        <paletteEntry label="Nov 05" alpha="255" value="1105" color="#3679e3"/>
        <paletteEntry label="Nov 19" alpha="255" value="1119" color="#5c9ce3"/>
        <paletteEntry label="Dec 04" alpha="255" value="1204" color="#bee8ff"/>
        <paletteEntry label="No Ice - Dec 04" alpha="255" value="0" color="#96c8ff"/>
        <paletteEntry label="Land" alpha="255" value="900" color="#d3b58d"/>
        <paletteEntry label="No Data" alpha="0" value="123" color="#ffffff"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeRed="255" colorizeBlue="128" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" saturation="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
