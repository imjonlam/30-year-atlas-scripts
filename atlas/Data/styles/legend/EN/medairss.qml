<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="1e+08" version="3.12.3-București" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" maxScale="0">
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
    <rasterrenderer nodataColor="" alphaBand="-1" band="1" opacity="1" type="paletted">
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
        <paletteEntry color="#080808" label="CAC2-CAC1" value="0" alpha="255"/>
        <paletteEntry color="#ac0018" label="CAC3" value="1" alpha="255"/>
        <paletteEntry color="#e60f0f" label="CAC4" value="2" alpha="255"/>
        <paletteEntry color="#ff7d07" label="A" value="3" alpha="255"/>
        <paletteEntry color="#ffb400" label="B" value="4" alpha="255"/>
        <paletteEntry color="#ffff9c" label="C" value="5" alpha="255"/>
        <paletteEntry color="#ffffcd" label="D" value="6" alpha="255"/>
        <paletteEntry color="#a4acb4" label="E" value="7" alpha="255"/>
        <paletteEntry color="#ffffff" label="Other" value="8" alpha="255"/>
      </colorPalette>
      <colorramp type="randomcolors" name="[source]"/>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0"/>
    <huesaturation grayscaleMode="0" colorizeGreen="128" saturation="0" colorizeRed="255" colorizeOn="0" colorizeBlue="128" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
