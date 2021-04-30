<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.12.3-București" hasScaleBasedVisibilityFlag="0" maxScale="0" minScale="1e+08" styleCategories="AllStyleCategories">
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
    <rasterrenderer type="paletted" band="1" nodataColor="" alphaBand="-1" opacity="1">
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
        <paletteEntry value="924" color="#4c0073" alpha="255" label="24 Sep ou avant"/>
        <paletteEntry value="1008" color="#002673" alpha="255" label="08 Oct"/>
        <paletteEntry value="1022" color="#004da8" alpha="255" label="22 Oct"/>
        <paletteEntry value="1105" color="#005ce6" alpha="255" label="05 Nov"/>
        <paletteEntry value="1119" color="#3679e3" alpha="255" label="19 Nov"/>
        <paletteEntry value="1204" color="#5c9ce3" alpha="255" label="04 Déc"/>
        <paletteEntry value="101" color="#78aeb9" alpha="255" label="01 Jan"/>
        <paletteEntry value="201" color="#93c090" alpha="255" label="01 Fév"/>
        <paletteEntry value="301" color="#ffff00" alpha="255" label="01 Mars"/>
        <paletteEntry value="0" color="#ededed" alpha="255" label="Pas de banquise côtière - 01 Mars"/>
        <paletteEntry value="900" color="#d3b58d" alpha="255" label="Terre"/>
        <paletteEntry value="123" color="#ffffff" alpha="0" label="Aucunes données"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors"/>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0"/>
    <huesaturation grayscaleMode="0" colorizeOn="0" colorizeStrength="100" colorizeBlue="128" saturation="0" colorizeGreen="128" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
