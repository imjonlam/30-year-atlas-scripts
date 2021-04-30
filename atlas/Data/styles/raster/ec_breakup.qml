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
        <paletteEntry label="319" value="319" alpha="255" color="#f2f1a2"/>
        <paletteEntry label="402" value="402" alpha="255" color="#fcfa58"/>
        <paletteEntry label="416" value="416" alpha="255" color="#ffff00"/>
        <paletteEntry label="430" value="430" alpha="255" color="#ff1c00"/>
        <paletteEntry label="514" value="514" alpha="255" color="#f7058a"/>
        <paletteEntry label="528" value="528" alpha="255" color="#ce07ed"/>
        <paletteEntry label="611" value="611" alpha="255" color="#6f19d1"/>
        <paletteEntry label="625" value="625" alpha="255" color="#071d71"/>
        <paletteEntry label="900" value="900" alpha="255" color="#d3b58d"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation saturation="0" colorizeRed="255" colorizeGreen="128" colorizeStrength="100" colorizeOn="0" grayscaleMode="0" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
