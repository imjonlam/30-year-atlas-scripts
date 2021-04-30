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
        <paletteEntry label="123" value="123" alpha="0" color="#ffffff"/>
        <paletteEntry label="900" value="900" alpha="255" color="#d3b58d"/>
        <paletteEntry label="910" value="910" alpha="255" color="#4c0073"/>
        <paletteEntry label="924" value="924" alpha="255" color="#002673"/>
        <paletteEntry label="1008" value="1008" alpha="255" color="#004da8"/>
        <paletteEntry label="1022" value="1022" alpha="255" color="#005ce6"/>
        <paletteEntry label="1105" value="1105" alpha="255" color="#3679e3"/>
        <paletteEntry label="1119" value="1119" alpha="255" color="#5c9ce3"/>
        <paletteEntry label="1204" value="1204" alpha="255" color="#bee8ff"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation saturation="0" colorizeRed="255" colorizeGreen="128" colorizeStrength="100" colorizeOn="0" grayscaleMode="0" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
