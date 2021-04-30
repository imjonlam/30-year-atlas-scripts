<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.18.2-Zürich" maxScale="0" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal fetchMode="0" enabled="0" mode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour" enabled="false"/>
    </provider>
    <rasterrenderer type="paletted" band="1" alphaBand="-1" opacity="1" nodataColor="">
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
        <paletteEntry color="#96c8ff" value="0" alpha="255" label="0"/>
        <paletteEntry color="#f0d2fa" value="1" alpha="255" label="1"/>
        <paletteEntry color="#873cd7" value="4" alpha="255" label="4"/>
        <paletteEntry color="#dc50d7" value="5" alpha="255" label="5"/>
        <paletteEntry color="#ffff00" value="6" alpha="255" label="6"/>
        <paletteEntry color="#9bd200" value="7" alpha="255" label="7"/>
        <paletteEntry color="#00c814" value="10" alpha="255" label="10"/>
        <paletteEntry color="#007800" value="11" alpha="255" label="11"/>
        <paletteEntry color="#b46432" value="12" alpha="255" label="12"/>
        <paletteEntry color="#ffffff" value="123" alpha="0" label="123"/>
        <paletteEntry color="#d3b58d" value="900" alpha="255" label="900"/>
      </colorPalette>
      <colorramp name="[source]" type="randomcolors">
        <Option/>
      </colorramp>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
    <huesaturation colorizeStrength="100" saturation="0" colorizeOn="0" grayscaleMode="0" colorizeRed="255" colorizeGreen="128" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
