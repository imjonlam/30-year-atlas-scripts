<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" version="3.12.3-București" minScale="1e+08">
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
    <rasterrenderer alphaBand="-1" band="1" type="paletted" opacity="1" nodataColor="">
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
        <paletteEntry value="0" alpha="255" color="#ddebf5" label="8"/>
        <paletteEntry value="1" alpha="255" color="#fffe03" label="1 - 4"/>
        <paletteEntry value="2" alpha="255" color="#ffc000" label="5 - 10"/>
        <paletteEntry value="3" alpha="255" color="#e97e37" label="11 - 15"/>
        <paletteEntry value="4" alpha="255" color="#fd0200" label="16 - 20"/>
        <paletteEntry value="5" alpha="255" color="#7026a0" label="21 - 25"/>
        <paletteEntry value="6" alpha="255" color="#0071c1" label="26 - 29"/>
        <paletteEntry value="7" alpha="255" color="#757170" label="30"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation saturation="0" colorizeOn="0" grayscaleMode="0" colorizeStrength="100" colorizeGreen="128" colorizeBlue="128" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
