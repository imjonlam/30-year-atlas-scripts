import os
import logging
from osgeo import ogr, osr, gdal
from typing import List, Union

from Common.ErrorHandler import baseException

# pylint: disable=import-error
from qgis.core import ( 
  QgsVectorLayer,
  QgsRasterLayer,
  QgsReadWriteContext,
  QgsProject,
  QgsPrintLayout,
  QgsLayoutItem,
  QgsLayoutExporter,
  QgsLayerTree,
  QgsLegendRenderer,
  QgsLegendStyle,
  QgsMapLayerLegendUtils
)
from qgis.PyQt.QtXml import QDomDocument 

QgsLayer = Union[QgsVectorLayer,QgsRasterLayer]

# global
dirname = os.path.dirname
ROOT = dirname(dirname(os.path.realpath(__file__)))

'''''''''''''''
Generic METHODS
'''''''''''''''
def get_path(arr: List[str], formats: List[str]=[]):
  '''Returns the full root path'''
  if not isinstance(formats, list):
    formats = [formats]
  
  return os.path.join(ROOT, *arr).format(*formats)
  
'''''''''''''''
QGIS METHODS
'''''''''''''''
def open_layer(project: QgsProject, fp: str) -> QgsLayer:
  '''Opens and returns a QgsVectorLayer/QgsRasterLayer'''
  if fp is None:
    return None

  logging.info(f'opening layer: {fp}')
  basename, ext = os.path.splitext(os.path.basename(fp))
  vector = not (ext in ['.tif', '.tiff'])

  # create vector or raster layer
  if vector:
    layer = QgsVectorLayer(fp, basename)
  else:
    layer = QgsRasterLayer(fp, basename)

  if not layer.isValid():
    raise baseException(f'failed to load layer: {fp}', 
                        baseException.ERR_CFG_LEVEL)

  # add layer to project
  project.addMapLayer(layer)
  return layer

def set_map(layout: QgsPrintLayout, item_id: str, layers: List[QgsLayer]) -> QgsLayoutItem:
  '''Adds layer(s) to the map'''
  logging.info(f'setting map, id={item_id}')
  map_ = layout.itemById(item_id)

  # add layer(s) to map
  map_.setLayers(layers)
  return map_

def set_style(layer: QgsLayer, fp: str):
  '''Sets the styling of a particular layer'''
  logging.info(f'setting styles: {fp}')
  if layer is not None:
    layer.loadNamedStyle(fp)

def open_template(layout: QgsPrintLayout, fp: str):
  '''Load items from template into layout'''
  logging.info(f'opening template: {fp}')
  doc = QDomDocument()
  context = QgsReadWriteContext()

  # read template
  with open(fp, 'rt', encoding='utf-8') as f:
    content = f.read()

  # set content and load items from template
  doc.setContent(content)
  _, ok = layout.loadFromTemplate(doc, context)
  if not ok:
    raise baseException(f'failed to load QGS template: {fp}',
                        baseException.ERR_CODE_LEVEL)

def set_image(layout: QgsPrintLayout, item_id: str, fp: str):
  '''Adds references to the layout image items'''
  logging.info(f'setting image source for {item_id} using {fp}')
  item = layout.itemById(item_id)
  item.setPicturePath(fp)
 
def set_legend(layout: QgsPrintLayout, tree: QgsLayerTree, layer: QgsLayer, item_id: str):
  '''Sets the Legend items'''
  logging.info(f'setting legend: {item_id}')
  item = layout.itemById(item_id)

  # set layer as root for legend
  tree.addLayer(layer)
  model = item.model()
  model.setRootGroup(tree)
  root = model.rootGroup().findLayer(layer)
  
  # hide the node title
  QgsLegendRenderer.setNodeLegendStyle(root, QgsLegendStyle.Hidden)

  # hide the node with label: Band 1 (Gray)
  if isinstance(layer, QgsRasterLayer):
    nodes = model.layerLegendNodes(root)
    if nodes[0].data(0) == 'Band 1 (Gray)':
      indexes = list(range(1, len(nodes)))
      QgsMapLayerLegendUtils.setLegendNodeOrder(root, indexes)
      model.refreshLayerLegend(root)

