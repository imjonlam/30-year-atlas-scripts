<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" maxScale="0" minScale="1e+08" version="3.12.3-București" hasScaleBasedVisibilityFlag="0">
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
    <rasterrenderer opacity="1" type="paletted" alphaBand="-1" nodataColor="" band="1">
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
        <paletteEntry label="0 %" alpha="255" value="0" color="#96c8ff"/>
        <paletteEntry label="1 - 4 %" alpha="255" value="1" color="#fffbaa"/>
        <paletteEntry label="4 - 16 %" alpha="255" value="2" color="#fff200"/>
        <paletteEntry label="16 - 34 %" alpha="255" value="3" color="#ffc800"/>
        <paletteEntry label="34 - 51 %" alpha="255" value="4" color="#ff7d03"/>
        <paletteEntry label="51 - 67 %" alpha="255" value="5" color="#ff0070"/>
        <paletteEntry label="67 - 85 %" alpha="255" value="6" color="#cc00b8"/>
        <paletteEntry label="85 - 100 %" alpha="255" value="7" color="#0000ff"/>
        <paletteEntry label="100 %" alpha="255" value="8" color="#4b4b4b"/>
        <paletteEntry label="Land" alpha="255" value="9" color="#d3b58d"/>
        <paletteEntry label="No Data" alpha="255" value="10" color="#ffffff"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation saturation="0" grayscaleMode="0" colorizeOn="0" colorizeRed="255" colorizeBlue="128" colorizeGreen="128" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
