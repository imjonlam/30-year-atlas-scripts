<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" maxScale="0" minScale="1e+08" version="3.12.3-București" hasScaleBasedVisibilityFlag="0">
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
    <rasterrenderer opacity="1" alphaBand="-1" nodataColor="" band="1" type="paletted">
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
        <paletteEntry value="0" label="&lt; 1 %" alpha="255" color="#96c8ff"/>
        <paletteEntry value="1" label="1 - 16 %" alpha="255" color="#fff200"/>
        <paletteEntry value="2" label="16 - 34 %" alpha="255" color="#ffc800"/>
        <paletteEntry value="3" label="34 - 51 %" alpha="255" color="#ff7d03"/>
        <paletteEntry value="4" label="51 - 67 %" alpha="255" color="#ff0070"/>
        <paletteEntry value="5" label="67 - 85 %" alpha="255" color="#cc00b8"/>
        <paletteEntry value="6" label="85 - 100 %" alpha="255" color="#0000ff"/>
        <paletteEntry value="7" label="100 %" alpha="255" color="#4b4b4b"/>
        <paletteEntry value="8" label="Land" alpha="255" color="#d3b58d"/>
        <paletteEntry value="9" label="No Data" alpha="255" color="#ffffff"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation saturation="0" colorizeRed="255" colorizeGreen="128" colorizeBlue="128" grayscaleMode="0" colorizeOn="0" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
