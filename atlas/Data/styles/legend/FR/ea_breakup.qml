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
        <paletteEntry label="Pas de glace - 04 Juin" alpha="255" value="0" color="#96c8ff"/>
        <paletteEntry label="04 Juin" alpha="255" value="604" color="#f2f1a2"/>
        <paletteEntry label="18 Juin" alpha="255" value="618" color="#ffff00"/>
        <paletteEntry label="02 Juil" alpha="255" value="702" color="#faaa00"/>
        <paletteEntry label="16 Juil" alpha="255" value="716" color="#ff1c00"/>
        <paletteEntry label="30 Juil" alpha="255" value="730" color="#f7058a"/>
        <paletteEntry label="13 Août" alpha="255" value="813" color="#ce07ed"/>
        <paletteEntry label="27 Août" alpha="255" value="827" color="#6f19d1"/>
        <paletteEntry label="Étendue minimale de glace - 10 Sep" alpha="255" value="910" color="#071d71"/>
        <paletteEntry label="Terre" alpha="255" value="900" color="#d3b58d"/>
        <paletteEntry label="Aucunes données" alpha="0" value="123" color="#ffffff"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeRed="255" colorizeBlue="128" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" saturation="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
