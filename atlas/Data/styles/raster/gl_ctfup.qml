<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.12.3-București" hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <rasterrenderer nodataColor="" type="paletted" opacity="1" alphaBand="-1" band="1">
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
        <paletteEntry label="0" value="0" alpha="255" color="#96c8ff"/>
        <paletteEntry label="101" value="101" alpha="255" color="#192ca8"/>
        <paletteEntry label="115" value="115" alpha="255" color="#204cbd"/>
        <paletteEntry label="123" value="123" alpha="0" color="#ffffff"/>
        <paletteEntry label="129" value="129" alpha="255" color="#2072d6"/>
        <paletteEntry label="212" value="212" alpha="255" color="#3d90e3"/>
        <paletteEntry label="226" value="226" alpha="255" color="#6baee8"/>
        <paletteEntry label="900" value="900" alpha="255" color="#d3b58d"/>
        <paletteEntry label="1218" value="1218" alpha="255" color="#090991"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation saturation="0" colorizeRed="255" colorizeGreen="128" colorizeStrength="100" colorizeOn="0" grayscaleMode="0" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