def set_label(layout: QgsPrintLayout, item_id: str, text: str):
  '''Set the text for existing layout items'''
  logging.info(f'setting text with label id={item_id}')
  item = layout.itemById(item_id)

  if item is not None:
    item.setText(text)
  else:
    raise baseException(f'item_id {item_id} does not exist', 
                        baseException.ERR_CODE_LEVEL)

def format_label(layout: QgsPrintLayout, item_id: str, params: List[Union[int, str]]):
  '''Formats the text for existing layout items'''
  logging.info(f'formatting text with label id={item_id}')

  item = layout.itemById(item_id)
  text = item.text().format(*params)

  if item is not None:
    item.setText(text)
  else:
    raise baseException(f'item_id {item_id} does not exist', 
                        baseException.ERR_CODE_LEVEL)

def hide_item(layout: QgsPrintLayout, item_id: str):
  '''Hides an item by item_id from Layout'''
  logging.info(f'hiding {item_id} in layout')
  item = layout.itemById(item_id)
  item.setVisibility(False)

def export(layout: QgsPrintLayout, dest: str):
  '''Exports the layout to an image'''
  logging.info(f'exporting to {dest}')
  exporter = QgsLayoutExporter(layout)

  # export as image (.png, .jpg, etc.)
  exporter.exportToImage(dest, QgsLayoutExporter.ImageExportSettings())

'''''''''''''''
OGR METHODS
'''''''''''''''
def reproject_raster(fp: str, srs: osr.SpatialReference, out_dir: str) -> str:
  '''Reprojects a raster dataset to specified out_dir'''
  logging.info(f'reprojecting {fp}')
  ds = gdal.Open(fp)
  out = os.path.join(out_dir, os.path.basename(fp))

  # no action needed
  if ds.GetProjection() == srs:
    logging.info('no reprojection required')
    ds = None
    return fp

  opt = gdal.WarpOptions(
    dstSRS = srs
  )

  gdal.Warp(out, ds, options=opt)

  ds = None
  return out

def reproject_shapefile(fp: str, srs: osr.SpatialReference, out_dir: str) -> str:
  '''Reprojects an existing layer given a spatial reference'''
  logging.info(f'reprojecting {fp}')
  driver = ogr.GetDriverByName('ESRI Shapefile')

  # check if reprojection is needed
  in_ds = driver.Open(fp)
  in_srs = in_ds.GetLayer().GetSpatialRef()

  # no spatial reference found
  if in_srs is None:
    raise baseException(f'layer: {in_ds.GetLayer().GetName()} does not have a spatial reference.',
                        baseException.ERR_INPUT_LEVEL)

  # spatial references match, no action needed
  if in_srs.IsSame(srs):
    logging.info('no reprojection required')
    in_ds.Release()
    in_ds = None
    return fp

  # copy datasource
  out = os.path.join(out_dir, os.path.basename(fp))
  out_ds = driver.CopyDataSource(in_ds, out)
  layer = out_ds.GetLayer()

  try:
    # transform
    coordTrans = osr.CoordinateTransformation(in_srs, srs)

    # copy features
    layer.ResetReading()

    for ft in layer:
      geom = ft.GetGeometryRef()
      geom.Transform(coordTrans)
      ft.SetGeometry(geom)
  except Exception as e:
    raise baseException(f'layer: {layer.GetName()} could not be reprojected.',
                        baseException.ERR_CODE_LEVEL, e)
  finally:
    in_ds.Release()
    out_ds.Release()
    in_ds, out_ds = None, None
  
  return out

def get_spref(wkt: str, deg: int) -> osr.SpatialReference:
  '''Returns an osr SpatialReference with a Central Meridian of degree'''
  with open(wkt) as w:
    srs = osr.SpatialReference()
    srs.ImportFromWkt(w.read())
    srs.SetProjParm(osr.SRS_PP_CENTRAL_MERIDIAN, deg)

  return srs