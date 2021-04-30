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
        <paletteEntry label="04 Déc" alpha="255" value="1204" color="#1727a3"/>
        <paletteEntry label="18 Déc" alpha="255" value="1218" color="#173eb5"/>
        <paletteEntry label="01 Jan" alpha="255" value="101" color="#2259c7"/>
        <paletteEntry label="15 Jan" alpha="255" value="115" color="#2176d9"/>
        <paletteEntry label="29 Jan" alpha="255" value="129" color="#368de3"/>
        <paletteEntry label="12 Fév" alpha="255" value="212" color="#5c9ce3"/>
        <paletteEntry label="26 Fév" alpha="255" value="226" color="#91bee9"/>
        <paletteEntry label="12 Mars" alpha="255" value="312" color="#b4dcff"/>
        <paletteEntry label="Pas de glace - 12 Mars" alpha="255" value="0" color="#96c8ff"/>
        <paletteEntry label="Terre" alpha="255" value="900" color="#d3b58d"/>
        <paletteEntry label="Aucunes données" alpha="255" value="123" color="#ffffff"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeRed="255" colorizeBlue="128" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" saturation="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
