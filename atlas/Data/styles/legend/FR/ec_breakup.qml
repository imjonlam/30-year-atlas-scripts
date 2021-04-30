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
        <paletteEntry label="Pas de glace - 19 Mars" alpha="255" value="0" color="#96c8ff"/>
        <paletteEntry label="19 Mars" alpha="255" value="319" color="#f2f1a2"/>
        <paletteEntry label="02 Avr" alpha="255" value="402" color="#fcfa58"/>
        <paletteEntry label="16 Avr" alpha="255" value="416" color="#ffff00"/>
        <paletteEntry label="30 Avr" alpha="255" value="430" color="#ff1c00"/>
        <paletteEntry label="14 Mai" alpha="255" value="514" color="#f7058a"/>
        <paletteEntry label="28 Mai" alpha="255" value="528" color="#ce07ed"/>
        <paletteEntry label="11 Juin" alpha="255" value="611" color="#6f19d1"/>
        <paletteEntry label="25 Juin" alpha="255" value="625" color="#071d71"/>
        <paletteEntry label="Terre" alpha="255" value="900" color="#d3b58d"/>
        <paletteEntry label="Aucunes Données" alpha="255" value="123" color="#ffffff"/>
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation colorizeRed="255" colorizeBlue="128" colorizeStrength="100" grayscaleMode="0" colorizeOn="0" saturation="0" colorizeGreen="128"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
