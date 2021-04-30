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
        <paletteEntry label="Eau libre ou libre de glace" alpha="255" value="0" color="#96c8ff"/>
        <paletteEntry label="Nouvelle glace de lac" alpha="255" value="1" color="#f0d2fa"/>
        <paletteEntry label="Glace de lac mince" alpha="255" value="2" color="#873cd7"/>
        <paletteEntry label="Glace de lac moyenne" alpha="255" value="3" color="#dc50d7"/>
        <paletteEntry label="Glace de lac épaisse" alpha="255" value="4" color="#9bd200"/>
        <paletteEntry label="Glace de lac très épaisse" alpha="255" value="5" color="#00c814"/>
        <paletteEntry label="Terre" alpha="255" value="6" color="#d3b58d"/>
        <paletteEntry label="Aucunes données" alpha="255" value="7" color="#ffffff"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeRed="255" colorizeBlue="128" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" saturation="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
